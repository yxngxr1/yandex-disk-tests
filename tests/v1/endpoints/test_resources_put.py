import pytest

from client import YaDiskApiClient
from utils.assertions import assert_status_code, assert_schema
from models import ResourceResponse, ErrorResponse

'''
PUT /v1/disk/resources
Создание папки
'''

class TestResourcesPut:

    def test_create_folder_success(client: YaDiskApiClient):
        pass