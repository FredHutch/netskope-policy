"""
Policy Management Module
Handles creation, update, and management of Netskope policies
"""

from typing import Dict, Any, List, Optional
from .exceptions import PolicyNotFoundError, ValidationError


class PolicyManager:
    """
    Manages Netskope real-time protection policies

    Handles:
    - Web policies
    - Cloud app policies
    - URL lists
    - Policy profiles
    """

    def __init__(self, client):
        """
        Initialize PolicyManager

        Args:
            client: NetskopeClient instance
        """
        self.client = client

    def list_policies(
        self,
        policy_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        List all policies

        Args:
            policy_type: Filter by policy type (e.g., 'web', 'cloudapp', 'dlp')
            limit: Maximum number of results
            offset: Offset for pagination

        Returns:
            List of policies
        """
        params = {
            "limit": limit,
            "offset": offset
        }

        if policy_type:
            params["type"] = policy_type

        response = self.client.get("/policy", params=params)
        return response.get("data", [])

    def get_policy(self, policy_id: str) -> Dict[str, Any]:
        """
        Get a specific policy by ID

        Args:
            policy_id: Policy identifier

        Returns:
            Policy details
        """
        try:
            response = self.client.get(f"/policy/{policy_id}")
            return response.get("data", {})
        except Exception as e:
            raise PolicyNotFoundError(f"Policy {policy_id} not found: {str(e)}")

    def create_policy(self, policy_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new policy

        Args:
            policy_data: Policy configuration

        Returns:
            Created policy details
        """
        self._validate_policy_data(policy_data)

        response = self.client.post("/policy", data=policy_data)
        return response.get("data", {})

    def update_policy(
        self,
        policy_id: str,
        policy_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing policy

        Args:
            policy_id: Policy identifier
            policy_data: Updated policy configuration

        Returns:
            Updated policy details
        """
        self._validate_policy_data(policy_data)

        response = self.client.put(f"/policy/{policy_id}", data=policy_data)
        return response.get("data", {})

    def delete_policy(self, policy_id: str) -> bool:
        """
        Delete a policy

        Args:
            policy_id: Policy identifier

        Returns:
            True if successful
        """
        self.client.delete(f"/policy/{policy_id}")
        return True

    def enable_policy(self, policy_id: str) -> Dict[str, Any]:
        """
        Enable a policy

        Args:
            policy_id: Policy identifier

        Returns:
            Updated policy details
        """
        return self.update_policy(policy_id, {"enabled": True})

    def disable_policy(self, policy_id: str) -> Dict[str, Any]:
        """
        Disable a policy

        Args:
            policy_id: Policy identifier

        Returns:
            Updated policy details
        """
        return self.update_policy(policy_id, {"enabled": False})

    def create_url_list(
        self,
        name: str,
        urls: List[str],
        list_type: str = "exact",
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a URL list for policy use

        Args:
            name: Name of the URL list
            urls: List of URLs
            list_type: Type of list ('exact', 'regex', 'category')
            description: Optional description

        Returns:
            Created URL list details
        """
        data = {
            "name": name,
            "urls": urls,
            "type": list_type
        }

        if description:
            data["description"] = description

        response = self.client.post("/policy/urllist", data=data)
        return response.get("data", {})

    def get_url_lists(self) -> List[Dict[str, Any]]:
        """
        Get all URL lists

        Returns:
            List of URL lists
        """
        response = self.client.get("/policy/urllist")
        return response.get("data", [])

    def update_url_list(
        self,
        list_id: str,
        urls: Optional[List[str]] = None,
        name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update a URL list

        Args:
            list_id: URL list identifier
            urls: Updated list of URLs
            name: Updated name

        Returns:
            Updated URL list details
        """
        data = {}
        if urls is not None:
            data["urls"] = urls
        if name is not None:
            data["name"] = name

        response = self.client.put(f"/policy/urllist/{list_id}", data=data)
        return response.get("data", {})

    def delete_url_list(self, list_id: str) -> bool:
        """
        Delete a URL list

        Args:
            list_id: URL list identifier

        Returns:
            True if successful
        """
        self.client.delete(f"/policy/urllist/{list_id}")
        return True

    def create_web_policy(
        self,
        name: str,
        action: str,
        categories: Optional[List[str]] = None,
        url_lists: Optional[List[str]] = None,
        user_groups: Optional[List[str]] = None,
        enabled: bool = True
    ) -> Dict[str, Any]:
        """
        Create a web filtering policy

        Args:
            name: Policy name
            action: Action to take ('allow', 'block', 'alert')
            categories: Web categories to apply policy to
            url_lists: URL list IDs to apply policy to
            user_groups: User groups to apply policy to
            enabled: Whether policy is enabled

        Returns:
            Created policy details
        """
        policy_data = {
            "name": name,
            "type": "web",
            "action": action,
            "enabled": enabled,
            "rules": []
        }

        rule = {}
        if categories:
            rule["categories"] = categories
        if url_lists:
            rule["url_lists"] = url_lists
        if user_groups:
            rule["user_groups"] = user_groups

        if rule:
            policy_data["rules"].append(rule)

        return self.create_policy(policy_data)

    def create_cloud_app_policy(
        self,
        name: str,
        app_name: str,
        action: str,
        activities: Optional[List[str]] = None,
        user_groups: Optional[List[str]] = None,
        enabled: bool = True
    ) -> Dict[str, Any]:
        """
        Create a cloud app policy

        Args:
            name: Policy name
            app_name: Cloud application name (e.g., 'Box', 'Google Drive')
            action: Action to take ('allow', 'block', 'alert')
            activities: Activities to control (e.g., 'upload', 'download', 'share')
            user_groups: User groups to apply policy to
            enabled: Whether policy is enabled

        Returns:
            Created policy details
        """
        policy_data = {
            "name": name,
            "type": "cloudapp",
            "app": app_name,
            "action": action,
            "enabled": enabled,
            "rules": []
        }

        rule = {}
        if activities:
            rule["activities"] = activities
        if user_groups:
            rule["user_groups"] = user_groups

        if rule:
            policy_data["rules"].append(rule)

        return self.create_policy(policy_data)

    def _validate_policy_data(self, policy_data: Dict[str, Any]) -> None:
        """
        Validate policy data before creation/update

        Args:
            policy_data: Policy configuration to validate

        Raises:
            ValidationError: If validation fails
        """
        required_fields = ["name", "type"]

        for field in required_fields:
            if field not in policy_data:
                raise ValidationError(f"Missing required field: {field}")

        # Validate action if present
        if "action" in policy_data:
            valid_actions = ["allow", "block", "alert", "bypass"]
            if policy_data["action"] not in valid_actions:
                raise ValidationError(
                    f"Invalid action. Must be one of: {', '.join(valid_actions)}"
                )

        # Validate type
        valid_types = ["web", "cloudapp", "dlp", "malware", "threat"]
        if policy_data["type"] not in valid_types:
            raise ValidationError(
                f"Invalid policy type. Must be one of: {', '.join(valid_types)}"
            )
