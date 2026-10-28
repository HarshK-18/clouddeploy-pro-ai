
import re
from pathlib import Path

import joblib

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "failure_classifier.joblib"
MAX_MESSAGE_LENGTH = 2000

TROUBLESHOOTING_ADVICE = {
    "test_failure": (
        "Review the failing test, assertion, and expected versus actual output."
    ),
    "dependency_issue": (
        "Check requirements.txt, installed packages, and dependency versions."
    ),
    "config_issue": (
        "Verify required environment variables and configuration values."
    ),
    "aws_permission": (
        "Review the IAM role, policy permissions, trust policy, and PassRole scope."
    ),
    "deployment_error": (
        "Inspect the SAM and CloudFormation deployment logs and failed resources."
    ),
    "app_runtime": (
        "Inspect the application exception and sanitized runtime logs."
    ),
}


def sanitize_error_message(message: str) -> str:
    """Remove common sensitive values and limit the input length."""
    if not isinstance(message, str) or not message.strip():
        raise ValueError("Error message must be a non-empty string.")

    sanitized = message[:MAX_MESSAGE_LENGTH]

    # Redact common key=value secrets and bearer tokens.
    sanitized = re.sub(
        r"(?i)\b(password|passwd|token|secret|api[_-]?key)"
        r"\s*[:=]\s*['\"]?[^,\s;'\"\"]+",
        r"\1=[REDACTED]",
        sanitized,
    )
    sanitized = re.sub(
        r"(?i)\bBearer\s+\S+",
        "Bearer [REDACTED]",
        sanitized,
    )

    return sanitized


def analyze_failure(message: str) -> dict[str, str]:
    """Classify a sanitized error; always provide a safe fallback."""
    try:
        sanitized = sanitize_error_message(message)
        model = joblib.load(MODEL_PATH)
        category = str(model.predict([sanitized])[0])

        if category not in TROUBLESHOOTING_ADVICE:
            raise ValueError("Model returned an unsupported category.")

        return {
            "category": category,
            "advice": TROUBLESHOOTING_ADVICE[category],
        }

    except Exception:
        return {
            "category": "unknown",
            "advice": (
                "Automated diagnosis is unavailable. "
                "Review the workflow logs and troubleshoot manually."
            ),
        }


if __name__ == "__main__":
    example = (
        "AccessDenied when calling Lambda UpdateFunctionCode"
    )
    result = analyze_failure(example)
    print(f"Category: {result['category']}")
    print(f"Advice: {result['advice']}")
