#!/usr/bin/env python3
"""
BCM REST API Test Script

This script demonstrates how to interact with the NVIDIA Base Command Manager
REST API for querying categories, devices, and other cluster information.

Usage:
    python3 test_bcm_rest_api.py

Configuration:
    Edit the variables below to match your BCM server settings.
"""

import json
import sys
import urllib3
from typing import Dict, List, Any, Optional

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    import requests
except ImportError:
    print("ERROR: requests library not found. Install with: pip install requests")
    sys.exit(1)

# ============================================================================
# Configuration
# ============================================================================

BCM_HOST = "192.168.122.163"
BCM_PORT = 8081
BCM_USERNAME = "root"
BCM_PASSWORD = "redhat"
BCM_BASE_URL = f"https://{BCM_HOST}:{BCM_PORT}/rest/v1"

# ============================================================================
# API Client Class
# ============================================================================

class BCMRestClient:
    """Client for interacting with BCM REST API"""

    def __init__(self, host: str, port: int, username: str, password: str):
        """
        Initialize BCM REST API client

        Args:
            host: BCM server hostname or IP
            port: API port (usually 8081)
            username: Username for authentication
            password: Password for authentication
        """
        self.base_url = f"https://{host}:{port}/rest/v1"
        self.auth = (username, password)
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.verify = False  # Disable SSL verification for self-signed certs

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        """
        Make GET request to API

        Args:
            endpoint: API endpoint (e.g., '/category')
            params: Optional query parameters

        Returns:
            JSON response data
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()

            # Some endpoints return empty response
            if not response.text:
                return None

            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"ERROR: API request failed: {e}")
            return None

    def _post(self, endpoint: str, data: Dict) -> Any:
        """
        Make POST request to API

        Args:
            endpoint: API endpoint
            data: JSON data to send

        Returns:
            JSON response data
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()

            if not response.text:
                return None

            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"ERROR: API request failed: {e}")
            return None

    def get_endpoints(self) -> List[str]:
        """Get list of available API endpoints"""
        return self._get("")

    def get_categories(self) -> List[Dict]:
        """Get list of all categories"""
        return self._get("/category")

    def get_category(self, name: str) -> Optional[Dict]:
        """
        Get specific category by name

        Args:
            name: Category name

        Returns:
            Category data or None if not found
        """
        result = self._get("/category", params={"name": name})
        if result and len(result) > 0:
            return result[0]
        return None

    def get_devices(self) -> List[Dict]:
        """Get list of all devices/nodes"""
        return self._get("/device")

    def get_device(self, hostname: str) -> Optional[Dict]:
        """
        Get specific device by hostname

        Args:
            hostname: Device hostname

        Returns:
            Device data or None if not found
        """
        devices = self._get("/device", params={"hostname": hostname})
        if devices:
            for device in devices:
                if device.get("hostname") == hostname:
                    return device
        return None

    def get_power_operations(self) -> List[str]:
        """Get list of available power operations"""
        return self._get("/power")

    def get_network_endpoints(self) -> List[str]:
        """Get list of network-related endpoints"""
        return self._get("/network")

    def get_version(self) -> Any:
        """Get BCM version information"""
        return self._get("/version")


# ============================================================================
# Test Functions
# ============================================================================

def print_header(text: str):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def test_endpoints(client: BCMRestClient):
    """Test: List all available API endpoints"""
    print_header("Available API Endpoints")

    endpoints = client.get_endpoints()
    if endpoints:
        for endpoint in endpoints:
            print(f"  /rest/v1/{endpoint}")
    else:
        print("  ERROR: Could not retrieve endpoints")


def test_categories(client: BCMRestClient):
    """Test: Query categories"""
    print_header("Categories")

    categories = client.get_categories()
    if categories:
        for cat in categories:
            print(f"Category: {cat['name']}")
            print(f"  Software Image: {cat.get('image', 'N/A')}")
            print(f"  Nodes: {len(cat.get('nodes', []))}")
            if cat.get('nodes'):
                for node in cat['nodes']:
                    print(f"    - {node}")
            print()
    else:
        print("  ERROR: Could not retrieve categories")


def test_specific_category(client: BCMRestClient, name: str = "default"):
    """Test: Query specific category"""
    print_header(f"Category Details: {name}")

    category = client.get_category(name)
    if category:
        print(json.dumps(category, indent=2))
    else:
        print(f"  ERROR: Category '{name}' not found")


def test_devices(client: BCMRestClient):
    """Test: Query devices/nodes"""
    print_header("Devices/Nodes")

    devices = client.get_devices()
    if devices:
        for device in devices:
            print(f"Device: {device['hostname']}")
            print(f"  Type: {device.get('type', 'Unknown')}")
            print(f"  UUID: {device.get('uuid', 'N/A')}")
            print(f"  MAC: {device.get('mac', 'N/A')}")
            print(f"  IP: {device.get('ip', 'N/A')}")
            print(f"  Category: {device.get('category', 'N/A')}")
            print(f"  Network: {device.get('network', 'N/A')}")
            print(f"  Cluster: {device.get('cluster', 'N/A')}")

            roles = device.get('roles', [])
            if roles:
                print(f"  Roles: {', '.join(roles)}")
            print()
    else:
        print("  ERROR: Could not retrieve devices")


def test_specific_device(client: BCMRestClient, hostname: str = "node001"):
    """Test: Query specific device"""
    print_header(f"Device Details: {hostname}")

    device = client.get_device(hostname)
    if device:
        print(json.dumps(device, indent=2))
    else:
        print(f"  ERROR: Device '{hostname}' not found")


def test_power_operations(client: BCMRestClient):
    """Test: List power management operations"""
    print_header("Power Management Operations")

    operations = client.get_power_operations()
    if operations:
        print("Available operations:")
        for op in operations:
            print(f"  - {op}")
    else:
        print("  ERROR: Could not retrieve power operations")


def test_network(client: BCMRestClient):
    """Test: Network endpoints"""
    print_header("Network Endpoints")

    endpoints = client.get_network_endpoints()
    if endpoints:
        print("Available network endpoints:")
        for endpoint in endpoints:
            print(f"  - /rest/v1/network/{endpoint}")
    else:
        print("  ERROR: Could not retrieve network endpoints")


def test_version(client: BCMRestClient):
    """Test: Get BCM version"""
    print_header("BCM Version Information")

    version = client.get_version()
    if version:
        print(json.dumps(version, indent=2))
    else:
        print("  No version information available")


def test_device_category_mapping(client: BCMRestClient):
    """Test: Show device to category mapping"""
    print_header("Device to Category Mapping")

    devices = client.get_devices()
    categories = client.get_categories()

    if not devices or not categories:
        print("  ERROR: Could not retrieve data")
        return

    # Build category map
    cat_map = {}
    for cat in categories:
        cat_name = cat['name']
        cat_map[cat_name] = {
            'image': cat.get('image', 'N/A'),
            'devices': []
        }

    # Assign devices to categories
    for device in devices:
        cat_name = device.get('category')
        if cat_name and cat_name in cat_map:
            cat_map[cat_name]['devices'].append(device['hostname'])

    # Print mapping
    for cat_name, info in cat_map.items():
        print(f"Category: {cat_name}")
        print(f"  Software Image: {info['image']}")
        print(f"  Devices ({len(info['devices'])}):")
        if info['devices']:
            for dev in info['devices']:
                print(f"    - {dev}")
        else:
            print("    (none)")
        print()


# ============================================================================
# Main
# ============================================================================

def main():
    """Run all API tests"""
    print("\n" + "=" * 80)
    print("  BCM REST API Test Script")
    print(f"  Server: {BCM_HOST}:{BCM_PORT}")
    print("=" * 80)

    # Initialize client
    client = BCMRestClient(BCM_HOST, BCM_PORT, BCM_USERNAME, BCM_PASSWORD)

    # Run tests
    try:
        test_endpoints(client)
        test_version(client)
        test_categories(client)
        test_specific_category(client, "default")
        test_devices(client)
        test_device_category_mapping(client)
        test_power_operations(client)
        test_network(client)

        print_header("Testing Complete")
        print("All API tests completed successfully!\n")

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nERROR: Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
