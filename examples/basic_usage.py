#!/usr/bin/env python3
"""
Basic Usage Example
Demonstrates basic Netskope SDK usage
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from netskope_sdk import NetskopeClient
from policies import HealthcarePolicy


def main():
    """Basic usage example"""

    # Initialize client
    print("Initializing Netskope client...")
    client = NetskopeClient(
        tenant=os.getenv("NETSKOPE_TENANT", "your-tenant"),
        api_token=os.getenv("NETSKOPE_API_TOKEN", "your-token")
    )

    # Test connection
    print("Testing connection...")
    if client.test_connection():
        print("✓ Connection successful!\n")
    else:
        print("✗ Connection failed. Check your credentials.\n")
        return

    # Get API usage statistics
    usage = client.get_api_usage()
    print(f"API Usage:")
    print(f"  Tenant: {usage['tenant']}")
    print(f"  Request count: {usage['request_count']}")
    print(f"  API version: {usage['api_version']}\n")

    # Initialize healthcare policy manager
    print("Initializing healthcare policy manager...")
    healthcare = HealthcarePolicy(
        client=client,
        organization_name="Example Cancer Center"
    )

    # Example: Deploy PHI protection (commented out for safety)
    # Uncomment to actually deploy policies
    """
    print("Deploying PHI protection policies...")
    phi_policies = healthcare.deploy_phi_protection()
    print(f"✓ Created {len(phi_policies)} PHI protection policies\n")

    # Example: Deploy threat protection
    print("Deploying threat protection policies...")
    threat_policies = healthcare.deploy_ransomware_protection()
    print(f"✓ Created {len(threat_policies)} threat protection policies\n")

    # Get deployment summary
    summary = healthcare.get_deployment_summary()
    print(f"Deployment Summary:")
    print(f"  Organization: {summary['organization']}")
    print(f"  Total policies: {summary['total_policies']}")
    """

    print("Example completed successfully!")


if __name__ == "__main__":
    main()
