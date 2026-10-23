
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

Automated pytest coverage will be added on Day 3.

