
"""CloudDeploy Pro AI application handler."""

import json
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#Defines which application environment values are accepted.
ALLOWED_ENVIRONMENTS = {"development", "test", "production"}

#Produces a consistent response with a status code, headers, and JSON body.
def json_response(status_code: int, payload: dict[str, Any]) -> dict[str, Any]:
    """Build a consistent API Gateway-compatible response."""
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(payload),
    }

# Lambda entry point: event holds the request; context holds runtime metadata.
def handler(event: Any, context: Any) -> dict[str, Any]:
    """Handle a health/status request locally or through AWS Lambda."""
#Input validation - Rejects non-dictionary requests and unsupported actions.
    if not isinstance(event, dict):
        logger.warning(
            json.dumps({"event": "request_rejected", "reason": "invalid_event"})
        )
        return json_response(400, { 
            "status": "error",
            "message": "Request must be a JSON object.",
        })
    
    #Read the environment name; default to development.
    environment = os.getenv("APP_ENV", "development").strip().lower()     

    if environment not in ALLOWED_ENVIRONMENTS:
        logger.error(
            json.dumps({
                "event": "configuration_error",
                "reason": "invalid_app_environment",
            })
        )
        return json_response(500, {
            "status": "error",
            "message": "Application configuration is invalid.",
        })

    action = event.get("action", "health")

#Input validation - Rejects non-dictionary requests and unsupported actions.
    if not isinstance(action, str) or action not in {"health", "status"}:
        logger.warning(
            json.dumps({"event": "request_rejected", "reason": "invalid_action"})
        )
        return json_response(400, {
            "status": "error",
            "message": "Action must be 'health' or 'status'.",
        })

    logger.info(
        json.dumps({
            "event": "request_processed",
            "action": action,
            "status": "success",
            "environment": environment,
        })
    )
## Log JSON events without exposing request data or secrets.
    return json_response(200, {
        "status": "healthy",
        "action": action,
        "environment": environment,
    })

#Allows you to run a local demonstration directly, without invoking AWS.
if __name__ == "__main__":
    # Simple local demonstration without AWS.
    result = handler({"action": "health"}, None)
    print(json.dumps(result, indent=2))
