"""
Data Loss Prevention (DLP) Module
Handles DLP policies, profiles, and rules for healthcare PHI protection
"""

from typing import Dict, Any, List, Optional
from .exceptions import ValidationError


class DLPManager:
    """
    Manages Netskope DLP policies and profiles

    Specialized for healthcare PHI protection:
    - Patient identifiers
    - Medical record numbers
    - Diagnosis codes
    - Treatment information
    - Genomic data
    """

    def __init__(self, client):
        """
        Initialize DLPManager

        Args:
            client: NetskopeClient instance
        """
        self.client = client

    def list_dlp_profiles(self) -> List[Dict[str, Any]]:
        """
        List all DLP profiles

        Returns:
            List of DLP profiles
        """
        response = self.client.get("/policy/dlp/profiles")
        return response.get("data", [])

    def get_dlp_profile(self, profile_id: str) -> Dict[str, Any]:
        """
        Get a specific DLP profile

        Args:
            profile_id: DLP profile identifier

        Returns:
            DLP profile details
        """
        response = self.client.get(f"/policy/dlp/profiles/{profile_id}")
        return response.get("data", {})

    def create_dlp_profile(
        self,
        name: str,
        rules: List[Dict[str, Any]],
        description: Optional[str] = None,
        severity: str = "high"
    ) -> Dict[str, Any]:
        """
        Create a DLP profile

        Args:
            name: Profile name
            rules: List of DLP rules
            description: Profile description
            severity: Severity level ('low', 'medium', 'high', 'critical')

        Returns:
            Created DLP profile
        """
        data = {
            "name": name,
            "rules": rules,
            "severity": severity
        }

        if description:
            data["description"] = description

        self._validate_dlp_rules(rules)

        response = self.client.post("/policy/dlp/profiles", data=data)
        return response.get("data", {})

    def update_dlp_profile(
        self,
        profile_id: str,
        name: Optional[str] = None,
        rules: Optional[List[Dict[str, Any]]] = None,
        severity: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update a DLP profile

        Args:
            profile_id: DLP profile identifier
            name: Updated profile name
            rules: Updated list of DLP rules
            severity: Updated severity level

        Returns:
            Updated DLP profile
        """
        data = {}

        if name:
            data["name"] = name
        if rules:
            self._validate_dlp_rules(rules)
            data["rules"] = rules
        if severity:
            data["severity"] = severity

        response = self.client.put(f"/policy/dlp/profiles/{profile_id}", data=data)
        return response.get("data", {})

    def delete_dlp_profile(self, profile_id: str) -> bool:
        """
        Delete a DLP profile

        Args:
            profile_id: DLP profile identifier

        Returns:
            True if successful
        """
        self.client.delete(f"/policy/dlp/profiles/{profile_id}")
        return True

    def create_dlp_policy(
        self,
        name: str,
        profile_id: str,
        action: str,
        cloud_apps: Optional[List[str]] = None,
        user_groups: Optional[List[str]] = None,
        enabled: bool = True
    ) -> Dict[str, Any]:
        """
        Create a DLP policy

        Args:
            name: Policy name
            profile_id: DLP profile to apply
            action: Action to take ('block', 'alert', 'quarantine', 'encrypt')
            cloud_apps: Cloud apps to apply policy to
            user_groups: User groups to apply policy to
            enabled: Whether policy is enabled

        Returns:
            Created DLP policy
        """
        data = {
            "name": name,
            "type": "dlp",
            "profile_id": profile_id,
            "action": action,
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

        response = self.client.post("/policy/dlp", data=data)
        return response.get("data", {})

    def create_phi_protection_profile(
        self,
        name: str = "PHI Protection Profile",
        include_mrn: bool = True,
        include_ssn: bool = True,
        include_dob: bool = True,
        include_diagnosis_codes: bool = True,
        custom_patterns: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Create a healthcare-specific PHI protection DLP profile

        Args:
            name: Profile name
            include_mrn: Include Medical Record Number detection
            include_ssn: Include SSN detection
            include_dob: Include Date of Birth detection
            include_diagnosis_codes: Include ICD-10 diagnosis codes
            custom_patterns: Custom regex patterns for additional PHI

        Returns:
            Created DLP profile
        """
        rules = []

        # Medical Record Number (MRN) - typical format: 7-10 digits
        if include_mrn:
            rules.append({
                "name": "Medical Record Number",
                "pattern_type": "regex",
                "pattern": r"\b(MRN|MR#|Medical Record)[\s:#-]*([0-9]{7,10})\b",
                "match_count": 1,
                "proximity": 50,
                "description": "Detects medical record numbers"
            })

        # Social Security Number
        if include_ssn:
            rules.append({
                "name": "Social Security Number",
                "pattern_type": "predefined",
                "pattern": "SSN",
                "match_count": 1,
                "description": "Detects US Social Security Numbers"
            })

        # Date of Birth patterns
        if include_dob:
            rules.append({
                "name": "Date of Birth",
                "pattern_type": "regex",
                "pattern": r"\b(DOB|Date of Birth)[\s:#-]*(0[1-9]|1[0-2])[/-](0[1-9]|[12][0-9]|3[01])[/-](19|20)\d{2}\b",
                "match_count": 1,
                "proximity": 30,
                "description": "Detects dates of birth"
            })

        # ICD-10 Diagnosis Codes
        if include_diagnosis_codes:
            rules.append({
                "name": "ICD-10 Diagnosis Codes",
                "pattern_type": "regex",
                "pattern": r"\b[A-Z]\d{2}(\.\d{1,4})?\b",
                "match_count": 2,
                "proximity": 200,
                "description": "Detects ICD-10 diagnosis codes"
            })

        # Health Insurance information
        rules.append({
            "name": "Health Insurance Information",
            "pattern_type": "regex",
            "pattern": r"\b(Policy|Member|Subscriber)[\s#:]*([A-Z0-9]{8,})\b",
            "match_count": 1,
            "proximity": 100,
            "description": "Detects health insurance policy/member numbers"
        })

        # Patient name patterns (when near other PHI)
        rules.append({
            "name": "Patient Name Context",
            "pattern_type": "regex",
            "pattern": r"\b(Patient|Subject)[\s:]*(Name|ID)[\s:]*([A-Z][a-z]+\s[A-Z][a-z]+)\b",
            "match_count": 1,
            "proximity": 50,
            "description": "Detects patient name fields"
        })

        # Add custom patterns
        if custom_patterns:
            for pattern in custom_patterns:
                rules.append(pattern)

        return self.create_dlp_profile(
            name=name,
            rules=rules,
            description="Healthcare PHI protection profile for HIPAA compliance",
            severity="critical"
        )

    def create_research_data_profile(
        self,
        name: str = "Clinical Research Data Profile"
    ) -> Dict[str, Any]:
        """
        Create a DLP profile for clinical research data protection

        Args:
            name: Profile name

        Returns:
            Created DLP profile
        """
        rules = [
            {
                "name": "Clinical Trial Protocol",
                "pattern_type": "regex",
                "pattern": r"\b(Protocol|Study)\s*(Number|ID)[\s:#-]*([A-Z0-9-]{5,})\b",
                "match_count": 1,
                "proximity": 100,
                "description": "Detects clinical trial protocol identifiers"
            },
            {
                "name": "Subject ID",
                "pattern_type": "regex",
                "pattern": r"\b(Subject|Participant)[\s#:]*([0-9]{4,})\b",
                "match_count": 1,
                "proximity": 50,
                "description": "Detects research subject identifiers"
            },
            {
                "name": "Genomic Data Markers",
                "pattern_type": "regex",
                "pattern": r"\b(rs\d{7,}|chr[0-9XY]{1,2}:\d+|ENSG\d{11})\b",
                "match_count": 3,
                "proximity": 500,
                "description": "Detects genomic data identifiers (SNPs, gene IDs)"
            },
            {
                "name": "Biospecimen ID",
                "pattern_type": "regex",
                "pattern": r"\b(Specimen|Sample)[\s#:]*([A-Z0-9-]{6,})\b",
                "match_count": 1,
                "proximity": 50,
                "description": "Detects biospecimen identifiers"
            },
            {
                "name": "IRB Protocol",
                "pattern_type": "regex",
                "pattern": r"\bIRB[\s#-]*(\d{4,})\b",
                "match_count": 1,
                "proximity": 50,
                "description": "Detects IRB protocol numbers"
            }
        ]

        return self.create_dlp_profile(
            name=name,
            rules=rules,
            description="Clinical research data protection profile",
            severity="high"
        )

    def list_dlp_incidents(
        self,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        severity: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        List DLP incidents

        Args:
            start_time: Start time for incident search (ISO format)
            end_time: End time for incident search (ISO format)
            severity: Filter by severity
            limit: Maximum number of results

        Returns:
            List of DLP incidents
        """
        params = {"limit": limit}

        if start_time:
            params["starttime"] = start_time
        if end_time:
            params["endtime"] = end_time
        if severity:
            params["severity"] = severity

        response = self.client.get("/events/data/dlp", params=params)
        return response.get("data", [])

    def get_dlp_statistics(
        self,
        start_time: str,
        end_time: str
    ) -> Dict[str, Any]:
        """
        Get DLP statistics for a time period

        Args:
            start_time: Start time (ISO format)
            end_time: End time (ISO format)

        Returns:
            DLP statistics
        """
        params = {
            "starttime": start_time,
            "endtime": end_time
        }

        response = self.client.get("/reports/dlp/summary", params=params)
        return response.get("data", {})

    def _validate_dlp_rules(self, rules: List[Dict[str, Any]]) -> None:
        """
        Validate DLP rules

        Args:
            rules: List of DLP rules to validate

        Raises:
            ValidationError: If validation fails
        """
        required_fields = ["name", "pattern_type", "pattern"]

        for i, rule in enumerate(rules):
            for field in required_fields:
                if field not in rule:
                    raise ValidationError(
                        f"Rule {i}: Missing required field '{field}'"
                    )

            # Validate pattern_type
            valid_pattern_types = ["regex", "predefined", "fingerprint", "keyword"]
            if rule["pattern_type"] not in valid_pattern_types:
                raise ValidationError(
                    f"Rule {i}: Invalid pattern_type. Must be one of: {', '.join(valid_pattern_types)}"
                )
