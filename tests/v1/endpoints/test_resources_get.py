import pytest

from client import YaDiskApiClient
from utils.assertions import assert_status_code, assert_schema
from models import ResourceResponse

class TestResourcesGet:

    @pytest.mark.high
    @pytest.mark.positive
    def test_get_existing_folder(self, 
                                 client: YaDiskApiClient, 
                                 created_folder_path: str):
        """Получение существующей папки"""
        exp_path = created_folder_path

        response = client.get_resource_meta(exp_path)
        
        assert_status_code(response, 200)
        body = assert_schema(response, ResourceResponse)
        
        assert body["path"] == exp_path
        assert body["type"] == "dir"

