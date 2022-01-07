import requests


class YandexDisk:

    def __init__(self, token):
        self.token = token
        self.headers = self.get_headers()

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def _get_upload_link(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.headers
        params = {'path': disk_file_path, 'overwrite': 'true'}
        response = requests.get(url=upload_url, params=params, headers=headers)
        return response.json()

    def upload_file(self, disk_file_path, file):
        dir_name = disk_file_path.split('/')[0]
        if not self.is_dir_on_disk(dir_name):
            self.create_dir(dir_name)
        response = self._get_upload_link(disk_file_path=disk_file_path)
        url = response.get('href', '')
        if url:
            response = requests.put(url=url, data=open(file, 'rb'))
            response.raise_for_status()
            if response.status_code == 201:
                print('Success')
                return True
        else:
            print('Empty url')

    def create_dir(self, new_dir):
        headers = self.headers
        params = {'path': new_dir}
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        response = requests.put(url=url, headers=headers, params=params)
        return response.status_code

    def is_dir_on_disk(self, dir_name):
        headers = self.headers
        params = {'path': dir_name}
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        response = requests.get(url=url, headers=headers, params=params)
        response.raise_for_status()
        if response.status_code == 200:
            return True

    def delete_dir(self, dir_name):
        headers = self.headers
        params = {'path': dir_name, 'permanently': True}
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        response = requests.delete(url=url, headers=headers, params=params)
        return response.status_code