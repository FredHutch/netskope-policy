#!/usr/bin/env python3
"""
Department-Specific Policies Example
Demonstrates how to create policies for different departments
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from netskope_sdk import NetskopeClient
from policies import HealthcarePolicy


def main():
    """Department-specific policies example"""

    # Initialize client
    client = NetskopeClient(
        tenant=os.getenv("NETSKOPE_TENANT"),
        api_token=os.getenv("NETSKOPE_API_TOKEN")
    )

    # Initialize healthcare policy manager
    healthcare = HealthcarePolicy(
        client=client,
        organization_name="Cancer Care Center"
    )

    print("Creating department-specific policies...\n")

    # Oncology Department
    print("1. Oncology Department")
    print("   - Allowed apps: Epic, Cerner, Box, Office 365")
    print("   - External sharing: BLOCKED")

    # Note: Commented out for safety - uncomment to deploy
    """
    oncology_policies = healthcare.create_department_policy(
        department_name="Oncology",
        user_group="oncology_users",
        allowed_apps=["Epic MyChart", "Cerner", "Box", "Office 365"],
        block_external_sharing=True
    )
    print(f"   ✓ Created {len(oncology_policies)} policies\n")
    """

    # Clinical Research Department
    print("2. Clinical Research Department")
    print("   - Allowed apps: Box, Office 365, Salesforce Health Cloud")
    print("   - External sharing: BLOCKED")

    """
    research_policies = healthcare.create_department_policy(
        department_name="Clinical Research",
        user_group="research_users",
        allowed_apps=["Box", "Office 365", "Salesforce Health Cloud"],
        block_external_sharing=True
    )
    print(f"   ✓ Created {len(research_policies)} policies\n")
    """

    # Radiology Department
    print("3. Radiology Department")
    print("   - Allowed apps: PACS, Box, Office 365")
    print("   - External sharing: BLOCKED")

    """
    radiology_policies = healthcare.create_department_policy(
        department_name="Radiology",
        user_group="radiology_users",
        allowed_apps=["PACS", "Box", "Office 365"],
        block_external_sharing=True
    )
    print(f"   ✓ Created {len(radiology_policies)} policies\n")
    """

    # Administration
    print("4. Administration Department")
    print("   - Allowed apps: Office 365, SharePoint")
    print("   - External sharing: ALLOWED (with monitoring)")

    """
    admin_policies = healthcare.create_department_policy(
        department_name="Administration",
        user_group="admin_users",
        allowed_apps=["Office 365", "SharePoint Online"],
        block_external_sharing=False
    )
    print(f"   ✓ Created {len(admin_policies)} policies\n")
    """

    # IT Department
    print("5. IT Department")
    print("   - Allowed apps: All sanctioned apps + admin tools")
    print("   - External sharing: MONITORED")

    """
    it_policies = healthcare.create_department_policy(
        department_name="IT",
        user_group="it_users",
        allowed_apps=["Office 365", "Box", "Salesforce", "Jira", "GitHub"],
        block_external_sharing=False
    )
    print(f"   ✓ Created {len(it_policies)} policies\n")
    """

    print("\nDepartment Policy Structure:")
    print("- Each department has specific app access")
    print("- Clinical departments have stricter controls")
    print("- All departments monitored for PHI")
    print("- External sharing controlled by department risk level")

    print("\nTo deploy these policies:")
    print("1. Create user groups in Netskope for each department")
    print("2. Uncomment the deployment code sections")
    print("3. Run this script with valid credentials")


if __name__ == "__main__":
    main()
