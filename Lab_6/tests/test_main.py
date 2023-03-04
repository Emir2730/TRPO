import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from src.models.core import Base
from src.dependencies.db import db_session
from src.main import app

SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.drop_all(bind=engine)  # Удалем таблицы из БД
Base.metadata.create_all(bind=engine)  # Создаем таблицы в БД


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[db_session] = override_get_db


@pytest.fixture(scope='session')
def app_client() -> TestClient:
    client = TestClient(app)

    return client


def test_create_user(app_client):
    data = {
        'first_name': 'firstname',
        'last_name': 'lastname',
        'middle_name': 'middlename',
    }

    response = app_client.post('/users', json=data)
    response_data = response.json()

    assert response_data['first_name'] == data['first_name'], response.json()


def test_update_user(app_client):
    data = {
        'first_name': 'firstname',
        'last_name': 'lastname',
        'middle_name': 'middlename',
    }

    response = app_client.put('/users/1', json=data)
    response_data = response.json()

    assert response_data['first_name'] == data['first_name'], response.json()


def test_get_users(app_client):
    response = app_client.get('/users')
    response_data = response.json()

    assert len(response_data['data']) != 0, response_data


def test_get_user(app_client):
    response = app_client.get('/users/1')
    response_data = response.json()

    assert response_data['id'], response_data


def test_create_book(app_client):
    data = {
        'name': 'name',
        'isbn': '392352-23523i',
        'edition': 123,
        'expenses': 123.123,
        'publication_date': str(datetime.date.today()),
        'price': 100.500,
        'total_royalti': 100.500,
    }

    response = app_client.post('/books', json=data)
    response_data = response.json()

    assert response_data['name'] == data['name'], response.json()


def test_update_book(app_client):
    data = {
        'name': 'another_name',
        'isbn': '392352-23523i',
        'edition': 123,
        'expenses': 123.123,
        'publication_date': str(datetime.date.today()),
        'price': 100.500,
        'total_royalti': 100.500,
    }

    response = app_client.put('/books/1', json=data)
    response_data = response.json()

    assert response_data['name'] == data['name'], response.json()


def test_get_books(app_client):
    response = app_client.get('/books')
    response_data = response.json()

    assert len(response_data['data']) != 0, response_data


def test_get_book(app_client):
    response = app_client.get('/books/1')
    response_data = response.json()

    assert response_data['id'], response_data


def test_create_contract(app_client):
    data = {
        'number': 1,
        'signing_date': str(datetime.datetime.utcnow()),
        'term': 123,
        'is_terminate': True,
        'terminate_date': str(datetime.datetime.utcnow()),
        'author_id': 1,
    }

    response = app_client.post('/contracts', json=data)
    response_data = response.json()

    assert response_data['number'] == data['number'], response.json()


def test_update_contract(app_client):
    data = {
        'number': 1,
        'signing_date': str(datetime.datetime.utcnow()),
        'term': 123,
        'is_terminate': True,
        'terminate_date': str(datetime.datetime.utcnow()),
        'author_id': 1,
    }

    response = app_client.put('/contracts/1', json=data)
    response_data = response.json()

    assert response_data['number'] == data['number'], response.json()


def test_get_contracts(app_client):
    response = app_client.get('/contracts')
    response_data = response.json()

    assert len(response_data['data']) != 0, response_data


def test_get_contract(app_client):
    response = app_client.get('/contracts/1')
    response_data = response.json()

    assert response_data['id'] == 1, response_data


def test_create_author(app_client):
    data = {
        'passport': '7019 24825',
        'address': 'some address',
        'phone': '+7 924 249-55-55',
        'user_id': 1
    }

    response = app_client.post('/authors', json=data)
    response_data = response.json()

    assert response_data['passport'] == data['passport'], response.json()


def test_update_author(app_client):
    data = {
        'passport': '7019 24825',
        'address': 'some address',
        'phone': '+7 924 249-55-55',
        'user_id': 1
    }

    response = app_client.put('/authors/1', json=data)
    response_data = response.json()

    assert response_data['passport'] == data['passport'], response.json()


def test_get_authors(app_client):
    response = app_client.get('/authors')
    response_data = response.json()

    assert len(response_data['data']) != 0, response_data


def test_get_author(app_client):
    response = app_client.get('/authors/1')
    response_data = response.json()

    assert response_data['id'], response_data


def test_create_customer(app_client):
    data = {
        'name': 'some name',
        'address': 'some address',
        'phone': '+7 924 249-55-55',
        'user_id': 1
    }

    response = app_client.post('/customers', json=data)
    response_data = response.json()

    assert response_data['name'] == data['name'], response.json()


def test_update_customer(app_client):
    data = {
        'name': 'some name',
        'address': 'some address',
        'phone': '+7 924 249-55-55',
        'user_id': 1
    }

    response = app_client.put('/customers/1', json=data)
    response_data = response.json()

    assert response_data['name'] == data['name'], response.json()


def test_get_customers(app_client):
    response = app_client.get('/customers')
    response_data = response.json()

    assert len(response_data['data']) != 0, response_data


def test_get_customer(app_client):
    response = app_client.get('/customers/1')
    response_data = response.json()

    assert response_data['id'], response_data


def test_create_order(app_client):
    data = {
        'identifier': 123,
        'closed_at': str(datetime.datetime.utcnow() + datetime.timedelta(days=10)),
        'count': 5,
        'book_id': 1,
        'customer_id': 1
    }

    response = app_client.post('/orders', json=data)
    response_data = response.json()

    assert response_data['count'] == data['count'], response.json()


def test_update_order(app_client):
    data = {
        'identifier': 123,
        'closed_at': str(datetime.datetime.utcnow() + datetime.timedelta(days=10)),
        'count': 10,
    }

    response = app_client.put('/orders/1', json=data)
    response_data = response.json()

    assert response_data['count'] == data['count'], response.json()


def test_get_orders(app_client):
    response = app_client.get('/orders')
    response_data = response.json()

    assert len(response_data['data']) != 0, response_data


def test_get_order(app_client):
    response = app_client.get('/orders/1')
    response_data = response.json()

    assert response_data['id'], response_data