from typing import Type
from pydantic import BaseModel
from requests import Response
from models import *

def assert_status_code(response: Response, expected_code):
    """
    Сравнивает код ответа от сервера с ожидаемым
    :param response: полученный от сервера ответ
    :param expected_code: ожидаемый код ответа
    :raises AssertionError: если значения не совпали
    """
    assert expected_code == response.status_code


def assert_schema(response, model: Type[BaseModel]) -> dict:
    """
    Проверяет тело ответа на соответствие его схеме механизмами pydantic
    :param response: ответ от сервера
    :param model: модель, по которой будет проверяться схема json
    :raises ValidationError: если тело ответа не соответствует схеме
    """

    # 1. Пустое тело
    if not response.content:
        raise AssertionError(
            f"Ожидалось тело ответа по схеме {model.__name__}, "
            f"но получен пустой ответ (status={response.status_code})"
        )

    # 2. Тело не JSON
    try:
        body = response.json()
    except ValueError as e:
        raise AssertionError(
            f"Ожидался JSON по схеме {model.__name__}, "
            f"но тело не является JSON: {response.text!r}"
        )

    body = response.json()
    if isinstance(body, list):
        for item in body:
            model.model_validate(item, strict=True)
    else:
        model.model_validate(body, strict=True)
    return body