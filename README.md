
# CloudDeploy Pro AI

AI-assisted AWS deployment automation for Cloud and DevOps engineering.

## Project Goal

Build a small, explainable system that validates application changes,
automates deployment through GitHub Actions, and helps categorize
failures using a lightweight machine-learning model.

## Planned Technology Stack

- Python, pytest, Ruff, and Boto3
- Git, GitHub, and GitHub Actions
- Docker and Linux/Bash
- AWS Lambda, IAM, GitHub OIDC, AWS SAM, and CloudFormation
- Amazon CloudWatch and Amazon SNS
- scikit-learn with TF-IDF and Multinomial Naive Bayes

## Mandatory Safety Rules

1. Tests, linting, configuration checks, and required security checks
   must pass before deployment.
2. AI-generated failure categories are advisory only.
3. AI must never bypass validation, authorization, or security controls.
4. Never commit credentials, tokens, or private configuration.
5. Review AWS pricing and account eligibility before creating resources.

## Cost Objective

Target cost: ₹0.

This is a goal, not a guarantee. Actual charges depend on account
eligibility, credits, region, service usage, and current pricing.

AWS resources will be reviewed before deployment and cleaned up
after testing when no longer needed.

## Project Status

Day 1: Repository and project foundation in progress.

Implementation, tests, architecture diagrams, deployment workflows,
and demonstration evidence will be added and verified incrementally.


## Application Handler (Day 2)

The application is implemented in `src/app.py` as a Python handler
compatible with the AWS Lambda event-handler interface.

### Supported actions

| Action | Expected behavior |
|---|---|
| `health` | Returns HTTP-style status 200 and a healthy response |
| `status` | Returns HTTP-style status 200 and a healthy response |
| Unsupported action | Returns HTTP-style status 400 |
| Non-dictionary event | Returns HTTP-style status 400 |
| Invalid `APP_ENV` configuration | Returns HTTP-style status 500 |

### Configuration

The `APP_ENV` environment variable controls the application environment.
Supported values are `development`, `test`, and `production`.
If the variable is not set, the application defaults to `development`.

### Logging and error handling

The handler emits JSON-formatted log messages for successful requests,
rejected requests, and invalid configuration. It does not log the
entire incoming event or return internal configuration details.

### Local execution

Run the application from the repository root:

```powershell
python src/app.py
```

For a manual interactive test:

```python
from src.app import handler

print(handler({"action": "health"}, None))
```

The handler returns a response dictionary containing `statusCode`,
`headers`, and a JSON-encoded `body`.

### Day 2 verification

Manually verified:
- Successful health and status requests
- Rejection of a non-dictionary event
- Rejection of an unsupported action
- Rejection of invalid application configuration


## Local Development and Testing (Day 3)

### Python environment

Create a virtual environment:

```powershell
python -m venv .venv
```

Install development dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

### Automated tests

Run pytest:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Run Ruff:

```powershell
.\.venv\Scripts\ruff.exe check src tests
```

### Docker

Build the application image:

```powershell
docker build -t clouddeploy-pro-ai:day3 .
```

Run the container:

```powershell
docker run --rm clouddeploy-pro-ai:day3
```

Verify the non-root user:

```powershell
docker run --rm clouddeploy-pro-ai:day3 whoami
```

Expected output: `appuser`.

The container runs locally and does not deploy application resources
to AWS.

## Day 5 — Validation and Security Gates

Implemented automated validation checks in GitHub Actions to improve code quality and security.

**Checks implemented:**
- **Gitleaks:** Scans for potential exposed secrets.
- **Ruff:** Checks Python code quality.
- **pip-audit:** Scans application and development dependencies for known vulnerabilities.
- **Configuration validation:** Validates `APP_ENV` values using `validation/check_config.py`.
- **pytest:** Runs six unit tests.

**Release Policy:**
- All mandatory checks must pass before deployment.
- Failed checks block subsequent steps in the same job.
- `.gitignore` helps prevent accidental commits of sensitive files.
- AI-assisted diagnostics cannot override security or validation failures.

**Result:** Local linting, configuration validation, dependency audits, and all six tests passed. The GitHub Actions workflow was updated with the new validation and security checks.

## Day 6 — AWS Setup and Security Review

**Completed:**
- Installed and verified AWS CLI v2.38.5.
- Installed and verified AWS SAM CLI 1.170.0.
- Verified AWS authentication using `aws sts get-caller-identity`.
- Confirmed the configured AWS region: `ap-southeast-2` (Sydney).
- Inspected IAM role policies, trust policy, and permissions boundary.
- Prepared the planned AWS resource inventory for the project.

**Security Findings:**
- The active `AccountFullAccessRole` has the AWS-managed `AdministratorAccess` policy attached.
- No inline role policies or permissions boundary were found during inspection.
- A dedicated least-privilege deployment role will be planned before deploying project resources.
- AWS Management Console will be preferred for IAM and other tasks that can be safely performed through the web interface.

**Cost and Safety Policy:**
- No project AWS resources were created during this review.
- Review regional pricing and Free Tier eligibility before creating resources.
- Avoid unnecessary EC2, NAT Gateway, EKS, and always-on infrastructure.
- Document resource ownership, expected cost, and cleanup steps before deployment.

**Next:** Design and review the least-privilege AWS deployment architecture.

## Day 7 — GitHub Actions OIDC Integration

**Completed:**
- Created the GitHub OIDC identity provider in AWS IAM.
- Created `CloudDeployProAIGitHubActionsRole`.
- Restricted role assumption to the repository's `main` branch using GitHub's immutable subject claim.
- Configured GitHub Actions to obtain temporary AWS credentials through OIDC.
- Verified AWS identity with `sts:GetCallerIdentity`.
- Confirmed both CI validation and OIDC authentication jobs pass.

**Security:** No permanent AWS access keys stored in GitHub. The IAM role currently has only identity-verification permissions.

**Next:** Prepare the AWS SAM deployment foundation and least-privilege deployment permissions.

## Day 8 — AWS SAM Deployment Foundation

**Completed:**
- Created `template.yaml` using AWS SAM and AWS CloudFormation.
- Defined the Lambda function `CloudDeployProAIHandler`.
- Configured the Python handler as `src.app.handler`.
- Defined a dedicated Lambda execution role with CloudWatch Logs permissions.
- Configured a CloudWatch log group with seven-day retention.
- Set the application environment variable `APP_ENV=development`.
- Validated the SAM template using `sam validate --lint`.
- Built the application using `sam build`.
- Confirmed all six automated tests pass.

**Validation results:** SAM validation successful, SAM build successful, and 6/6 tests passed.

**Security and cost:** No AWS deployment performed during this step. Deployment and AWS resource costs have not yet been incurred by these local validation commands.

**Next:** Review deployment permissions, validate the deployment plan, and assess AWS costs before creating resources.

## Day 9 - AWS Deployment by Github using OIDC SAM , CloufFormation , Lambda

Configured GitHub Actions CI with Ruff, pytest, dependency audits, configuration validation, and Gitleaks.
Configured passwordless AWS authentication using GitHub OIDC.
Created a dedicated CloudFormation execution role and Lambda execution role.
Configured a private S3 bucket for SAM deployment artifacts.
Deployed the application through AWS SAM and CloudFormation.
Restricted deployment to manually triggered workflows on main.

## Day 10 — Amazon SNS Email Notifications

Objective: Configure email notifications using Amazon Simple Notification Service (SNS).

Created the Standard SNS topic CloudDeployProAI-Notifications in ap-southeast-2.

Created and confirmed an email subscription.

Published a test notification and verified email delivery.

Established the notification foundation for future CI/CD alerts.

Key concepts: SNS topics, email subscriptions, subscription confirmation, message publishing, and notification delivery.

### Day 11 — Automated CI/CD Failure Notifications

**Objective:** Integrate Amazon SNS email notifications with GitHub Actions.

**Implemented:**
- Added `sns:Publish` permission for the existing SNS topic to `CloudDeployProAIGitHubActionsRole`.
- Added a `notify_failure` job to `ci.yml` to detect failed pipeline jobs on `main`.
- Configured OIDC authentication for the notification job.
- Included repository, branch, commit, job results, and workflow run link in alert messages.
- Created a separate manual test workflow to simulate a failure and verify SNS email delivery.

**Validation:** Normal CI workflow passed; simulated failure notification was successfully published and received by email.

**Status:** Core implementation completed. Production failure-trigger behavior remains to be verified.

## Day 12 — AI-Powered Failure Classification

### Overview
Implemented a machine-learning classifier to categorize deployment and application failures. The classifier uses TF-IDF for text feature extraction and Multinomial Naive Bayes for predicting failure categories.

### Features Implemented
- Created a synthetic labelled dataset with 100 failure examples.
- Implemented text classification using `TfidfVectorizer` and `MultinomialNB`.
- Used a scikit-learn `Pipeline` to combine feature extraction and classification while preventing training/test data leakage.
- Split the dataset into training and testing sets using stratified sampling.
- Evaluated model performance using precision, recall, F1-score, and accuracy.
- Saved and loaded the trained pipeline using `joblib`.
- Implemented failure prediction for new error messages.
- Added input validation to reject empty error messages.
- Created automated pytest tests for dataset validation, predictions, and invalid input.
- Integrated ML dependencies into the project requirements and GitHub Actions CI workflow.

### Failure Categories
The classifier recognizes six categories:

1. `test_failure` — Unit test, integration test, and smoke test failures.
2. `dependency_issue` — Missing packages, import errors, and dependency conflicts.
3. `config_issue` — Missing environment variables and invalid configuration.
4. `aws_permission` — AWS IAM authorization and access-denied errors.
5. `deployment_error` — SAM and CloudFormation deployment failures.
6. `app_runtime` — Runtime exceptions and application execution failures.

### Technology Stack
- Python
- pandas
- scikit-learn
- TF-IDF Vectorization
- Multinomial Naive Bayes
- joblib
- pytest
- Ruff
- GitHub Actions

### Model Evaluation
- Dataset size: 100 synthetic labelled examples.
- Test split: 40% of the dataset.
- Observed accuracy: approximately 81% in the recorded evaluation.
- Evaluation metrics: precision, recall, F1-score, and accuracy.

**Note:** The evaluation uses a small synthetic dataset. These metrics are intended for learning and experimentation and do not establish production-level classification accuracy.

### Model Artifact
The trained pipeline is saved locally at:

`models/failure_classifier.joblib`

The generated model artifact is excluded from Git tracking. It can be regenerated by running the training script.

### How to Run
Train, evaluate, save, and reload the classifier:

```bash
python src/failure_classifier.py
```

Run classifier-specific tests:

```bash
python -m pytest tests/test_failure_classifier.py -v
```

Run the complete test suite:

```bash
python -m pytest -v
```

Run linting:

```bash
python -m ruff check .
```

### CI/CD Integration
Updated the GitHub Actions workflow to install both application and development dependencies before validation and testing.

The classifier provides **advisory failure categorization only**. It does not replace mandatory CI validation, security scanning, automated tests, or deployment approval gates.

### Day 12 Outcome
Implemented and tested an end-to-end machine-learning workflow for failure classification, including dataset preparation, model training, evaluation, serialization, prediction, and automated testing.
