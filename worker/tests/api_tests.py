from http import HTTPStatus
from unittest.mock import patch


@patch('worker.main.get_task')
def test_get_task_api(mocked, client, create_task):
    URL = '/'

    response = client.get(URL)
    assert response.status_code == HTTPStatus.OK
    assert 'message' in response.json()

    response = client.get(URL, params={'task_id': 'anything'})
    assert response.status_code == HTTPStatus.NOT_FOUND

    mocked.return_value = None
    task = create_task()
    response = client.get(URL, params={'task_id': str(task.id)})
    assert response.status_code == HTTPStatus.NOT_FOUND

    mocked.return_value = task
    response = client.get(URL, params={'task_id': str(task.id)})
    assert response.status_code == HTTPStatus.OK
    assert response.json()['id'] == str(task.id)


@patch('worker.main.add_task')
def test_add_task_api(mocked, client, create_task):
    URL = '/'

    response = client.post(URL)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    mocked.return_value = 1
    response = client.post(URL, params={
        'task_title': 'word', 'exp_sec': 60
    })
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'task_id': 1}
