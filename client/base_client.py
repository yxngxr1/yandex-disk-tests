import requests

class BaseApiClient:
    """
    Базовый класс, обёртка над requests.Session.

    Реализованы методы HTTP: GET, POST, PUT и DELETE.
    Ничего не знает о эндпоинтах API — логикой занимается дочерний DiskApiClient.
    """

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"OAuth {token}",
                "Content-Type": "application/json",
            }
        )

    def close(self):
        self.session.close()

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"
    
    # http методы

    def _get(self, path: str, params: dict = None, **kwargs) -> requests.Response:
        return self.session.get(
            self._url(path), params=params, **kwargs
        )

    def _post(self, path: str, params: dict = None, json: dict = None, data=None, **kwargs) -> requests.Response:
        return self.session.post(
            self._url(path),
            params=params,
            json=json,
            data=data,
            **kwargs,
        )

    def _put(self, path: str, params: dict = None, json: dict = None, data=None, **kwargs) -> requests.Response:
        return self.session.put(
            self._url(path),
            params=params,
            json=json,
            data=data,
            **kwargs,
        )

    def _delete(self, path: str, params: dict = None, **kwargs) -> requests.Response:
        return self.session.delete(
            self._url(path), params=params, **kwargs
        )

