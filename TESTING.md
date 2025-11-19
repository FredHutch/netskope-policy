# Testing Framework and Quality Assurance

## Overview

This file describes the required and recommended testing practices for the FredHutch/netskope-policy repository, ensuring robust quality assurance and stable healthcare compliance.

## Requirements
- All new features must include unit tests with coverage >90%.
- Policy-related logic requires integration tests using sandboxed Netskope tenant or mocks.
- Run all tests locally prior to submission; automated CI/CD will enforce them post-push.

## Technologies
- **pytest** – for test execution and discovery.
- **flake8, pylint** – for lint and code style enforcement.
- **pytest-cov** – for measuring test coverage.
- **mypy** – for static type checking.

## Test Organization
- Place unit tests in `tests/unit/`, integration tests in `tests/integration/`, and policy validation scripts in `tests/policies/`.
- Name test files and methods with clear intent (e.g., test_client_auth, test_policy_deploy_success).

## Integration Testing
- Use mock responses for Netskope API.
- Validate complex policy deployments against actual/sandbox endpoints.

## CI/CD Integration
- Add workflows in `.github/workflows/` to automate tests on push/PR.
- Collect and publish test coverage reports for every merge.

## Policy Testing
- Add dry-run (monitor-only) capability before full deployment.
- Integrate rollback support when tests or deployments fail.

For any questions, consult CONTRIBUTING.md or contact the maintainers.
