def test_phase1_lifecycle_parity_over_api(client, auth_header):
    create = client.post('/tasks', headers=auth_header, json={'title': 'phase1-like'})
    assert create.status_code == 201
    task_id = create.json()['id']

    update = client.patch(f'/tasks/{task_id}', headers=auth_header, json={'title': 'phase1-updated'})
    assert update.status_code == 200

    toggle = client.post(f'/tasks/{task_id}/toggle-complete', headers=auth_header)
    assert toggle.status_code == 200
    assert toggle.json()['is_completed'] is True

    delete = client.delete(f'/tasks/{task_id}', headers=auth_header)
    assert delete.status_code == 204

    missing = client.get(f'/tasks/{task_id}', headers=auth_header)
    assert missing.status_code == 404
