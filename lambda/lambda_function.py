import json
import requests
import os
import boto3

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

def get_all_listed_info(id_token: str) -> str:
    headers = {'Authorization': f'Bearer {id_token}'}
    res = requests.get("https://api.jquants.com/v1/listed/info", headers=headers)

    if res.status_code != 200:
        print(f'Failed to get listed info: {r.status_code}, {r.text}')
        return {'statusCode': r.status_code, 'body': 'Failed to get listed info'}

    return res.json()
    
def lambda_handler(event, context):
    if 'REFLESH_TOKEN' not in os.environ:
        raise EnvironmentError('JQUANTS_MAIL_ADDRESS or JQUANTS_PASSWORD is not set in environment variables')

    reflesh_token = os.environ['REFLESH_TOKEN']

    try:
        id_token = get_id_token(reflesh_token)
        print(id_token)
    except Exception as e:
        print(f'Error getting ID token: {e}')
        return {'statusCode': 500, 'body': 'Failed to get ID token'}

    listed_info = get_all_listed_info(id_token)
    s3 = boto3.resource('s3')
    s3_object = s3.Object(BUCKET_NAME, LISTED_INFO_KEY)

    try:
        res = s3_object.put(Body=listed_info)
        return listed_info
    except Exception as e:
        print(f'Error putting object to S3: {e}')
        return {'statusCode': 500, 'body': 'Failed to put object'}

