import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities


@pytest.fixture(autouse=True)
def reset_activity_state():
    original_state = {
        name: list(details["participants"])
        for name, details in activities.items()
    }
    yield
    for name, details in activities.items():
        details["participants"] = original_state[name]


client = TestClient(app)


def test_signup_adds_participant_to_activity():
    response = client.post(
        "/activities/Chess Club/signup?email=newstudent@mergington.edu"
    )

    assert response.status_code == 200
    assert "newstudent@mergington.edu" in response.json()["message"]

    activity = client.get("/activities").json()["Chess Club"]
    assert "newstudent@mergington.edu" in activity["participants"]


def test_unregister_removes_participant_from_activity():
    client.post("/activities/Chess Club/signup?email=remove_me@mergington.edu")

    response = client.delete(
        "/activities/Chess Club/participants/remove_me@mergington.edu"
    )

    assert response.status_code == 200
    activity = client.get("/activities").json()["Chess Club"]
    assert "remove_me@mergington.edu" not in activity["participants"]
