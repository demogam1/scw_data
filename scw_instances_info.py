#!/usr/bin/env python3

import subprocess
import json
from typing import Dict, List

def run_scw_command(command: List[str]) -> Dict:
    """
    Execute a Scaleway CLI command and return the JSON output
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error output: {e.stderr}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON output: {e}")
        return {}

def get_instances() -> List[Dict]:
    """
    Get all instances information
    """
    return run_scw_command(["scw", "instance", "server", "list", "-o", "json"])

def get_security_groups() -> List[Dict]:
    """
    Get all security groups information
    """
    return run_scw_command(["scw", "instance", "security-group", "list", "-o", "json"])

def main():
    # Get instances
    instances = get_instances()
    if not instances:
        print("No instances found or error occurred")
        return

    # Get security groups
    security_groups = get_security_groups()
    if not security_groups:
        print("No security groups found or error occurred")
        return

    # Create a mapping of security group IDs to their rules
    security_group_rules = {
        sg["id"]: sg["rules"] for sg in security_groups
    }

    # Print information for each instance
    print("\nInstance Information:")
    print("-" * 50)
    
    for instance in instances:
        print(f"\nInstance Name: {instance.get('name', 'N/A')}")
        print(f"Instance ID: {instance.get('id', 'N/A')}")
        print(f"Status: {instance.get('state', 'N/A')}")
        
        # Get security group information
        security_group_id = instance.get("security_group", {}).get("id")
        if security_group_id and security_group_id in security_group_rules:
            print("\nFirewall Rules:")
            for rule in security_group_rules[security_group_id]:
                print(f"- Protocol: {rule.get('protocol', 'N/A')}")
                print(f"  Direction: {rule.get('direction', 'N/A')}")
                print(f"  Action: {rule.get('action', 'N/A')}")
                print(f"  IP Range: {rule.get('ip_range', 'N/A')}")
                print(f"  Port: {rule.get('dest_port_from', 'N/A')}-{rule.get('dest_port_to', 'N/A')}")
                print()
        else:
            print("No firewall rules found for this instance")
        
        print("-" * 50)

if __name__ == "__main__":
    main() 