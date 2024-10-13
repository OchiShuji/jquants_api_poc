import json
import requests
import os
import boto3
import get_listed_info

BUCKET_NAME = 'jquants-knowledge-base-bucket-s3'
LISTED_INFO_KEY = 'listed_info.json'

def get_reflesh_token(mail_address, password) -> str:
    '''Obtain reflesh token (It expires in 1 week).'''
    data = {"mailaddress": f"{mail_address}", "password": f"{password}"}

    res = requests.post("https://api.jquants.com/v1/token/auth_user", data=json.dumps(data))

    if res.status_code == 200:
        value = res.json()['refreshToken']
        return value
    else:
        raise Exception(f'Failed to get idToken: {res.status_code}, {res.text}')

def get_id_token(reflesh_token: str) -> str:
    '''Obtain ID token (It expires in 24 hours).'''
    res = requests.post(f"https://api.jquants.com/v1/token/auth_refresh?refreshtoken={reflesh_token}")

    if res.status_code == 200:
        value = res.json()['idToken']
        return value
    else:
        raise Exception(f'Failed to get idToken: {res.status_code}, {res.text}')


def lambda_handler(event, context):
    if 'REFLESH_TOKEN' not in os.environ:
        raise EnvironmentError('JQUANTS_MAIL_ADDRESS or JQUANTS_PASSWORD is not set in environment variables')

    reflesh_token = os.environ['REFLESH_TOKEN']

    try:
        id_token = get_id_token(reflesh_token)
    except Exception as e:
        print(f'Error getting ID token: {e}')
        return {'statusCode': 500, 'body': 'Failed to get ID token'}

    # Get all listed info
    listed_info_json = get_listed_info.get_all_listed_info(id_token)['info']
    listed_info = ''
    for obj in listed_info_json:
        listed_info += f"{json.dumps(obj)}\n"

    s3 = boto3.resource('s3')
    s3_object = s3.Object(BUCKET_NAME, 'listed_info/listed_info.json')
    
    try:
        res = s3_object.put(Body=listed_info,ContentType='application/json')
        return {'statusCode': 200, 'body': 'Succeed!'}
    except Exception as e:
        print(f'Error putting object to S3')
        return {'statusCode': 500, 'body': 'Failed to put object to S3'}



