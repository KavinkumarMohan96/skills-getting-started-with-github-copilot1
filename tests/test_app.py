import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# GET /activities
def test_get_activities():
    # Arrange: None needed
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data, dict)

# POST /activities/{activity_name}/signup (success)
def test_signup_for_activity_success():
    # Arrange: Ensure not registered
    email = "pytest_signup@mergington.edu"
    client.post(f"/activities/Chess Club/unregister?email={email}")
    # Act
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

# POST /activities/{activity_name}/signup (already signed up)
def test_signup_for_activity_already_signed_up():
    # Arrange: Register first
    email = "pytest_duplicate@mergington.edu"
    client.post(f"/activities/Chess Club/unregister?email={email}")
    client.post(f"/activities/Chess Club/signup?email={email}")
    # Act
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

# POST /activities/{activity_name}/signup (activity not found)
def test_signup_for_activity_not_found():
    # Arrange: None needed
    # Act
    response = client.post("/activities/Nonexistent/signup?email=pytest@mergington.edu")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

# POST /activities/{activity_name}/unregister (success)
def test_unregister_from_activity_success():
    # Arrange: Register first
    email = "pytest_unregister@mergington.edu"
    client.post(f"/activities/Chess Club/signup?email={email}")
    # Act
    response = client.post(f"/activities/Chess Club/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]

# POST /activities/{activity_name}/unregister (not registered)
def test_unregister_from_activity_not_registered():
    # Arrange: Ensure not registered
    email = "pytest_notregistered@mergington.edu"
    client.post(f"/activities/Chess Club/unregister?email={email}")
    # Act
    response = client.post(f"/activities/Chess Club/unregister?email={email}")
    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]

# POST /activities/{activity_name}/unregister (activity not found)
def test_unregister_from_activity_not_found():
    # Arrange: None needed
    # Act
    response = client.post("/activities/Nonexistent/unregister?email=pytest@mergington.edu")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
