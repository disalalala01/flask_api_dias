
def test_list(user, video, client, user_headers):
    res = client.get('/tutorials', headers=user_headers)

    assert res.status_code == 200
    assert len(res.get_json()) == 1

    assert res.get_json()[0] == {
        'name': 'Video 1',
        'description': 'Description',
        'user_id': user.id,
        'id': video.id
    }


def test_new_video(user, client, user_headers):
    res = client.post('/tutorials', json={
        'name': 'Video 1',
        'description': 'Description'
    }, headers=user_headers)
    assert res.status_code == 200
    assert res.get_json()['name'] == 'Video 1'
    assert res.get_json()['description'] == 'Description'
    assert res.get_json()['user_id'] == user.id


def test_edit_video(video, client, user_headers):
    res = client.put(f'/tutorials/{video.id}', json={
        'name': 'Video upd',
        'description': 'Description'
    }, headers=user_headers)
    assert res.status_code == 200
    assert res.get_json()['name'] == 'Video upd'
    assert res.get_json()['description'] == 'Description'


def test_delete_video(video, client, user_headers):
    res = client.delete(f'/tutorials/{video.id}', headers=user_headers)
    assert res.status_code == 204