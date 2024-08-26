import requests
import json
import base64

def get_session_key():
    url = 'https://prelead-admin.limesurvey.net/admin/remotecontrol'

    payload = {
        "method" : "get_session_key",
        "params" : ["prelead-admin", "Siddharth.ad2b"],
        "id" : 1
    }

    headers = {
        "Content-Type" : "application/json",
        "User-Agent": "Defined",
    }

    response = requests.request("POST", url, json=payload, headers=headers, verify=False)
    key_dict = json.loads(response.text)
    key = key_dict['result']

    return str(key)

def get_latest_suggestion():
    key = get_session_key()
    url = 'https://prelead-admin.limesurvey.net/admin/remotecontrol'
    payload = {
        "method": "export_responses",
        "params": [key, 288439, 'json', 'en'],
        "id": 1
    }
    headers = {
        "Content-Type" : "application/json",
        "Connection": "Keep-Alive",
        "User-Agent": "Defined",
    }
    response = requests.post(url=url, json=payload, headers=headers, verify=False)
    response_data = response.json()
    encoded_survey_response_data = response_data['result']
    survey_response_data = json.loads(base64.b64decode(encoded_survey_response_data).decode('utf-8'))
    latest_response = survey_response_data['responses'][-1]
    suggestion = latest_response["G02Q03"]
    return suggestion

