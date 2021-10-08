import requests
from pprint import pprint


class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def _get_upload_link(self, path_to_file):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': path_to_file}
        response = requests.get(url=upload_url, params=params, headers=headers)
        pprint(response.json())
        return response.json()