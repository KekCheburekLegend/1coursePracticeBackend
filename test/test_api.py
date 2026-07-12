import sys
import os
from pathlib import Path

# Добавляем корневую папку проекта в PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

import os
os.environ["DB_URL"] = "sqlite:///./test.db"

# Самый простой вариант без фикстур
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app
from database import get_db


def test_create_url():
    # 1. Создаем мок
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.side_effect = [None, None]

    # 2. Подменяем БД
    app.dependency_overrides[get_db] = lambda: mock_db

    # 3. Тестируем
    client = TestClient(app)
    response = client.post("/post/url", json={"url": "https://example.com"})

    # 4. Проверяем
    assert response.status_code == 200

    # 5. Очищаем
    app.dependency_overrides.clear()


def test_redirect():
    # 1. Мок с существующим URL
    mock_db = MagicMock()

    # Создаем объект URLS
    from model import URLS
    url_entry = URLS(id="abc123", url="https://example.com")
    mock_db.query.return_value.filter.return_value.first.return_value = url_entry

    # 2. Подменяем
    app.dependency_overrides[get_db] = lambda: mock_db

    # 3. Тестируем
    client = TestClient(app)
    response = client.get("/abc123", follow_redirects=False)

    # 4. Проверяем
    assert response.status_code == 302
    assert response.headers["location"] == "https://example.com"

    # 5. Очищаем
    app.dependency_overrides.clear()


if __name__ == "__main__":
    test_create_url()
    test_redirect()
    print("Все тесты пройдены!")