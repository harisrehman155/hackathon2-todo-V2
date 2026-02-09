def test_unauthenticated_requests_return_401(client):
    assert client.get('/tasks').status_code == 401
    assert client.post('/tasks', json={'title': 'x'}).status_code == 401
    assert client.get('/tasks/1').status_code == 401
    assert client.patch('/tasks/1', json={'title': 'y'}).status_code == 401
    assert client.delete('/tasks/1').status_code == 401
    assert client.post('/tasks/1/toggle-complete').status_code == 401


def test_invalid_token_returns_401(client):
    bad = {'Authorization': 'Bearer invalid.token.value'}
    assert client.get('/tasks', headers=bad).status_code == 401
