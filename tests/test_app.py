#Tests for the CloudDeploy Pro AI application handler
#Run with -  python -m pytest -v

"""Automated tests for the CloudDeploy Pro AI application handler."""

import json

from src.app import handler


def response_body(response: dict) -> dict:
    """Decode the JSON response body for easier assertions."""
    return json.loads(response["body"])


def test_health_request_returns_200(monkeypatch):
# monkeypatch restores environment changes after each test.
# Assertions fail the test when actual values differ from expectations.
    monkeypatch.delenv("APP_ENV", raising=False)

    response = handler({"action": "health"}, None)

#Assertions: assert response["statusCode"] == 200 checks a condition. 
#If it is false, pytest marks that test as failed.
    assert response["statusCode"] == 200
    assert response_body(response)["status"] == "healthy"
    assert response_body(response)["environment"] == "development"


def test_status_request_returns_200(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")

    response = handler({"action": "status"}, None)

    assert response["statusCode"] == 200
    assert response_body(response)["action"] == "status"
    assert response_body(response)["environment"] == "test"


def test_non_dictionary_event_returns_400():
    response = handler(None, None)

    assert response["statusCode"] == 400
    assert response_body(response)["message"] == (
        "Request must be a JSON object."
    )


def test_unsupported_action_returns_400():
    response = handler({"action": "deploy-everything"}, None)

    assert response["statusCode"] == 400
    assert response_body(response)["status"] == "error"


def test_invalid_environment_returns_500(monkeypatch):
    monkeypatch.setenv("APP_ENV", "invalid-environment")

    response = handler({"action": "health"}, None)

    assert response["statusCode"] == 500
    assert response_body(response)["message"] == (
        "Application configuration is invalid."
    )


def test_production_environment_is_accepted(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")

    response = handler({"action": "health"}, None)

    assert response["statusCode"] == 200
    assert response_body(response)["environment"] == "production"
