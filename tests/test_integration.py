from urllib.parse import quote


def test_signup_then_unregister_lifecycle(client):
    # Arrange
    activity_name = "Science Club"
    email = "lifecycle.student@mergington.edu"
    signup_endpoint = f"/activities/{quote(activity_name)}/signup"
    unregister_endpoint = f"/activities/{quote(activity_name)}/unregister"

    # Act
    signup_response = client.post(signup_endpoint, params={"email": email})
    unregister_response = client.post(unregister_endpoint, params={"email": email})
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert email not in participants


def test_unregister_twice_returns_404_on_second_attempt(client):
    # Arrange
    activity_name = "Drama Club"
    email = "amelia@mergington.edu"
    endpoint = f"/activities/{quote(activity_name)}/unregister"

    # Act
    first_response = client.post(endpoint, params={"email": email})
    second_response = client.post(endpoint, params={"email": email})

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 404
    assert second_response.json() == {"detail": "Student is not registered for this activity"}
