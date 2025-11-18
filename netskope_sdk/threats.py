"""
Threat Protection Module
Handles malware, ransomware, and threat protection policies
"""

from typing import Dict, Any, List, Optional
from .exceptions import ValidationError


class ThreatManager:
    """
    Manages Netskope threat protection policies

    Handles:
    - Malware detection and blocking
    - Ransomware protection
    - Command and Control (C2) blocking
    - Phishing protection
    - Advanced threat protection
    """

    def __init__(self, client):
        """
        Initialize ThreatManager

        Args:
            client: NetskopeClient instance
        """
        self.client = client

    def list_threat_policies(self) -> List[Dict[str, Any]]:
        """
        List all threat protection policies

        Returns:
            List of threat policies
        """
        response = self.client.get("/policy/threat")
        return response.get("data", [])

    def get_threat_policy(self, policy_id: str) -> Dict[str, Any]:
        """
        Get a specific threat policy

        Args:
            policy_id: Threat policy identifier

        Returns:
            Threat policy details
        """
        response = self.client.get(f"/policy/threat/{policy_id}")
        return response.get("data", {})

    def create_threat_policy(
        self,
        name: str,
        action: str,
        threat_types: List[str],
        cloud_apps: Optional[List[str]] = None,
        user_groups: Optional[List[str]] = None,
        enabled: bool = True
    ) -> Dict[str, Any]:
        """
        Create a threat protection policy

        Args:
            name: Policy name
            action: Action to take ('block', 'alert', 'quarantine')
            threat_types: Types of threats to protect against
            cloud_apps: Cloud apps to apply policy to
            user_groups: User groups to apply policy to
            enabled: Whether policy is enabled

        Returns:
            Created threat policy
        """
        data = {
            "name": name,
            "type": "threat",
            "action": action,
            "threat_types": threat_types,
            "enabled": enabled,
            "rules": []
        }

        rule = {}
        if cloud_apps:
            rule["apps"] = cloud_apps
        if user_groups:
            rule["user_groups"] = user_groups

        if rule:
            data["rules"].append(rule)

        self._validate_threat_types(threat_types)

        response = self.client.post("/policy/threat", data=data)
        return response.get("data", {})

    def create_malware_policy(
        self,
        name: str,
        action: str = "block",
        scan_downloads: bool = True,
        scan_uploads: bool = True,
        cloud_apps: Optional[List[str]] = None,
        enabled: bool = True
    ) -> Dict[str, Any]:
        """
        Create a malware protection policy

        Args:
            name: Policy name
            action: Action to take ('block', 'alert', 'quarantine')
            scan_downloads: Scan file downloads
            scan_uploads: Scan file uploads
            cloud_apps: Cloud apps to apply policy to
            enabled: Whether policy is enabled

        Returns:
            Created malware policy
        """
        data = {
            "name": name,
            "type": "malware",
            "action": action,
            "enabled": enabled,
            "settings": {
                "scan_downloads": scan_downloads,
                "scan_uploads": scan_uploads
            },
            "rules": []
        }

        if cloud_apps:
            data["rules"].append({"apps": cloud_apps})

        response = self.client.post("/policy/malware", data=data)
        return response.get("data", {})

    def create_ransomware_protection(
        self,
        name: str = "Ransomware Protection Policy",
        action: str = "block",
        enable_behavioral_detection: bool = True,
        enable_file_type_blocking: bool = True,
        enable_anomaly_detection: bool = True
    ) -> Dict[str, Any]:
        """
        Create a comprehensive ransomware protection policy

        Args:
            name: Policy name
            action: Action to take ('block', 'alert', 'quarantine')
            enable_behavioral_detection: Enable behavioral analysis
            enable_file_type_blocking: Block known ransomware file types
            enable_anomaly_detection: Enable anomaly detection

        Returns:
            Created ransomware policy
        """
        data = {
            "name": name,
            "type": "threat",
            "action": action,
            "enabled": True,
            "threat_types": [
                "ransomware",
                "malware",
                "cryptominer"
            ],
            "settings": {
                "behavioral_detection": enable_behavioral_detection,
                "file_type_blocking": enable_file_type_blocking,
                "anomaly_detection": enable_anomaly_detection,
                "aggressive_mode": True  # More aggressive for healthcare
            },
            "rules": [
                {
                    "description": "Block all ransomware activities",
                    "severity": "critical"
                }
            ]
        }

        response = self.client.post("/policy/threat", data=data)
        return response.get("data", {})

    def create_phishing_protection(
        self,
        name: str = "Phishing Protection Policy",
        action: str = "block",
        enable_credential_theft_prevention: bool = True,
        enable_url_analysis: bool = True
    ) -> Dict[str, Any]:
        """
        Create a phishing protection policy

        Args:
            name: Policy name
            action: Action to take ('block', 'alert')
            enable_credential_theft_prevention: Prevent credential theft
            enable_url_analysis: Enable URL reputation analysis

        Returns:
            Created phishing policy
        """
        data = {
            "name": name,
            "type": "threat",
            "action": action,
            "enabled": True,
            "threat_types": [
                "phishing",
                "credential_theft",
                "social_engineering"
            ],
            "settings": {
                "credential_theft_prevention": enable_credential_theft_prevention,
                "url_analysis": enable_url_analysis,
                "real_time_protection": True
            },
            "rules": [
                {
                    "description": "Block phishing and credential theft attempts",
                    "severity": "high"
                }
            ]
        }

        response = self.client.post("/policy/threat", data=data)
        return response.get("data", {})

    def create_c2_blocking_policy(
        self,
        name: str = "Command and Control Blocking",
        action: str = "block"
    ) -> Dict[str, Any]:
        """
        Create a Command and Control (C2) blocking policy

        Args:
            name: Policy name
            action: Action to take ('block', 'alert')

        Returns:
            Created C2 blocking policy
        """
        data = {
            "name": name,
            "type": "threat",
            "action": action,
            "enabled": True,
            "threat_types": [
                "c2",
                "botnet",
                "backdoor"
            ],
            "settings": {
                "block_known_c2": True,
                "block_suspicious_dns": True,
                "block_tor_traffic": True  # Optional: block Tor for healthcare
            },
            "rules": [
                {
                    "description": "Block all C2 and botnet communication",
                    "severity": "critical"
                }
            ]
        }

        response = self.client.post("/policy/threat", data=data)
        return response.get("data", {})

    def create_healthcare_threat_protection(
        self,
        organization_name: str
    ) -> List[Dict[str, Any]]:
        """
        Create comprehensive threat protection suite for healthcare

        Args:
            organization_name: Name of the healthcare organization

        Returns:
            List of created policies
        """
        policies = []

        # 1. Ransomware Protection (Highest Priority)
        policies.append(
            self.create_ransomware_protection(
                name=f"{organization_name} - Ransomware Protection",
                action="block",
                enable_behavioral_detection=True,
                enable_file_type_blocking=True,
                enable_anomaly_detection=True
            )
        )

        # 2. Phishing Protection
        policies.append(
            self.create_phishing_protection(
                name=f"{organization_name} - Phishing Protection",
                action="block",
                enable_credential_theft_prevention=True,
                enable_url_analysis=True
            )
        )

        # 3. C2 Blocking
        policies.append(
            self.create_c2_blocking_policy(
                name=f"{organization_name} - C2 Blocking",
                action="block"
            )
        )

        # 4. General Malware Protection
        policies.append(
            self.create_malware_policy(
                name=f"{organization_name} - Malware Protection",
                action="block",
                scan_downloads=True,
                scan_uploads=True
            )
        )

        return policies

    def list_threat_incidents(
        self,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        threat_type: Optional[str] = None,
        severity: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        List threat incidents

        Args:
            start_time: Start time for incident search (ISO format)
            end_time: End time for incident search (ISO format)
            threat_type: Filter by threat type
            severity: Filter by severity
            limit: Maximum number of results

        Returns:
            List of threat incidents
        """
        params = {"limit": limit}

        if start_time:
            params["starttime"] = start_time
        if end_time:
            params["endtime"] = end_time
        if threat_type:
            params["threat_type"] = threat_type
        if severity:
            params["severity"] = severity

        response = self.client.get("/events/data/threat", params=params)
        return response.get("data", [])

    def get_threat_statistics(
        self,
        start_time: str,
        end_time: str
    ) -> Dict[str, Any]:
        """
        Get threat statistics for a time period

        Args:
            start_time: Start time (ISO format)
            end_time: End time (ISO format)

        Returns:
            Threat statistics
        """
        params = {
            "starttime": start_time,
            "endtime": end_time
        }

        response = self.client.get("/reports/threat/summary", params=params)
        return response.get("data", {})

    def update_threat_policy(
        self,
        policy_id: str,
        action: Optional[str] = None,
        threat_types: Optional[List[str]] = None,
        enabled: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Update a threat policy

        Args:
            policy_id: Threat policy identifier
            action: Updated action
            threat_types: Updated threat types
            enabled: Updated enabled status

        Returns:
            Updated threat policy
        """
        data = {}

        if action:
            data["action"] = action
        if threat_types:
            self._validate_threat_types(threat_types)
            data["threat_types"] = threat_types
        if enabled is not None:
            data["enabled"] = enabled

        response = self.client.put(f"/policy/threat/{policy_id}", data=data)
        return response.get("data", {})

    def delete_threat_policy(self, policy_id: str) -> bool:
        """
        Delete a threat policy

        Args:
            policy_id: Threat policy identifier

        Returns:
            True if successful
        """
        self.client.delete(f"/policy/threat/{policy_id}")
        return True

    def _validate_threat_types(self, threat_types: List[str]) -> None:
        """
        Validate threat types

        Args:
            threat_types: List of threat types to validate

        Raises:
            ValidationError: If validation fails
        """
        valid_threat_types = [
            "malware",
            "ransomware",
            "phishing",
            "credential_theft",
            "c2",
            "botnet",
            "backdoor",
            "cryptominer",
            "social_engineering",
            "trojan",
            "virus",
            "worm",
            "spyware",
            "adware"
        ]

        for threat_type in threat_types:
            if threat_type not in valid_threat_types:
                raise ValidationError(
                    f"Invalid threat type '{threat_type}'. Must be one of: {', '.join(valid_threat_types)}"
                )
