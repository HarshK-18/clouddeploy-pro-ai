
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

## Local Development

Setup instructions and test commands will be documented as the
application and development dependencies are implemented.
