import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities


@pytest.fixture(autouse=True)
def reset_activity_state():
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
    yield
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    signup_response = client.post(
        "/activities/Chess Club/signup?email=test@mergington.edu"
    )
    assert signup_response.status_code == 200

    delete_response = client.delete(
        "/activities/Chess Club/participants/test@mergington.edu"
    )
    assert delete_response.status_code == 200

    activity = client.get("/activities").json()["Chess Club"]
    assert "test@mergington.edu" not in activity["participants"]
