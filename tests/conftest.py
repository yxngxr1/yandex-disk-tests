import pytest
import uuid
from client import Config, YaDiskApiClient

def pytest_configure(config):
    Config.validate()  # проверка переменных перед тестом

@pytest.fixture(scope="session")
def client():
    """Создаёт и возвращает клиент API на всю сессию тестов и закрывает его по окончании."""
    client = YaDiskApiClient(Config.BASE_URL, Config.TOKEN)
    yield client
    client.close()

@pytest.fixture
def unique_resource_path() -> str:
    """Возвращает уникальное имя для нового ресурса"""
    return f"test_resource_{uuid.uuid4()}"

@pytest.fixture
def created_folder_path(client: YaDiskApiClient, unique_resource_path):
    """Создаёт пустой каталог до теста и удаляет её после (без корзины). Возвращает path."""
    client.create_folder(unique_resource_path)
    yield unique_resource_path
    client.delete_resource(unique_resource_path, permanently=True)

@pytest.fixture
def uploaded_file_txt_by_href_path(client: YaDiskApiClient, unique_resource_path):
    """Создаёт небольшой файл до теста и удаляет его после (без корзины). Возвращает path."""
    file_path = f"{unique_resource_path}.txt"
    upload_response = client.get_upload_link(file_path, overwrite=True)
    href = upload_response.json()["href"]
    client.upload_file_by_link(href, b"TEXT EXAMPLE TEXT")
    yield file_path
    client.delete_resource(file_path, permanently=True)

@pytest.fixture
def client_without_auth():
    """API-клиент без OAuth-токена — для проверки неавторизованных запросов"""
    client = YaDiskApiClient(base_url=Config.BASE_URL, token="")
    yield client
    client.close()