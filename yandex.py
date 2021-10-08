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

    def _get_upload_link(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': disk_file_path, 'overwrite': 'true'}
        response = requests.get(url=upload_url, params=params, headers=headers)
        return response.json()

    def upload_file(self, disk_file_path, file):
        response = self._get_upload_link(disk_file_path=disk_file_path)
        url = response.get('href', '')
        if url:
            response = requests.put(url=url, data=open(file, 'rb'))
            response.raise_for_status()
            if response.status_code == 201:
                print('Success')
        else:
            print('Empty url')