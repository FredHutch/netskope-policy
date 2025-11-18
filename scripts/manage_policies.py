#!/usr/bin/env python3
"""
Policy Management Script
Manage existing Netskope policies - list, enable, disable, delete
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from typing import List, Dict, Any

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from netskope_sdk import NetskopeClient
from netskope_sdk.policies import PolicyManager
from netskope_sdk.dlp import DLPManager
from netskope_sdk.threats import ThreatManager


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_credentials() -> tuple:
    """Get Netskope credentials"""
    tenant = os.getenv("NETSKOPE_TENANT")
    api_token = os.getenv("NETSKOPE_API_TOKEN")

    if not tenant or not api_token:
        logger.error("Missing credentials. Set NETSKOPE_TENANT and NETSKOPE_API_TOKEN")
        sys.exit(1)

    return tenant, api_token


def list_all_policies(client: NetskopeClient) -> Dict[str, List[Dict[str, Any]]]:
    """
    List all policies

    Args:
        client: NetskopeClient instance

    Returns:
        Dictionary of policies by type
    """
    policy_manager = PolicyManager(client)
    dlp_manager = DLPManager(client)
    threat_manager = ThreatManager(client)

    policies = {
        "all_policies": policy_manager.list_policies(),
        "dlp_profiles": dlp_manager.list_dlp_profiles(),
        "threat_policies": threat_manager.list_threat_policies()
    }

    return policies


def display_policies(policies: Dict[str, List[Dict[str, Any]]]):
    """
    Display policies in formatted output

    Args:
        policies: Dictionary of policies
    """
    print("\n" + "="*80)
    print("NETSKOPE POLICIES")
    print("="*80)

    for policy_type, policy_list in policies.items():
        print(f"\n{policy_type.upper().replace('_', ' ')}:")
        print("-" * 80)

        if not policy_list:
            print("  No policies found")
            continue

        for policy in policy_list:
            policy_id = policy.get("id", "N/A")
            name = policy.get("name", "Unnamed")
            enabled = policy.get("enabled", False)
            status = "✓ ENABLED" if enabled else "✗ DISABLED"

            print(f"  [{policy_id}] {name}")
            print(f"    Status: {status}")

            if "type" in policy:
                print(f"    Type: {policy['type']}")
            if "action" in policy:
                print(f"    Action: {policy['action']}")
            if "severity" in policy:
                print(f"    Severity: {policy['severity']}")

            print()


def enable_policy(client: NetskopeClient, policy_id: str) -> bool:
    """
    Enable a policy

    Args:
        client: NetskopeClient instance
        policy_id: Policy identifier

    Returns:
        True if successful
    """
    policy_manager = PolicyManager(client)

    try:
        policy_manager.enable_policy(policy_id)
        logger.info(f"✓ Policy {policy_id} enabled")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to enable policy: {e}")
        return False


def disable_policy(client: NetskopeClient, policy_id: str) -> bool:
    """
    Disable a policy

    Args:
        client: NetskopeClient instance
        policy_id: Policy identifier

    Returns:
        True if successful
    """
    policy_manager = PolicyManager(client)

    try:
        policy_manager.disable_policy(policy_id)
        logger.info(f"✓ Policy {policy_id} disabled")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to disable policy: {e}")
        return False


def delete_policy(client: NetskopeClient, policy_id: str, force: bool = False) -> bool:
    """
    Delete a policy

    Args:
        client: NetskopeClient instance
        policy_id: Policy identifier
        force: Skip confirmation

    Returns:
        True if successful
    """
    if not force:
        confirm = input(f"Are you sure you want to delete policy {policy_id}? (yes/no): ")
        if confirm.lower() != "yes":
            logger.info("Deletion cancelled")
            return False

    policy_manager = PolicyManager(client)

    try:
        policy_manager.delete_policy(policy_id)
        logger.info(f"✓ Policy {policy_id} deleted")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to delete policy: {e}")
        return False


def get_policy_details(client: NetskopeClient, policy_id: str):
    """
    Get detailed information about a policy

    Args:
        client: NetskopeClient instance
        policy_id: Policy identifier
    """
    policy_manager = PolicyManager(client)

    try:
        policy = policy_manager.get_policy(policy_id)
        print("\n" + "="*80)
        print(f"POLICY DETAILS: {policy_id}")
        print("="*80)
        print(json.dumps(policy, indent=2))
    except Exception as e:
        logger.error(f"✗ Failed to get policy details: {e}")


def list_dlp_incidents(client: NetskopeClient, days: int = 7):
    """
    List recent DLP incidents

    Args:
        client: NetskopeClient instance
        days: Number of days to look back
    """
    dlp_manager = DLPManager(client)

    try:
        from datetime import timedelta
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)

        incidents = dlp_manager.list_dlp_incidents(
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            limit=100
        )

        print("\n" + "="*80)
        print(f"DLP INCIDENTS (Last {days} days)")
        print("="*80)

        if not incidents:
            print("No incidents found")
            return

        for incident in incidents:
            print(f"\nIncident ID: {incident.get('id', 'N/A')}")
            print(f"  Time: {incident.get('timestamp', 'N/A')}")
            print(f"  User: {incident.get('user', 'N/A')}")
            print(f"  Policy: {incident.get('policy', 'N/A')}")
            print(f"  Action: {incident.get('action', 'N/A')}")
            print(f"  Severity: {incident.get('severity', 'N/A')}")

    except Exception as e:
        logger.error(f"✗ Failed to list DLP incidents: {e}")


def list_threat_incidents(client: NetskopeClient, days: int = 7):
    """
    List recent threat incidents

    Args:
        client: NetskopeClient instance
        days: Number of days to look back
    """
    threat_manager = ThreatManager(client)

    try:
        from datetime import timedelta
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)

        incidents = threat_manager.list_threat_incidents(
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            limit=100
        )

        print("\n" + "="*80)
        print(f"THREAT INCIDENTS (Last {days} days)")
        print("="*80)

        if not incidents:
            print("No incidents found")
            return

        for incident in incidents:
            print(f"\nIncident ID: {incident.get('id', 'N/A')}")
            print(f"  Time: {incident.get('timestamp', 'N/A')}")
            print(f"  User: {incident.get('user', 'N/A')}")
            print(f"  Threat Type: {incident.get('threat_type', 'N/A')}")
            print(f"  Action: {incident.get('action', 'N/A')}")
            print(f"  Severity: {incident.get('severity', 'N/A')}")

    except Exception as e:
        logger.error(f"✗ Failed to list threat incidents: {e}")


def export_policies(client: NetskopeClient, output_file: str):
    """
    Export all policies to JSON file

    Args:
        client: NetskopeClient instance
        output_file: Output file path
    """
    policies = list_all_policies(client)

    with open(output_file, 'w') as f:
        json.dump(policies, f, indent=2)

    logger.info(f"✓ Policies exported to: {output_file}")


def main():
    """Main management script"""
    parser = argparse.ArgumentParser(
        description="Manage Netskope policies"
    )

    parser.add_argument(
        "action",
        choices=[
            "list",
            "enable",
            "disable",
            "delete",
            "details",
            "dlp-incidents",
            "threat-incidents",
            "export"
        ],
        help="Action to perform"
    )

    parser.add_argument(
        "--policy-id",
        help="Policy ID (required for enable, disable, delete, details)"
    )

    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days for incident reports (default: 7)"
    )

    parser.add_argument(
        "--output",
        help="Output file for export"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Force action without confirmation"
    )

    args = parser.parse_args()

    # Get credentials
    tenant, api_token = get_credentials()

    # Initialize client
    client = NetskopeClient(tenant=tenant, api_token=api_token)

    # Perform action
    try:
        if args.action == "list":
            policies = list_all_policies(client)
            display_policies(policies)

        elif args.action == "enable":
            if not args.policy_id:
                logger.error("--policy-id required for enable action")
                sys.exit(1)
            enable_policy(client, args.policy_id)

        elif args.action == "disable":
            if not args.policy_id:
                logger.error("--policy-id required for disable action")
                sys.exit(1)
            disable_policy(client, args.policy_id)

        elif args.action == "delete":
            if not args.policy_id:
                logger.error("--policy-id required for delete action")
                sys.exit(1)
            delete_policy(client, args.policy_id, args.force)

        elif args.action == "details":
            if not args.policy_id:
                logger.error("--policy-id required for details action")
                sys.exit(1)
            get_policy_details(client, args.policy_id)

        elif args.action == "dlp-incidents":
            list_dlp_incidents(client, args.days)

        elif args.action == "threat-incidents":
            list_threat_incidents(client, args.days)

        elif args.action == "export":
            output = args.output or f"policies_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            export_policies(client, output)

    except Exception as e:
        logger.error(f"Action failed: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
