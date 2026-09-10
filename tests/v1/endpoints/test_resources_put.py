import uuid

import pytest

from client import YaDiskApiClient
from utils.assertions import assert_status_code, assert_schema
from models import LinkResponse, ErrorResponse

'''
PUT /v1/disk/resources
Создание папки
'''

@pytest.mark.positive
class TestCreateResourcePositive:

    def test_create_folder_success(self, client: YaDiskApiClient, unique_resource_path):
        """Успешное создание папки"""
        response = client.create_folder(unique_resource_path)
        
        assert_status_code(response, 201)
        body = assert_schema(response, LinkResponse)
        
        assert body["method"] == "GET"
        assert unique_resource_path.split("/")[-1] in body["href"]

        client.delete_resource(unique_resource_path)  # удаляем созданную папку

    def test_create_folder_with_fields(self, client: YaDiskApiClient, unique_resource_path):
        """Создание папки с фильтром полей в ответе"""
        exp_fields = "href"
        response = client.create_folder(unique_resource_path, fields=exp_fields)
        
        assert_status_code(response, 201)
        body = response.json()
        assert set(body.keys()) == set(exp_fields.split(","))

        client.delete_resource(unique_resource_path)

    def test_create_folder_in_existing_parent(self, client: YaDiskApiClient, created_folder_path, unique_resource_path):
        """Создание вложенной папки в существующую"""
        nested = f"{created_folder_path}/nested_{unique_resource_path}"
        response = client.create_folder(nested)
        assert_status_code(response, 201)
        assert_schema(response, LinkResponse)
        
        # Проверяем вложенность
        meta = client.get_resource_meta(nested)
        assert_status_code(meta, 200)
        assert meta.json()["path"].endswith(nested.split("/")[-1])


@pytest.mark.negative
class TestCreateResourceNegative:

    def test_create_folder_already_exists(self, client: YaDiskApiClient, created_folder_path):
        """Создание папки, которая уже существует"""
        response = client.create_folder(created_folder_path)
        
        assert_status_code(response, 409)
        assert_schema(response, ErrorResponse)

    def test_create_folder_without_auth(self, client_without_auth, unique_resource_path):
        """Создание папки без авторизации"""
        response = client_without_auth.create_folder(unique_resource_path)
        
        assert_status_code(response, 401)
        assert_schema(response, ErrorResponse)

    def test_create_folder_without_param_path(self, client: YaDiskApiClient):
        """Создание папки с пустым path"""
        response = client.create_folder(path=None)
        
        assert_status_code(response, 400)
        assert_schema(response, ErrorResponse)