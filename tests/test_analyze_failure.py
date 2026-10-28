
from unittest.mock import patch

import pytest

from ai.analyze_failure import (
    analyze_failure,
    sanitize_error_message,
)


def test_known_aws_permission_error() -> None:
    """Verify that a known AWS permission message is classified correctly."""
    from unittest.mock import Mock, patch

    mock_model = Mock()
    mock_model.predict.return_value = ["aws_permission"]

    with patch(
        "ai.analyze_failure.joblib.load",
        return_value=mock_model,
    ):
        result = analyze_failure(
            "AccessDenied when calling Lambda UpdateFunctionCode"
        )

    assert result["category"] == "aws_permission"
    assert "IAM" in result["advice"]



def test_missing_model_returns_generic_fallback() -> None:
    with patch(
        "ai.analyze_failure.MODEL_PATH"
    ) as model_path:
        model_path.exists.return_value = False

        with patch(
            "ai.analyze_failure.joblib.load",
            side_effect=FileNotFoundError,
        ):
            result = analyze_failure("Deployment failed")

    assert result["category"] == "unknown"
    assert "unavailable" in result["advice"]


@pytest.mark.parametrize("message", ["", "   ", None, 123])
def test_invalid_input_returns_unknown(message: object) -> None:
    result = analyze_failure(message)

    assert result["category"] == "unknown"
    assert result["advice"]


def test_sanitizer_redacts_common_secret_patterns() -> None:
    result = sanitize_error_message(
        "Request failed token=abc123 Bearer xyz987"
    )

    assert "abc123" not in result
    assert "xyz987" not in result
    assert "[REDACTED]" in result


def test_unexpected_model_error_returns_fallback() -> None:
    with patch(
        "ai.analyze_failure.joblib.load",
        side_effect=RuntimeError("model unavailable"),
    ):
        result = analyze_failure("Application crashed")

    assert result["category"] == "unknown"
