import pytest

from client.disk_client import YaDiskApiClient
from utils.assertions import assert_status_code


@pytest.mark.medium
@pytest.mark.positive
def test_get_disk_meta(client: YaDiskApiClient):
    """Получение метаинформации о диске"""
    response = client.get_disk_meta()
    assert_status_code(response, 200)

    
