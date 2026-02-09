def test_list_items_empty(client):
    """Test listing items when empty"""
    response = client.get("/api/v1/items")
    assert response.status_code == 200
    assert response.json() == []


def test_create_item_requires_auth(client):
    """Test creating item without authentication"""
    response = client.post(
        "/api/v1/items",
        json={"name": "Test Item", "price": 10.99, "description": "Test"}
    )
    assert response.status_code == 401


def test_create_item(client):
    """Test creating an item with authentication"""
    # Register and login
    client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "username": "testuser", "password": "testpass123"}
    )
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpass123"}
    )
    token = login_response.json()["access_token"]

    # Create item
    response = client.post(
        "/api/v1/items",
        json={"name": "Test Item", "price": 10.99, "description": "Test"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 10.99
    assert "id" in data


def test_get_item(client):
    """Test getting a specific item"""
    # Setup: Create authenticated user and item
    client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "username": "testuser", "password": "testpass123"}
    )
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpass123"}
    )
    token = login_response.json()["access_token"]

    create_response = client.post(
        "/api/v1/items",
        json={"name": "Test Item", "price": 10.99},
        headers={"Authorization": f"Bearer {token}"}
    )
    item_id = create_response.json()["id"]

    # Get item
    response = client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "Test Item"


def test_update_item(client):
    """Test updating an item"""
    # Setup
    client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "username": "testuser", "password": "testpass123"}
    )
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpass123"}
    )
    token = login_response.json()["access_token"]

    create_response = client.post(
        "/api/v1/items",
        json={"name": "Test Item", "price": 10.99},
        headers={"Authorization": f"Bearer {token}"}
    )
    item_id = create_response.json()["id"]

    # Update item
    response = client.put(
        f"/api/v1/items/{item_id}",
        json={"name": "Updated Item", "price": 15.99},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Item"
    assert data["price"] == 15.99


def test_delete_item(client):
    """Test deleting an item"""
    # Setup
    client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "username": "testuser", "password": "testpass123"}
    )
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpass123"}
    )
    token = login_response.json()["access_token"]

    create_response = client.post(
        "/api/v1/items",
        json={"name": "Test Item", "price": 10.99},
        headers={"Authorization": f"Bearer {token}"}
    )
    item_id = create_response.json()["id"]

    # Delete item
    response = client.delete(
        f"/api/v1/items/{item_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204

    # Verify deleted
    response = client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 404
