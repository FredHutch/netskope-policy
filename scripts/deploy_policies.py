#!/usr/bin/env python3
"""
Policy Deployment Script
Deploy Netskope real-time protection policies for healthcare organizations
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, Any, List

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from netskope_sdk import NetskopeClient
from policies import HealthcarePolicy


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"logs/deployment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_config(config_file: str = "config/netskope_config.json") -> Dict[str, Any]:
    """
    Load configuration from file

    Args:
        config_file: Path to configuration file

    Returns:
        Configuration dictionary
    """
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_file}")
        logger.info("Please create config/netskope_config.json or set environment variables")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in configuration file: {e}")
        sys.exit(1)


def get_credentials() -> tuple:
    """
    Get Netskope credentials from environment or config

    Returns:
        Tuple of (tenant, api_token)
    """
    # Try environment variables first
    tenant = os.getenv("NETSKOPE_TENANT")
    api_token = os.getenv("NETSKOPE_API_TOKEN")

    if tenant and api_token:
        return tenant, api_token

    # Try config file
    config = load_config()
    tenant = config.get("tenant")
    api_token = config.get("api_token")

    if not tenant or not api_token:
        logger.error("Missing credentials. Set NETSKOPE_TENANT and NETSKOPE_API_TOKEN environment variables")
        logger.error("or provide them in config/netskope_config.json")
        sys.exit(1)

    return tenant, api_token


def deploy_foundation_policies(client: NetskopeClient, org_name: str) -> Dict[str, Any]:
    """
    Deploy foundation healthcare policies

    Args:
        client: NetskopeClient instance
        org_name: Organization name

    Returns:
        Deployment results
    """
    logger.info("Deploying foundation healthcare policies...")

    healthcare = HealthcarePolicy(client, org_name)

    # Deploy PHI protection
    logger.info("Deploying PHI protection policies...")
    phi_policies = healthcare.deploy_phi_protection()
    logger.info(f"Created {len(phi_policies)} PHI protection policies")

    # Deploy threat protection
    logger.info("Deploying threat protection policies...")
    threat_policies = healthcare.deploy_ransomware_protection()
    logger.info(f"Created {len(threat_policies)} threat protection policies")

    return {
        "phi_policies": phi_policies,
        "threat_policies": threat_policies,
        "summary": healthcare.get_deployment_summary()
    }


def deploy_phi_protection(client: NetskopeClient, org_name: str) -> Dict[str, Any]:
    """
    Deploy PHI protection policies only

    Args:
        client: NetskopeClient instance
        org_name: Organization name

    Returns:
        Deployment results
    """
    logger.info("Deploying PHI protection policies...")

    healthcare = HealthcarePolicy(client, org_name)
    policies = healthcare.deploy_phi_protection()

    logger.info(f"Created {len(policies)} PHI protection policies")

    return {
        "policies": policies,
        "summary": healthcare.get_deployment_summary()
    }


def deploy_threat_protection(client: NetskopeClient, org_name: str) -> Dict[str, Any]:
    """
    Deploy threat protection policies only

    Args:
        client: NetskopeClient instance
        org_name: Organization name

    Returns:
        Deployment results
    """
    logger.info("Deploying threat protection policies...")

    healthcare = HealthcarePolicy(client, org_name)
    policies = healthcare.deploy_ransomware_protection()

    logger.info(f"Created {len(policies)} threat protection policies")

    return {
        "policies": policies,
        "summary": healthcare.get_deployment_summary()
    }


def deploy_research_protection(client: NetskopeClient, org_name: str) -> Dict[str, Any]:
    """
    Deploy clinical research data protection policies

    Args:
        client: NetskopeClient instance
        org_name: Organization name

    Returns:
        Deployment results
    """
    logger.info("Deploying clinical research data protection policies...")

    healthcare = HealthcarePolicy(client, org_name)
    policies = healthcare.deploy_research_data_protection()

    logger.info(f"Created {len(policies)} research data protection policies")

    return {
        "policies": policies,
        "summary": healthcare.get_deployment_summary()
    }


def deploy_all_policies(client: NetskopeClient, org_name: str) -> Dict[str, Any]:
    """
    Deploy all healthcare policies

    Args:
        client: NetskopeClient instance
        org_name: Organization name

    Returns:
        Deployment results
    """
    logger.info("Deploying all healthcare policies...")

    healthcare = HealthcarePolicy(client, org_name)
    results = healthcare.deploy_all()

    total = sum(len(policies) for policies in results.values())
    logger.info(f"Created {total} total policies")

    return {
        "results": results,
        "summary": healthcare.get_deployment_summary()
    }


def test_connection(client: NetskopeClient) -> bool:
    """
    Test API connection

    Args:
        client: NetskopeClient instance

    Returns:
        True if successful
    """
    logger.info("Testing API connection...")

    if client.test_connection():
        logger.info("✓ Connection successful")
        return True
    else:
        logger.error("✗ Connection failed")
        return False


def save_deployment_results(results: Dict[str, Any], output_file: str = None):
    """
    Save deployment results to file

    Args:
        results: Deployment results
        output_file: Output file path
    """
    if not output_file:
        output_file = f"logs/deployment_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    logger.info(f"Deployment results saved to: {output_file}")


def main():
    """Main deployment script"""
    parser = argparse.ArgumentParser(
        description="Deploy Netskope real-time protection policies for healthcare"
    )

    parser.add_argument(
        "--profile",
        choices=[
            "healthcare-foundation",
            "phi-protection",
            "threat-protection",
            "research-protection",
            "all"
        ],
        default="healthcare-foundation",
        help="Deployment profile to use"
    )

    parser.add_argument(
        "--org-name",
        default="Healthcare Organization",
        help="Organization name"
    )

    parser.add_argument(
        "--test-only",
        action="store_true",
        help="Test connection only, don't deploy policies"
    )

    parser.add_argument(
        "--output",
        help="Output file for deployment results"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run - show what would be deployed without deploying"
    )

    args = parser.parse_args()

    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)

    # Get credentials
    tenant, api_token = get_credentials()

    # Initialize client
    logger.info(f"Connecting to Netskope tenant: {tenant}")
    client = NetskopeClient(tenant=tenant, api_token=api_token)

    # Test connection
    if not test_connection(client):
        logger.error("Failed to connect to Netskope API")
        sys.exit(1)

    if args.test_only:
        logger.info("Test successful. Exiting.")
        sys.exit(0)

    if args.dry_run:
        logger.info("DRY RUN MODE - No policies will be deployed")
        logger.info(f"Would deploy profile: {args.profile}")
        logger.info(f"Organization: {args.org_name}")
        sys.exit(0)

    # Deploy policies based on profile
    try:
        if args.profile == "healthcare-foundation":
            results = deploy_foundation_policies(client, args.org_name)
        elif args.profile == "phi-protection":
            results = deploy_phi_protection(client, args.org_name)
        elif args.profile == "threat-protection":
            results = deploy_threat_protection(client, args.org_name)
        elif args.profile == "research-protection":
            results = deploy_research_protection(client, args.org_name)
        elif args.profile == "all":
            results = deploy_all_policies(client, args.org_name)

        # Save results
        save_deployment_results(results, args.output)

        logger.info("✓ Deployment completed successfully")

    except Exception as e:
        logger.error(f"Deployment failed: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
