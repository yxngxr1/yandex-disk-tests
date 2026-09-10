import pytest

from client import YaDiskApiClient
from utils.assertions import assert_status_code, assert_schema
from models import ResourceResponse, ErrorResponse

'''
GET /v1/disk/resources 
Получение метаинформации о файле или каталоге"""
'''

@pytest.mark.positive
class TestResourcesGetPositive:
    
    @pytest.mark.high
    def test_get_existing_folder(self, 
                                 client: YaDiskApiClient, 
                                 created_folder_path: str):
        """Получение мета существующей папки"""
        exp_path = created_folder_path

        response = client.get_resource_meta(exp_path)
        
        assert_status_code(response, 200)
        body = assert_schema(response, ResourceResponse)
        assert body["type"] == "dir"
        assert body["path"] == exp_path

    @pytest.mark.high
    def test_get_existing_file(self, 
                               client: YaDiskApiClient, 
                               uploaded_file_txt_by_href_path: str):
        """Получение мета существующего файла"""
        exp_path = uploaded_file_txt_by_href_path

        response = client.get_resource_meta(exp_path)
        
        assert_status_code(response, 200)
        body = assert_schema(response, ResourceResponse)
        assert body["type"] == "file"
        assert body["path"] == exp_path
        assert body["size"] > 0
        assert body["md5"] is not None

    def test_get_resource_with_fields_filter(self, 
                                             client: YaDiskApiClient):
        """Получение только выбранных полей"""
        exp_fields = "name,path"
        response = client.get_resource_meta("/", fields=exp_fields)
        
        assert_status_code(response, 200)
        body = response.json()
        assert set(body.keys()) == set(exp_fields.split(","))

    def test_get_root_folder(self, client: YaDiskApiClient):
        """Получение корневой папки"""
        response = client.get_resource_meta("/")
        
        assert_status_code(response, 200)
        assert_schema(response, ResourceResponse)
        
        data = response.json()
        assert data["type"] == "dir"
        assert data["path"] == "disk:/"


@pytest.mark.negative
class TestResourcesGetNegative:

    def test_get_not_existing_resource(self, 
                                 client: YaDiskApiClient, 
                                 deleted_resource_path: str):
        """Получение несуществующего ресурса"""
        response = client.get_resource_meta(deleted_resource_path)

        assert_status_code(response, 404)
        assert_schema(response, ErrorResponse)

    def test_get_resource_without_param_path(self, client: YaDiskApiClient):
        """Получение ресурса без обязательного параметра path"""
        response = client.get_resource_meta(path=None)

        assert_status_code(response, 400)

    @pytest.mark.critical
    def test_get_without_auth(self, client_without_auth):
        """Запрос без авторизации"""
        response = client_without_auth.get_resource_meta("mydir")
        
        assert_status_code(response, 401)
        assert_schema(response, ErrorResponse)

    