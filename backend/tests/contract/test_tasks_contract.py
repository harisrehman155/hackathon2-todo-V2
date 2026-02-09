def test_tasks_routes_exist_and_require_auth(client):
    endpoints = [
        ("get", "/tasks"),
        ("post", "/tasks"),
        ("get", "/tasks/1"),
        ("patch", "/tasks/1"),
        ("delete", "/tasks/1"),
        ("post", "/tasks/1/toggle-complete"),
    ]

    for method, path in endpoints:
        response = getattr(client, method)(path)
        assert response.status_code == 401


def test_create_and_fetch_task_contract(client, auth_header):
    created = client.post("/tasks", headers=auth_header, json={"title": "Contract Task"})
    assert created.status_code == 201
    body = created.json()
    assert set(["id", "title", "description", "is_completed", "created_at", "updated_at"]).issubset(body.keys())

    fetched = client.get(f"/tasks/{body['id']}", headers=auth_header)
    assert fetched.status_code == 200
    assert fetched.json()["title"] == "Contract Task"
