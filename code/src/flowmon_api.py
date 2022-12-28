import requests
import json
import urllib3
import warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def connect():
    """input here your flowmon username and password"""
    auth_header = {
        'grant_type': 'password',
        'client_id': 'invea-tech',
        'username': 'demo',
        'password': 'demo'
    }
    oauth_token = '/resources/oauth/token'
    auth_str = 'https://demo.flowmon.com' + oauth_token

    """sending auth data to server and receive auth token"""
    auth = requests.post(auth_str, data=auth_header, verify=False)
    access_js = json.loads(auth.text)
    """store access token"""
    key = access_js["access_token"]
    header = {
        'Authorization': 'Bearer ' + key,
        'accept': 'application/json'
    }
    return header


def is_real_event(event_id: int) -> bool:
    url = f"https://demo.flowmon.com/rest/ads/event/{event_id}?targets=1"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        header = connect()
        response = requests.get(url, headers=header, verify=False)
    return str(response.status_code).startswith("2")


def print_responce(url):
    header = connect()
    data = requests.get(url, headers=header, verify=False)
    f = open(f"dataa.json", "w")
    f.write(data.text)
    f.close()


if __name__ == '__main__':
    pass
