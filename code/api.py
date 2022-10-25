import requests
import json

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
    print(access_js)
    """store access token"""
    key = access_js["access_token"]
    header = {
        'Authorization': 'Bearer ' + key,
        'accept': 'application/json'
    }

    return header


if __name__ == '__main__':
	header = connect()
	url = f"https://demo.flowmon.com/rest/ads/events?count=1&orderBy=%5B%22time%20desc%22%5D&search=%7B%0A%20%20%22from%22%3A%20%222020-07-24%2011%3A00%22%2C%0A%20%20%22to%22%3A%20%222022-07-25%2011%3A00%22%0A%7D"
        data = requests.get(url, headers=header, verify=False)

        f = open(f"ismdata.json", "w")
        f.write(data.text)
        f.close()

