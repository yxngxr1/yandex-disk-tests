import pytest

from client.disk_client import YaDiskApiClient
from utils.assertions import assert_status_code

'''
GET /v1/disk
Получение метаинформации о диске
'''

@pytest.mark.endpoint
@pytest.mark.positive
def test_get_disk_meta_success(client: YaDiskApiClient):
    """Успешное получение"""
    response = client.get_disk_meta()
    assert_status_code(response, 200)

@pytest.mark.endpoint
@pytest.mark.negative
def test_get_disk_meta_without_auth(client_without_auth: YaDiskApiClient):
    """Получение без авторизации"""
    response = client_without_auth.get_disk_meta()
    assert_status_code(response, 401)
        