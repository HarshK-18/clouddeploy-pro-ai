
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "data" / "failure_samples.csv"
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODEL_DIR / "failure_classifier.joblib"


def load_dataset() -> tuple[list[str], list[str]]:
    """Load and validate labelled failure messages."""
    dataset = pd.read_csv(DATASET_PATH)

    required_columns = {"error_message", "category"}
    if not required_columns.issubset(dataset.columns):
        raise ValueError(
            "Dataset must contain error_message and category columns."
        )

    dataset = dataset.dropna(subset=["error_message", "category"])

    messages = dataset["error_message"].astype(str).tolist()
    categories = dataset["category"].astype(str).tolist()

    if len(messages) < 12:
        raise ValueError("Dataset is too small to train the classifier.")

    if len(set(categories)) < 2:
        raise ValueError("Dataset must contain at least two categories.")

    return messages, categories

#build_classifier() creates the complete ML pipeline.
def build_classifier() -> Pipeline:
    """Create the TF-IDF and Naive Bayes pipeline."""
    return Pipeline(
        [
            ("tfidf", TfidfVectorizer()),
            ("classifier", MultinomialNB()),
        ]
    )


def train_classifier() -> Pipeline:
    """Train and evaluate the failure classifier."""
    messages, categories = load_dataset()

    X_train, X_test, y_train, y_test = train_test_split(
        messages,
        categories,
        test_size=0.40,
        random_state=42,
        stratify=categories,
    )

    model = build_classifier()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("\nClassification report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0,
        )
    )

    return model

#save_model() saves the trained pipeline to your models folder.
def save_model(model: Pipeline) -> None:
    """Save the trained pipeline to disk."""
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"\nModel saved successfully: {MODEL_PATH}")

#load_model() loads the saved pipeline back into memory.
def load_model() -> Pipeline:
    """Load the saved pipeline from disk."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Saved model not found: {MODEL_PATH}"
        )

    model = joblib.load(MODEL_PATH)
    print("Saved model loaded successfully.")
    return model

#predict_failure() validates the input and predicts its category.
def predict_failure(model: Pipeline, message: str) -> str:
    """Predict the category of a failure message."""
    if not message.strip():
        raise ValueError("Error message cannot be empty.")

    return str(model.predict([message])[0])

#main() verifies the complete train → save → load → predict workflow.
def main() -> None:
    model = train_classifier()
    save_model(model)

    loaded_model = load_model()

    examples = [
        "AccessDenied when calling Lambda UpdateFunctionCode",
        "ModuleNotFoundError: No module named boto3",
        "CloudFormation stack deployment failed",
    ]

    print("\nPredictions using the loaded model:")

    for message in examples:
        category = predict_failure(loaded_model, message)
        print(f"Error: {message}")
        print(f"Predicted category: {category}\n")


if __name__ == "__main__":
    main()
