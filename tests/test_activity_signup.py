from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email():
    activity = "Chess Club"
    participant = "michael@mergington.edu"

    initial = client.get("/activities").json()[activity]["participants"]
    try:
        response = client.delete(f"/activities/{activity}/participants/{participant}")
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {participant} from {activity}"
        assert participant not in client.get("/activities").json()[activity]["participants"]
    finally:
        if participant not in client.get("/activities").json()[activity]["participants"]:
            client.post(f"/activities/{activity}/signup?email={participant}")


def test_unregister_participant_returns_404_when_missing():
    response = client.delete("/activities/Chess Club/participants/not-found@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
