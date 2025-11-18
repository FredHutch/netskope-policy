#!/usr/bin/env python3
"""
Custom PHI Patterns Example
Demonstrates how to create custom PHI protection policies
with organization-specific patterns
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from netskope_sdk import NetskopeClient
from policies import HealthcarePolicy


def main():
    """Custom PHI patterns example"""

    # Initialize client
    client = NetskopeClient(
        tenant=os.getenv("NETSKOPE_TENANT"),
        api_token=os.getenv("NETSKOPE_API_TOKEN")
    )

    # Initialize healthcare policy manager
    healthcare = HealthcarePolicy(
        client=client,
        organization_name="Cancer Research Institute"
    )

    # Define custom PHI patterns specific to your organization
    custom_patterns = [
        {
            "name": "Custom Patient ID",
            "pattern_type": "regex",
            "pattern": r"\bPT-[0-9]{6}\b",
            "match_count": 1,
            "proximity": 50,
            "description": "Custom patient identifier format: PT-######"
        },
        {
            "name": "Research Study ID",
            "pattern_type": "regex",
            "pattern": r"\bSTUDY-[A-Z]{3}-\d{4}\b",
            "match_count": 1,
            "proximity": 50,
            "description": "Research study identifier: STUDY-XXX-####"
        },
        {
            "name": "Tissue Sample ID",
            "pattern_type": "regex",
            "pattern": r"\bTS-[0-9]{8}\b",
            "match_count": 1,
            "proximity": 50,
            "description": "Tissue sample identifier: TS-########"
        },
        {
            "name": "Genetic Test Result ID",
            "pattern_type": "regex",
            "pattern": r"\bGTR-[A-Z0-9]{10}\b",
            "match_count": 1,
            "proximity": 50,
            "description": "Genetic test result identifier"
        },
        {
            "name": "Treatment Protocol ID",
            "pattern_type": "regex",
            "pattern": r"\bTPID-[0-9]{5}\b",
            "match_count": 1,
            "proximity": 50,
            "description": "Treatment protocol identifier"
        }
    ]

    # Create custom PHI protection policy
    print("Creating custom PHI protection policy...")

    # Note: Commented out for safety - uncomment to deploy
    """
    policy = healthcare.create_custom_phi_policy(
        name="Cancer Institute - Custom PHI Protection",
        custom_patterns=custom_patterns,
        action="block"
    )

    print(f"✓ Created custom PHI policy: {policy.get('id')}")
    print(f"  Name: {policy.get('name')}")
    print(f"  Action: {policy.get('action')}")
    print(f"  Custom patterns: {len(custom_patterns)}")
    """

    print("\nCustom PHI Patterns Defined:")
    for pattern in custom_patterns:
        print(f"  - {pattern['name']}: {pattern['pattern']}")

    print("\nTo deploy these patterns:")
    print("1. Review and customize the patterns above")
    print("2. Uncomment the deployment code")
    print("3. Run this script with valid credentials")


if __name__ == "__main__":
    main()
