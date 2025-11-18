#!/usr/bin/env python3
"""
Vendor/Business Associate Access Example
Demonstrates how to create policies for external vendors and business associates
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from netskope_sdk import NetskopeClient
from policies import HealthcarePolicy


def main():
    """Vendor access policies example"""

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

    print("Creating vendor/business associate access policies...\n")

    # CRO (Contract Research Organization)
    print("1. CRO Partner - Clinical Trial Management")
    print("   - Allowed apps: Box (specific folder access)")
    print("   - DLP monitoring: ENABLED")
    print("   - External sharing: BLOCKED")

    # Note: Commented out for safety - uncomment to deploy
    """
    cro_policies = healthcare.create_vendor_access_policy(
        vendor_name="CRO Partner",
        user_group="vendor_cro",
        allowed_apps=["Box"],
        enable_dlp=True
    )
    print(f"   ✓ Created {len(cro_policies)} policies\n")
    """

    # Medical Billing Service
    print("2. Medical Billing Service")
    print("   - Allowed apps: Office 365 Email, Billing Portal")
    print("   - DLP monitoring: ENABLED")
    print("   - PHI detection: STRICT")

    """
    billing_policies = healthcare.create_vendor_access_policy(
        vendor_name="Billing Service",
        user_group="vendor_billing",
        allowed_apps=["Office 365 Email"],
        enable_dlp=True
    )
    print(f"   ✓ Created {len(billing_policies)} policies\n")
    """

    # IT Support Vendor
    print("3. IT Support Vendor")
    print("   - Allowed apps: Remote Desktop, Office 365")
    print("   - DLP monitoring: ENABLED")
    print("   - Session recording: ENABLED")

    """
    it_vendor_policies = healthcare.create_vendor_access_policy(
        vendor_name="IT Support Vendor",
        user_group="vendor_it_support",
        allowed_apps=["Remote Desktop", "Office 365"],
        enable_dlp=True
    )
    print(f"   ✓ Created {len(it_vendor_policies)} policies\n")
    """

    # Genomics Lab Partner
    print("4. Genomics Lab Partner")
    print("   - Allowed apps: Box, SFTP")
    print("   - DLP monitoring: ENABLED")
    print("   - Genomic data protection: ENABLED")

    """
    genomics_policies = healthcare.create_vendor_access_policy(
        vendor_name="Genomics Lab",
        user_group="vendor_genomics",
        allowed_apps=["Box", "SFTP"],
        enable_dlp=True
    )
    print(f"   ✓ Created {len(genomics_policies)} policies\n")
    """

    print("\nVendor Access Best Practices:")
    print("✓ Minimum necessary access principle")
    print("✓ DLP monitoring on all vendor accounts")
    print("✓ Business Associate Agreements (BAA) required")
    print("✓ Regular access reviews (quarterly)")
    print("✓ Automatic deprovisioning after contract end")
    print("✓ Enhanced logging and monitoring")
    print("✓ MFA required for all vendor access")

    print("\nCompliance Requirements:")
    print("- HIPAA Business Associate requirements")
    print("- Access limited to specific applications")
    print("- All data transfers monitored and logged")
    print("- Breach notification procedures in place")

    print("\nTo deploy these policies:")
    print("1. Ensure BAA is signed with vendor")
    print("2. Create vendor user groups in Netskope")
    print("3. Configure MFA for vendor accounts")
    print("4. Uncomment the deployment code sections")
    print("5. Run this script with valid credentials")
    print("6. Document vendor access in compliance logs")


if __name__ == "__main__":
    main()
