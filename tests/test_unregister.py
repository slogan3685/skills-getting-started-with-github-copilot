def test_unregister_registered_student_success(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"
    endpoint = f"/activities/{activity_name}/unregister"

    # Act
    response = client.post(endpoint, params={"email": existing_email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload == {"message": f"Unregistered {existing_email} from {activity_name}"}


def test_unregister_removes_student_from_participants(client):
    # Arrange
    activity_name = "Programming Class"
    existing_email = "emma@mergington.edu"
    unregister_endpoint = f"/activities/{activity_name}/unregister"

    # Act
    unregister_response = client.post(unregister_endpoint, params={"email": existing_email})
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]

    # Assert
    assert unregister_response.status_code == 200
    assert existing_email not in participants


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "someone@mergington.edu"
    endpoint = f"/activities/{activity_name}/unregister"

    # Act
    response = client.post(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload == {"detail": "Activity not found"}


def test_unregister_non_registered_student_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    non_registered_email = "not.registered@mergington.edu"
    endpoint = f"/activities/{activity_name}/unregister"

    # Act
    response = client.post(endpoint, params={"email": non_registered_email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload == {"detail": "Student is not registered for this activity"}


def test_unregister_missing_email_returns_422(client):
    # Arrange
    activity_name = "Chess Club"
    endpoint = f"/activities/{activity_name}/unregister"

    # Act
    response = client.post(endpoint)

    # Assert
    assert response.status_code == 422
