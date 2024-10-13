import json
import requests

def get_all_listed_info(id_token: str) -> str:
    headers = {'Authorization': f'Bearer {id_token}'}
    res = requests.get("https://api.jquants.com/v1/listed/info", headers=headers)

    if res.status_code != 200:
        print(f'Failed to get listed info: {res.status_code}')
        return {'statusCode': res.status_code, 'body': 'Failed to get listed info'}

    return res.json()
