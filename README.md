# Yandex Disk Tests

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![pytest](https://img.shields.io/badge/pytest-9.1.1-brightgreen)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Автотесты REST API для сервиса **Яндекс.Диск**

---

## Оглавление
- [Описание](#описание)
- [Требования](#требования)
- [Воспроизведение](#воспроизведение)
- [Запуск тестов](#запуск-тестов)
- [Структура проекта](#структура-проекта)

---

## Описание
Тестовое задание для отбора на стажировку в Яндекс.Диск по направлению тестирование. Проект автотестов для открытого Api Диска ([документация](https://yandex.ru/dev/disk/rest)).
Стек: **Python: pytest · pytest-html · requests · pydantic · python-dotenv**

---

## Воспроизведение

0. **Установите python:**
   - Установите **Python 3.10+** ([официальный сайт](https://www.python.org/downloads/))  
   - Получите **OAuth‑токен** для Яндекс.Диск ([дайте два](https://yandex.ru/dev/disk-api/doc/ru/concepts/quickstart))

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/yxngxr1/yandex-disk-tests.git
   cd yandex-disk-tests
    ```

2. **Создайте и активируйте виртуальное окружение:**
    ```bash
    python -m venv .venv
    ```
    | OS | Команда активации |
    |----------------------|-------------------|
    | macOS / Linux (bash, zsh) | `source .venv/bin/activate` |
    | Windows (cmd) | `.venv\Scripts\activate.bat` |
    | Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |

3. **Установите зависимости:**
    ```
    pip install -r requirements.txt
    ```

4. **Задайте переменные окружения:**
Создайте .env в корне проекта по примеру с .env.example. Заполните OAUTH_TOKEN

## Запуск тестов

```bash
# Все тесты
pytest

# С генерацией HTML‑отчёта
pytest --html=report.html --self-contained-html

# Запуск конкретного теста
pytest tests/v1/endpoints/test_resources_get.py

# Запуск с определённой маркировкой
pytest -m positive
```

## Структура проекта

```
yandex-disk-tests/
├── client/                  # HTTP‑клиент для работы с API
│   ├── __init__.py
│   ├── base_client.py       # Базовый клиент с обёрткой над requests (методы HTTP)
│   ├── config.py            # Загрузка конфигурации из .env
│   ├── disk_client.py       # Сервисный клиент для Яндекс.Диск (методы API)
│   └── endpoints.py         # Константы URL‑эндпоинтов 
├── models/                  # Pydantic‑модели для ответов API
│   ├── __init__.py
│   └── response.py          # Модели ресурсов, ошибок и других
├── tests/                   # Тесты
│   ├── v1/                  # Версия API
│   │   ├── endpoints/       # Тесты отдельных эндпоинтов
│   │   │   ├── test_resources_get.py
│   │   │   └── ...          
│   │   ├── scenarios/       # Комплексные сценарии (e2e)
│   │   │   └── ...           
│   │   └── conftest.py      # Фикстуры pytest
├── utils/                   # Вспомогательные утилиты
│   └── assertions.py        # Переиспользуемые проверочные функции
├── .env.example             # Шаблон переменных окружения
├── .gitignore               # Список игнорируемых файлов для СКВ git
├── pytest.ini               # Конфигурация pytest
├── README.models            # --> Вы тут <--
├── requirements.txt         # Зависимости
└── TODO.md                  # План развития
```