# Contributing Guidelines

## Overview

Thank you for considering a contribution to the FredHutch/netskope-policy repository! This document outlines the best practices to help maintain code quality, security, and compliance.

## Code Standards
- Follow Python PEP 8 style guidelines.
- Use descriptive variable names, docstrings, and type hints.
- All new features and bug fixes require corresponding tests.
- Design for modularity, scalability, and healthcare compliance.

## Development Process
- Fork the repository and create feature branches based on the main branch.
- Submit pull requests to main or the appropriate development branch.
- Reference related issues in PR descriptions and commits.
- Ensure code passes CI/CD tests before requesting review.

## Security Practices
- Never commit API keys or credentials; use environment variables and secure vaults.
- Immediately report vulnerabilities via repository security contacts.
- When handling PHI, anonymize test data and use pattern validation.

## Testing Requirements
- Include unit tests for new modules/functions.
- Add integration tests for APIs and deployment workflows.
- Prefer pytest and flake8 for test and lint enforcement.
- Run tests locally before pushing PRs; CI will enforce on push.

## Documentation
- Update README, IMPROVEMENTS.md, and API_REFERENCE.md for public-facing changes.
- Add or update docstrings for all classes and functions.
- Create runbooks for major operational or deployment changes.

## Approval & Review
- Reviews required from core maintainers before merge.
- Major changes may require approval from security/compliance stakeholders.

## Contact
For questions, reach out via repository Issues or contact the maintainers listed in README.
