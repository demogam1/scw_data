#!/usr/bin/env python3

import subprocess
import json
import os
import sys
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def validate_environment():
    """
    Validate that all required environment variables are present
    """
    required_vars = [
        'SCW_ACCESS_KEY',
        'SCW_SECRET_KEY',
        'SCW_DEFAULT_PROJECT_ID',
        'SCW_DEFAULT_REGION',
        'SCW_DEFAULT_ORGANIZATION_ID'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"- {var}")
        print("\nPlease ensure these variables are set in your .env file")
        sys.exit(1)

def run_scw_command(command: List[str]) -> Dict:
    """
    Execute a Scaleway CLI command and return the JSON output
    """
    # Add environment variables to the command
    env = os.environ.copy()
    env.update({
        'SCW_ACCESS_KEY': os.getenv('SCW_ACCESS_KEY', ''),
        'SCW_SECRET_KEY': os.getenv('SCW_SECRET_KEY', ''),
        'SCW_DEFAULT_PROJECT_ID': os.getenv('SCW_DEFAULT_PROJECT_ID', ''),
        'SCW_DEFAULT_REGION': os.getenv('SCW_DEFAULT_REGION', ''),
        'SCW_DEFAULT_ORGANIZATION_ID': os.getenv('SCW_DEFAULT_ORGANIZATION_ID', '')
    })

    try:
        # Add the --output json flag to ensure JSON output
        if '-o' not in command and '--output' not in command:
            command.extend(['--output', 'json'])
            
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            env=env
        )
        
        # Handle empty output
        if not result.stdout.strip():
            return {}
            
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error output: {e.stderr}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON output: {e}")
        print(f"Raw output: {result.stdout}")
        return {}

def get_instances() -> List[Dict]:
    """
    Get all instances information
    """
    return run_scw_command([
        "scw", "instance", "server", "list",
        "--region", os.getenv('SCW_DEFAULT_REGION', ''),
        "--project-id", os.getenv('SCW_DEFAULT_PROJECT_ID', '')
    ])

def get_security_groups() -> List[Dict]:
    """
    Get all security groups information
    """
    return run_scw_command([
        "scw", "instance", "security-group", "list",
        "--region", os.getenv('SCW_DEFAULT_REGION', ''),
        "--project-id", os.getenv('SCW_DEFAULT_PROJECT_ID', '')
    ])

def main():
    # Validate environment variables first
    validate_environment()
    
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