"""
Healthcare-Specific Policy Templates
Pre-configured policies for cancer clinical care and research organizations
"""

from typing import Dict, Any, List, Optional
from netskope_sdk import NetskopeClient
from netskope_sdk.dlp import DLPManager
from netskope_sdk.threats import ThreatManager
from netskope_sdk.policies import PolicyManager


class HealthcarePolicy:
    """
    Healthcare-specific policy management

    Provides pre-configured policies for:
    - HIPAA compliance
    - PHI protection
    - Clinical research data protection
    - Ransomware and malware protection
    - Cloud app security for healthcare SaaS
    """

    def __init__(self, client: NetskopeClient, organization_name: str = "Healthcare Organization"):
        """
        Initialize HealthcarePolicy

        Args:
            client: NetskopeClient instance
            organization_name: Name of your organization
        """
        self.client = client
        self.organization_name = organization_name
        self.dlp_manager = DLPManager(client)
        self.threat_manager = ThreatManager(client)
        self.policy_manager = PolicyManager(client)

        self.deployed_policies = []

    def deploy_all(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Deploy all healthcare policies

        Returns:
            Dictionary of deployed policies by category
        """
        results = {
            "phi_protection": self.deploy_phi_protection(),
            "research_protection": self.deploy_research_data_protection(),
            "threat_protection": self.deploy_ransomware_protection(),
            "cloud_app_controls": self.deploy_cloud_app_controls(),
            "web_filtering": self.deploy_web_filtering()
        }

        return results

    def deploy_phi_protection(self) -> List[Dict[str, Any]]:
        """
        Deploy PHI protection policies

        Returns:
            List of created DLP policies
        """
        policies = []

        # Create PHI DLP Profile
        phi_profile = self.dlp_manager.create_phi_protection_profile(
            name=f"{self.organization_name} - PHI Protection Profile",
            include_mrn=True,
            include_ssn=True,
            include_dob=True,
            include_diagnosis_codes=True
        )

        # Create DLP Policy for unsanctioned cloud apps
        unsanctioned_policy = self.dlp_manager.create_dlp_policy(
            name=f"{self.organization_name} - Block PHI to Unsanctioned Apps",
            profile_id=phi_profile.get("id", "phi_profile"),
            action="block",
            enabled=True
        )
        policies.append(unsanctioned_policy)

        # Create DLP Policy for email
        email_policy = self.dlp_manager.create_dlp_policy(
            name=f"{self.organization_name} - PHI Email Protection",
            profile_id=phi_profile.get("id", "phi_profile"),
            action="encrypt",
            cloud_apps=["Gmail", "Office 365 Email", "Exchange Online"],
            enabled=True
        )
        policies.append(email_policy)

        # Create DLP Policy for file sharing
        file_sharing_policy = self.dlp_manager.create_dlp_policy(
            name=f"{self.organization_name} - PHI File Sharing Protection",
            profile_id=phi_profile.get("id", "phi_profile"),
            action="alert",
            cloud_apps=["Box", "OneDrive", "Google Drive", "Dropbox"],
            enabled=True
        )
        policies.append(file_sharing_policy)

        self.deployed_policies.extend(policies)
        return policies

    def deploy_research_data_protection(self) -> List[Dict[str, Any]]:
        """
        Deploy clinical research data protection policies

        Returns:
            List of created DLP policies
        """
        policies = []

        # Create Research Data DLP Profile
        research_profile = self.dlp_manager.create_research_data_profile(
            name=f"{self.organization_name} - Clinical Research Data Profile"
        )

        # Create DLP Policy for research data
        research_policy = self.dlp_manager.create_dlp_policy(
            name=f"{self.organization_name} - Clinical Research Data Protection",
            profile_id=research_profile.get("id", "research_profile"),
            action="alert",
            enabled=True
        )
        policies.append(research_policy)

        # Create policy for genomic data
        genomic_policy = self.dlp_manager.create_dlp_policy(
            name=f"{self.organization_name} - Genomic Data Protection",
            profile_id=research_profile.get("id", "research_profile"),
            action="block",
            cloud_apps=["Personal Cloud Storage"],
            enabled=True
        )
        policies.append(genomic_policy)

        self.deployed_policies.extend(policies)
        return policies

    def deploy_ransomware_protection(self) -> List[Dict[str, Any]]:
        """
        Deploy comprehensive ransomware and threat protection

        Returns:
            List of created threat policies
        """
        policies = self.threat_manager.create_healthcare_threat_protection(
            organization_name=self.organization_name
        )

        self.deployed_policies.extend(policies)
        return policies

    def deploy_cloud_app_controls(self) -> List[Dict[str, Any]]:
        """
        Deploy cloud app security controls

        Returns:
            List of created cloud app policies
        """
        policies = []

        # Sanctioned Healthcare Apps
        sanctioned_apps = [
            "Epic MyChart",
            "Cerner",
            "Box",
            "Microsoft Teams",
            "Zoom for Healthcare",
            "Office 365",
            "Salesforce Health Cloud"
        ]

        # Unsanctioned Apps to Block
        unsanctioned_apps = [
            "Personal Dropbox",
            "Personal Google Drive",
            "WeTransfer",
            "Personal OneDrive",
            "WhatsApp Web",
            "Telegram Web"
        ]

        # Allow sanctioned healthcare apps
        for app in sanctioned_apps:
            policy = self.policy_manager.create_cloud_app_policy(
                name=f"{self.organization_name} - Allow {app}",
                app_name=app,
                action="allow",
                activities=["upload", "download", "share"],
                enabled=True
            )
            policies.append(policy)

        # Block unsanctioned apps
        for app in unsanctioned_apps:
            policy = self.policy_manager.create_cloud_app_policy(
                name=f"{self.organization_name} - Block {app}",
                app_name=app,
                action="block",
                activities=["upload", "download", "share"],
                enabled=True
            )
            policies.append(policy)

        # Control file sharing
        file_sharing_policy = self.policy_manager.create_cloud_app_policy(
            name=f"{self.organization_name} - Control External Sharing",
            app_name="Box",
            action="alert",
            activities=["share_external"],
            enabled=True
        )
        policies.append(file_sharing_policy)

        self.deployed_policies.extend(policies)
        return policies

    def deploy_web_filtering(self) -> List[Dict[str, Any]]:
        """
        Deploy web filtering policies

        Returns:
            List of created web policies
        """
        policies = []

        # Block malicious categories
        malicious_categories = [
            "Malware",
            "Phishing",
            "Spam",
            "Adult Content",
            "Illegal Activities",
            "Gambling",
            "Hacking"
        ]

        malicious_policy = self.policy_manager.create_web_policy(
            name=f"{self.organization_name} - Block Malicious Sites",
            action="block",
            categories=malicious_categories,
            enabled=True
        )
        policies.append(malicious_policy)

        # Alert on risky categories
        risky_categories = [
            "Peer-to-Peer",
            "Anonymizers",
            "Remote Access",
            "Cloud Storage (Personal)"
        ]

        risky_policy = self.policy_manager.create_web_policy(
            name=f"{self.organization_name} - Alert Risky Sites",
            action="alert",
            categories=risky_categories,
            enabled=True
        )
        policies.append(risky_policy)

        self.deployed_policies.extend(policies)
        return policies

    def create_custom_phi_policy(
        self,
        name: str,
        custom_patterns: List[Dict[str, str]],
        action: str = "block"
    ) -> Dict[str, Any]:
        """
        Create a custom PHI protection policy with organization-specific patterns

        Args:
            name: Policy name
            custom_patterns: Custom regex patterns for organization-specific PHI
            action: Action to take ('block', 'alert', 'encrypt')

        Returns:
            Created DLP policy

        Example:
            custom_patterns = [
                {
                    "name": "Custom Patient ID",
                    "pattern_type": "regex",
                    "pattern": r"\\bPT-[0-9]{6}\\b",
                    "match_count": 1,
                    "proximity": 50,
                    "description": "Custom patient identifier format"
                }
            ]
        """
        profile = self.dlp_manager.create_phi_protection_profile(
            name=f"{name} - Profile",
            custom_patterns=custom_patterns
        )

        policy = self.dlp_manager.create_dlp_policy(
            name=name,
            profile_id=profile.get("id", "custom_profile"),
            action=action,
            enabled=True
        )

        self.deployed_policies.append(policy)
        return policy

    def create_department_policy(
        self,
        department_name: str,
        user_group: str,
        allowed_apps: List[str],
        block_external_sharing: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Create department-specific policies

        Args:
            department_name: Name of department (e.g., "Oncology")
            user_group: User group identifier
            allowed_apps: List of allowed cloud apps
            block_external_sharing: Block external sharing

        Returns:
            List of created policies
        """
        policies = []

        # Allow specific apps for department
        for app in allowed_apps:
            policy = self.policy_manager.create_cloud_app_policy(
                name=f"{self.organization_name} - {department_name} - {app} Access",
                app_name=app,
                action="allow",
                user_groups=[user_group],
                enabled=True
            )
            policies.append(policy)

        # Block external sharing if required
        if block_external_sharing:
            sharing_policy = self.policy_manager.create_cloud_app_policy(
                name=f"{self.organization_name} - {department_name} - Block External Sharing",
                app_name="All Apps",
                action="block",
                activities=["share_external"],
                user_groups=[user_group],
                enabled=True
            )
            policies.append(sharing_policy)

        self.deployed_policies.extend(policies)
        return policies

    def create_vendor_access_policy(
        self,
        vendor_name: str,
        user_group: str,
        allowed_apps: List[str],
        enable_dlp: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Create policies for vendor/business associate access

        Args:
            vendor_name: Vendor/business associate name
            user_group: Vendor user group
            allowed_apps: List of allowed cloud apps for vendor
            enable_dlp: Enable DLP monitoring for vendor

        Returns:
            List of created policies
        """
        policies = []

        # Allow specific apps for vendor
        for app in allowed_apps:
            policy = self.policy_manager.create_cloud_app_policy(
                name=f"{self.organization_name} - Vendor {vendor_name} - {app} Access",
                app_name=app,
                action="allow",
                user_groups=[user_group],
                enabled=True
            )
            policies.append(policy)

        # Enable DLP monitoring for vendor activities
        if enable_dlp:
            phi_profile = self.dlp_manager.create_phi_protection_profile(
                name=f"{self.organization_name} - Vendor {vendor_name} - PHI Monitoring"
            )

            dlp_policy = self.dlp_manager.create_dlp_policy(
                name=f"{self.organization_name} - Vendor {vendor_name} - DLP Monitoring",
                profile_id=phi_profile.get("id", "vendor_phi_profile"),
                action="alert",
                user_groups=[user_group],
                enabled=True
            )
            policies.append(dlp_policy)

        self.deployed_policies.extend(policies)
        return policies

    def get_deployment_summary(self) -> Dict[str, Any]:
        """
        Get summary of deployed policies

        Returns:
            Summary of all deployed policies
        """
        return {
            "organization": self.organization_name,
            "total_policies": len(self.deployed_policies),
            "policies": self.deployed_policies
        }

    def enable_monitor_mode(self, policy_id: str) -> Dict[str, Any]:
        """
        Switch a policy to monitor-only mode (alert instead of block)

        Args:
            policy_id: Policy identifier

        Returns:
            Updated policy
        """
        return self.policy_manager.update_policy(
            policy_id,
            {"action": "alert"}
        )

    def enable_enforcement_mode(self, policy_id: str) -> Dict[str, Any]:
        """
        Switch a policy to enforcement mode (block)

        Args:
            policy_id: Policy identifier

        Returns:
            Updated policy
        """
        return self.policy_manager.update_policy(
            policy_id,
            {"action": "block"}
        )
