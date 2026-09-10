import pytest

from client import YaDiskApiClient
from utils.assertions import assert_status_code, assert_schema
from models import LinkResponse, ErrorResponse

'''
POST /v1/disk/resources/copy
Копирование файла или папки
'''


@pytest.mark.positive
class TestResourcesCopyPositive:

    def test_copy_folder_success(self,
                                 client: YaDiskApiClient,
                                 created_folder_path: str):
        """Успешное копирование папки"""
        copy_path = f"{created_folder_path}_copy"

        response = client.copy_resource(
            from_path=created_folder_path,
            path=copy_path
        )

        assert_status_code(response, 201)
        assert_schema(response, LinkResponse)

        # Проверяем, что копия создана
        meta = client.get_resource_meta(copy_path)
        assert_status_code(meta, 200)
        body = meta.json()

        assert body["type"] == "dir"

        client.delete_resource(copy_path, permanently=True)

    def test_copy_file_success(self,
                               client: YaDiskApiClient,
                               uploaded_file_txt_by_href_path: str):
        """Успешное копирование файла"""
        copy_path = f"{uploaded_file_txt_by_href_path}_copy.txt"

        response = client.copy_resource(
            from_path=uploaded_file_txt_by_href_path,
            path=copy_path,
        )

        assert_status_code(response, 201)
        assert_schema(response, LinkResponse)

        # Проверяем, что копия создана
        copy_meta = client.get_resource_meta(copy_path, fields='path,name,type,size')
        assert_status_code(copy_meta, 200)
        body_copy = copy_meta.json()
        assert body_copy["type"] == "file"

        # Сверяем с оригиналом
        orig_meta = client.get_resource_meta(uploaded_file_txt_by_href_path, fields='path,name,size')
        assert_status_code(orig_meta, 200)
        body_orig = orig_meta.json()

        assert body_orig["path"] != body_copy["path"]
        assert body_orig["name"] != body_copy["name"]
        assert body_orig["size"] == body_copy["size"]
        
        client.delete_resource(copy_path, permanently=True)


@pytest.mark.negative
class TestResourcesCopyNegative:

    def test_copy_not_existing_resource(self,
                                        client: YaDiskApiClient,
                                        unique_resource_path: str):
        """Копирование несуществующего ресурса"""
        response = client.copy_resource(
            from_path=unique_resource_path,
            path=f"{unique_resource_path}_copy"
        )

        assert_status_code(response, 404)
        assert_schema(response, ErrorResponse)

    def test_copy_without_param_path(self,
                                        client: YaDiskApiClient,
                                        created_folder_path: str):
        """Копирование без параметра path"""
        response = client.copy_resource(
            from_path=created_folder_path,
            path=None
        )

        assert_status_code(response, 400)
        assert_schema(response, ErrorResponse)

    def test_copy_without_auth(self,
                               client_without_auth,
                               created_folder_path: str,
                               unique_resource_path: str):
        """Копирование без авторизации"""
        response = client_without_auth.copy_resource(
            from_path=created_folder_path,
            path=f"{unique_resource_path}_copy"
        )

        assert_status_code(response, 401)
        assert_schema(response, ErrorResponse)