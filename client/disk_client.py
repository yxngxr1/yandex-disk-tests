from .base_client import BaseApiClient
from .endpoints import Endpoints

class YaDiskApiClient(BaseApiClient):
    """
    Клиент для REST API Яндекс.Диска

    Каждый метод - один endpoint из API. Возвращают requests.Response
    """

    def __init__(self, base_url, token):
        super().__init__(base_url, token)

    def get_disk_meta(self):
        """GET /v1/disk - общая информация о Диске"""
        return self._get(Endpoints.DISK_META)

    def get_resource_meta(self, 
                          path: str, 
                          **params):
        """GET /v1/disk/resources - метаинформация о файле или каталоге по path"""
        return self._get(Endpoints.RESOURCES, params={"path": path, **params})

    def create_folder(self, 
                      path: str, 
                      **params):
        """PUT /v1/disk/resources - создать пустой каталог по path"""
        return self._put(Endpoints.RESOURCES, params={"path": path, **params})

    def delete_resource(self, 
                        path: str, 
                        force_async: bool = False, 
                        permanently: bool = False, 
                        **params):
        """
        DELETE /v1/disk/resources - удалить файл или папку по path

        :param force_async: Выполнить асинхронно
        :type force_async: bool
        :param permanently: Удалить не помещая в корзину
        :type permanently: bool
        """
        return self._delete(
            Endpoints.RESOURCES, 
            params={"path": path, 
                    "force_async": force_async, 
                    "permanently": permanently,
                    **params}
        )

    def copy_resource(self, 
                      from_path: str, 
                      path: str, 
                      **params):
        """POST /v1/disk/resources/copy — скопировать ресурс из from_path в path."""
        return self._post(
            f"{Endpoints.RESOURCES}/copy",
            params={"from": from_path, 
                    "path": path, 
                    **params},
        )