import subprocess
import json
import shutil
import pandas as pd
import sys
from pathlib import Path

def check_requirements():
    # Check if 'scw' CLI is installed
    if not shutil.which("scw"):
        print("❌ Scaleway CLI (scw) is not installed.")
        sys.exit(1)
    
    # Check if user is authenticated (by running a harmless command)
    try:
        subprocess.run(["scw", "whoami"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("❌ Scaleway CLI is not initialized. Run `scw init` first.")
        sys.exit(1)

def get_security_groups():
    result = subprocess.run(["scw", "instance", "security-group", "list", "-o", "json"], capture_output=True, text=True)
    return json.loads(result.stdout)

def get_rules_for_group(group_id):
    result = subprocess.run(
        ["scw", "instance", "security-group", "list-rules", f"security-group-id={group_id}", "-o", "json"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

def export_to_excel(groups_data):
    output_path = Path("security_group_rules.xlsx")
    writer = pd.ExcelWriter(output_path, engine="openpyxl")

    for group in groups_data:
        group_name = group["name"] or group["id"]
        group_id = group["id"]

        rules = get_rules_for_group(group_id)
        if not rules:
            continue

        df = pd.DataFrame(rules)
        df.rename(columns={
            "id": "ID",
            "direction": "Direction",
            "protocol": "Protocol",
            "action": "Action",
            "ip_range": "IP Range",
            "dest_port_from": "Port From",
            "dest_port_to": "Port To"
        }, inplace=True)

        # Truncate long sheet names (Excel limit: 31 chars)
        safe_name = group_name[:31]
        df.to_excel(writer, sheet_name=safe_name, index=False)

    writer.close()
    print(f"✅ Exported to: {output_path.absolute()}")

def main():
    check_requirements()
    groups = get_security_groups()
    export_to_excel(groups)

if __name__ == "__main__":
    main()