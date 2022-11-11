import requests
import json
import urllib3
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
    print(access_js)
    """store access token"""
    key = access_js["access_token"]
    header = {
        'Authorization': 'Bearer ' + key,
        'accept': 'application/json'
    }

    return header

decoded_url = '''https://demo.flowmon.com/rest/ads/events?async=0&count=1&limit=1&offset=0&orderBy=["time desc"]&search={
  "from": "2022-07-24 11:00",
  "to": "2022-08-25 11:00",
  "source": [
    "192.168.70.*"
  ],
  "target": [
    "209.99.40.*"
  ],
  "perspective": 4
}'''

def get_events_id():
    return "https://demo.flowmon.com/rest/ads/events?async=0&count=1&limit=1&offset=0&orderBy=[%22time desc%22%5D&search=%7B%0A  %22from%22%3A %222022-07-24 11%3A00%22%2C%0A  %22to%22%3A %222022-08-25 11%3A00%22%2C%0A  %22source%22%3A %5B%0A    %22192.168.70.*%22%0A  %5D%2C%0A  %22target%22%3A %5B%0A    %22209.99.40.*%22%0A  %5D%2C%0A  %22perspective%22%3A 4%0A%7D"

def print_responce(url):
    header = connect()
    data = requests.get(url, headers=header, verify=False)
    f = open(f"dataa.json", "w")
    f.write(data.text)
    f.close()


if __name__ == '__main__':
    #working_url = "https://demo.flowmon.com/rest/ads/events?count=1&orderBy=%5B%22time%20desc%22%5D&search=%7B%0A%20%20%22from%22%3A%20%222020-07-24%2011%3A00%22%2C%0A%20%20%22to%22%3A%20%222022-07-25%2011%3A00%22%0A%7D"
    #print_responce(working_url)
    #print_responce(get_events_id())
    print_responce(decoded_url)
