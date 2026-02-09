def test_user_cannot_access_other_user_tasks(client, auth_header, other_auth_header):
    created = client.post('/tasks', headers=auth_header, json={'title': 'private'})
    assert created.status_code == 201
    task_id = created.json()['id']

    assert client.get(f'/tasks/{task_id}', headers=other_auth_header).status_code == 404
    assert client.patch(f'/tasks/{task_id}', headers=other_auth_header, json={'title': 'hacked'}).status_code == 404
    assert client.delete(f'/tasks/{task_id}', headers=other_auth_header).status_code == 404
    assert client.post(f'/tasks/{task_id}/toggle-complete', headers=other_auth_header).status_code == 404


def test_user_list_only_contains_owned_tasks(client, auth_header, other_auth_header):
    assert client.post('/tasks', headers=auth_header, json={'title': 'a1'}).status_code == 201
    assert client.post('/tasks', headers=other_auth_header, json={'title': 'b1'}).status_code == 201

    a_list = client.get('/tasks', headers=auth_header)
    b_list = client.get('/tasks', headers=other_auth_header)

    assert a_list.status_code == 200
    assert b_list.status_code == 200
    assert [t['title'] for t in a_list.json()] == ['a1']
    assert [t['title'] for t in b_list.json()] == ['b1']
