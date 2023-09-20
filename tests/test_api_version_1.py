import requests
from jsonschema.validators import validate
from utils.helper import load_schema


def test_users_status_code():

    response = requests.get(url='https://reqres.in/api/users?per_page=2')
    
    assert response.status_code == 200


def test_users_per_page():
    per_page = 3

    response = requests.get(
        url='https://reqres.in/api/users?per_page=3',
        params={'per_page': per_page}
    )

    assert response.json()['per_page'] == per_page
    assert len(response.json()['data']) == per_page


def test_user_schema():
    schema = load_schema('get_users_schema.json')
    response = requests.get(url='https://reqres.in/api/users')

    validate(instance=response.json(), schema=schema)


def test_users_not_found_status_code():
    response = requests.get(url='https://reqres.in/api/users/23')

    assert response.status_code == 404


def test_create_user():
    response = requests.post(
        url='https://reqres.in/api/users',
        data={'name': 'TestUser',
              'job': 'Worker'}
    )
    assert response.status_code == 201
    assert response.json()['name'] == 'TestUser'
    assert response.json()['job'] == 'Worker'


def test_schema_create_user():
    schema = load_schema('create_user_schema.json')

    response = requests.post(
        url='https://reqres.in/api/users',
        data={'name': 'TestUser',
                'job': 'Worker'}
    )
    print(response.json())
    validate(instance=response.json(), schema=schema)


def test_delete_user():
    response = requests.delete(url='https://reqres.in/api/users/693')

    assert response.status_code == 204


def test_user_registration():
    response = requests.post(
        url='https://reqres.in/api/register',
        data={
            "email": "eve.holt@reqres.in",
            "password": "pistol"
        }
    )

    assert response.status_code == 200


def test_user_registration_failed():
    response = requests.post(
        url='https://reqres.in/api/register',
        data={
            "email": "eve.holt@reqres.in",
            }
    )

    assert response.status_code == 400
    assert response.json()['error'] == 'Missing password'


def test_user_update():
    response = requests.patch(
        url='https://reqres.in/api/users/2',
        data={
            'name': 'Test',
            'job': 'worker'
        }
    )

    assert response.status_code == 200
    assert response.json()['name'] == 'Test'
    assert response.json()['job'] == 'worker'
