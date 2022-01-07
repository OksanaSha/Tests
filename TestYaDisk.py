import pytest
from yandex import YandexDisk


TOKEN = ''
DIR = 'test_dir'
TEST_LIST = [
    (TOKEN, DIR, 201),
    ('Q1RRR2', DIR, 401),
    (TOKEN, DIR, 409)
]

class TestCreateDir:

    @classmethod
    def teardown_class(cls):
        ya_disk = YandexDisk(TOKEN)
        ya_disk.delete_dir(DIR)


    @pytest.mark.parametrize('token,dir_name,expected_code', TEST_LIST)
    def test_create_dir(self, token, dir_name, expected_code):
        ya_disk = YandexDisk(token)
        assert ya_disk.create_dir(dir_name) == expected_code
