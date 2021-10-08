import requests
from pprint import pprint

from yandex import YandexDisk

TOKEN = ''

if __name__ == '__main__':
    my_yandex = YandexDisk(TOKEN)
    my_yandex.upload_file('netology/toni_stark.jpg', 'toni_stark.jpg')