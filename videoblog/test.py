from . import client
from videoblog.models import Video


def test_get():
    res = client.get('/tutorials')
    assert res.status_code == 200
    assert len(res.get_json()) == len(Video.query.all())
    assert res.get_json()[0]['id'] == 1


def test_post():
    data = {
        'name': 'Test',
        'description': 'Pytest'
    }
    res = client.post('/tutorials', json=data)
    assert res.status_code == 200
    assert res.get_json()['name'] == data['name']


def test_put():
    res = client.put('/tutorials/5', json={'name': 'UPD'})
    assert res.status_code == 200
    assert Video.query.get(5).name == 'UPD'


def test_delete():
    res = client.delete('/tutorials/3')

    assert res.status_code == 204
    assert Video.query.get(1) is None


