
import pytest

from src.failure_classifier import (
    build_classifier,
    load_dataset,
    predict_failure,
)


def test_dataset_contains_all_six_categories() -> None:
    """Verify that the dataset has messages from all six categories."""
    messages, categories = load_dataset()

    assert len(messages) == len(categories)
    assert len(messages) >= 60
    assert len(set(categories)) == 6


def test_dataset_messages_are_not_empty() -> None:
    """Verify that every loaded message contains text."""
    messages, _ = load_dataset()

    assert all(message.strip() for message in messages)


def test_classifier_predicts_aws_permission() -> None:
    """Verify that the model recognizes an AWS permission error."""
    messages, categories = load_dataset()
    model = build_classifier()
    model.fit(messages, categories)

    prediction = predict_failure(
        model,
        "AccessDenied when calling Lambda UpdateFunctionCode",
    )

    assert prediction == "aws_permission"


def test_classifier_predicts_dependency_issue() -> None:
    """Verify that the model recognizes a missing dependency."""
    messages, categories = load_dataset()
    model = build_classifier()
    model.fit(messages, categories)

    prediction = predict_failure(
        model,
        "ModuleNotFoundError: No module named boto3",
    )

    assert prediction == "dependency_issue"


def test_classifier_predicts_deployment_error() -> None:
    """Verify that the model recognizes a deployment failure."""
    messages, categories = load_dataset()
    model = build_classifier()
    model.fit(messages, categories)

    prediction = predict_failure(
        model,
        "CloudFormation stack deployment failed",
    )

    assert prediction == "deployment_error"


def test_empty_error_message_is_rejected() -> None:
    """Verify that empty input raises a validation error."""
    messages, categories = load_dataset()
    model = build_classifier()
    model.fit(messages, categories)

    with pytest.raises(ValueError, match="cannot be empty"):
        predict_failure(model, "   ")
