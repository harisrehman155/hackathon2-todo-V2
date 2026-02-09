def test_task_lifecycle_create_update_toggle_delete(client, auth_header):
    create_response = client.post(
        "/tasks",
        headers=auth_header,
        json={"title": "Initial task", "description": "phase2"},
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    list_response = client.get("/tasks", headers=auth_header)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_response = client.patch(
        f"/tasks/{task_id}",
        headers=auth_header,
        json={"title": "Updated task"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated task"

    toggle_response = client.post(f"/tasks/{task_id}/toggle-complete", headers=auth_header)
    assert toggle_response.status_code == 200
    assert toggle_response.json()["is_completed"] is True

    delete_response = client.delete(f"/tasks/{task_id}", headers=auth_header)
    assert delete_response.status_code == 204

    missing_response = client.get(f"/tasks/{task_id}", headers=auth_header)
    assert missing_response.status_code == 404


def test_task_persists_between_requests_same_session(client, auth_header):
    create_response = client.post("/tasks", headers=auth_header, json={"title": "Persist me"})
    assert create_response.status_code == 201

    first = client.get("/tasks", headers=auth_header)
    second = client.get("/tasks", headers=auth_header)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
