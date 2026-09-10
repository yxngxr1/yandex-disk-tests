import uuid

import pytest

from client import YaDiskApiClient
from utils.assertions import assert_status_code, assert_schema
from models import LinkResponse, ErrorResponse, DeleteResourceResponse

'''
DELETE /v1/disk/resources
Удаление файла или папки
'''


@pytest.mark.positive
class TestResourcesDeletePositive:

    def test_delete_folder_success(self, client: YaDiskApiClient, created_folder_path: str):
        """Успешное удаление папки в корзину"""
        response = client.delete_resource(created_folder_path, permanentrly=False)
        
        assert_status_code(response, 204)
        #assert_schema(response, DeleteResourceResponse) ничего не приходит

        # Проверяем, что ресурс больше не доступен
        meta = client.get_resource_meta(created_folder_path)
        assert_status_code(meta, 404)

        client.delete_from_trash()

    def test_delete_file_permanently(self, client: YaDiskApiClient, created_folder_path: str):
        """Успешное удаление файла минуя корзину"""
        response = client.delete_resource(created_folder_path, permanently=True)
        
        assert_status_code(response, 204)
        
        meta = client.get_resource_meta(created_folder_path)
        assert_status_code(meta, 404)


@pytest.mark.negative
class TestResourcesDeleteNegative:

    def test_delete_not_existing_resource(self, client: YaDiskApiClient, unique_resource_path: str):
        """Удаление несуществующего ресурса"""
        response = client.delete_resource(unique_resource_path)
        
        assert_status_code(response, 404)
        assert_schema(response, ErrorResponse)

    def test_delete_without_auth(self, client_without_auth, created_folder_path: str):
        """Удаление без авторизации"""
        response = client_without_auth.delete_resource(created_folder_path)
        
        assert_status_code(response, 401)
        assert_schema(response, ErrorResponse)