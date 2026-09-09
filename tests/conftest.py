import pytest
import uuid
from client import Config, YaDiskApiClient

def pytest_configure(config):
    Config.validate()  # проверка переменных перед тестом

@pytest.fixture(scope="session")
def client():
    """Создаёт клиент API на всю сессию тестов и закрывает его по окончании."""
    client = YaDiskApiClient(Config.BASE_URL, Config.TOKEN)
    yield client
    client.close()

@pytest.fixture
def unique_resource_path() -> str:
    """Возвращает уникальное имя для нового ресурса"""
    return f"disk:/test_resource_{uuid.uuid4()}"

@pytest.fixture
def created_folder_path(client: YaDiskApiClient, unique_resource_path):
    """Создаёт пустой каталог до теста и удаляет её после (без корзины). Возвращает path."""
    client.create_folder(unique_resource_path)
    yield unique_resource_path
    client.delete_resource(unique_resource_path, permanently=True)