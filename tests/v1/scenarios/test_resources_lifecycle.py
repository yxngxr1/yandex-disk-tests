# tests/v1/scenarios/test_resources_lifecycle.py
import uuid

import pytest

from client import YaDiskApiClient
from utils.assertions import assert_status_code, assert_schema
from models import ResourceResponse, LinkResponse, ErrorResponse


'''
Жизненный цикл ресурса:
create folder -> get -> create file -> get -> copy file to folder -> get -> delete folder with permamently=False -> clear trash
'''

@pytest.mark.scenario
@pytest.mark.positive
def test_resources_lifecycle(client: YaDiskApiClient):
    # Уникальные имена
    base_name = f"lifecycle_{uuid.uuid4()}"
    folder_path = f"disk:/{base_name}"
    file_path = f"disk:/{base_name}_file.txt"
    copied_file_path = f"{folder_path}/{base_name}_file.txt"

    try:
        # Создание папки
        create_folder_response = client.create_folder(folder_path)
        assert_status_code(create_folder_response, 201)
        assert_schema(create_folder_response, LinkResponse)

        # Получение меты папки
        folder_meta_response = client.get_resource_meta(folder_path)
        assert_status_code(folder_meta_response, 200)
        folder_meta = assert_schema(folder_meta_response, ResourceResponse)
        assert folder_meta["type"] == "dir"
        assert folder_meta["path"] == folder_path
        assert folder_meta["name"] == base_name

        # Создание файла
        upload_link_response = client.get_upload_link(file_path, overwrite=True)
        assert_status_code(upload_link_response, 200)
        href = upload_link_response.json()["href"]
        client.upload_file_by_link(href, b"TEXT EXAMPLE TEXT")

        # Получение меты файла
        file_meta_response = client.get_resource_meta(file_path)
        assert_status_code(file_meta_response, 200)
        file_meta = assert_schema(file_meta_response, ResourceResponse)
        assert file_meta["type"] == "file"
        assert file_meta["path"] == file_path
        assert file_meta["size"] > 0
        assert file_meta["md5"] is not None

        # Копирование в папку
        copy_response = client.copy_resource(
            from_path=file_path,
            path=copied_file_path
        )
        assert_status_code(copy_response, 201)
        assert_schema(copy_response, LinkResponse)

        # Получение меты копии
        copied_meta_response = client.get_resource_meta(copied_file_path)
        assert_status_code(copied_meta_response, 200)
        copied_meta = assert_schema(copied_meta_response, ResourceResponse)
        assert copied_meta["type"] == "file"
        assert copied_meta["path"] == copied_file_path

        # Проверка оригинала
        original_meta = client.get_resource_meta(file_path)
        assert_status_code(original_meta, 200)

        # Удаление папки
        delete_folder_response = client.delete_resource(folder_path, force_async=False)
        assert delete_folder_response.status_code in [202, 204]
        if delete_folder_response.status_code == 202:
            operation_href = delete_folder_response.json()["href"]
            operation_id = operation_href.rstrip("/").split("/")[-1]
            status = client.wait_for_operation(operation_id)
            assert status == "success"

        # Проверка, что папка удалена
        deleted_folder_meta = client.get_resource_meta(folder_path)
        assert_status_code(deleted_folder_meta, 404)
        assert_schema(deleted_folder_meta, ErrorResponse)

        # Очистка корзины
        clear_trash_response = client.delete_from_trash("/")
        assert clear_trash_response.status_code in [202, 204]
        if clear_trash_response.status_code == 202:
            operation_href = clear_trash_response.json()["href"]
            operation_id = operation_href.rstrip("/").split("/")[-1]
            status = client.wait_for_operation(operation_id)
            assert status == "success"

    finally:
        # очистка всех созданных ресурсов
        for path in [file_path, folder_path]:
            try:
                client.delete_resource(path, permanently=True)
            except Exception:
                pass