import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


@pytest.fixture
def reset_activities():
    """Arrange: restore the in-memory activity data before each test."""
    original_activities = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_activities)


def test_unregister_participant_removes_email(reset_activities):
    # Arrange
    activity = "Chess Club"
    participant = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants/{participant}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {participant} from {activity}"
    assert participant not in client.get("/activities").json()[activity]["participants"]


def test_unregister_participant_returns_404_when_missing(reset_activities):
    # Arrange
    activity = "Chess Club"
    missing_participant = "not-found@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/participants/{missing_participant}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
