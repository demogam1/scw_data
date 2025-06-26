import subprocess
import shutil
import pandas as pd
import json
import sys
from pathlib import Path
import re

def check_requirements():
    if not shutil.which("scw"):
        print("❌ Scaleway CLI (scw) is not installed.")
        sys.exit(1)

    try:
        result = subprocess.run(["scw", "info"], capture_output=True, text=True, check=True)
        output = result.stdout

        required_keys = [
            "access_key", "secret_key",
            "default_project_id", "default_organization_id"
        ]
        missing = [key for key in required_keys if re.search(rf"^{key}\s+-\s+", output, re.MULTILINE)]

        if missing:
            print(f"❌ Missing credentials in `scw init`: {', '.join(missing)}")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print("❌ Failed to run `scw info`.")
        sys.exit(1)

def get_security_groups():
    result = subprocess.run(["scw", "instance", "security-group", "list", "-o", "json"],
                            capture_output=True, text=True)
    return json.loads(result.stdout)

def get_rules_for_group(group_id):
    result = subprocess.run(
        ["scw", "instance", "security-group", "list-rules", f"security-group-id={group_id}", "-o", "json"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

def get_servers():
    result = subprocess.run(["scw", "instance", "server", "list", "-o", "json"],
                            capture_output=True, text=True)
    return json.loads(result.stdout)

def export_security_groups_to_excel(groups_data, writer):
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

        sheet_name = group_name[:31]  # Excel limit
        df.to_excel(writer, sheet_name=sheet_name, index=False)

def export_servers_to_excel(servers_data, writer):
    export_rows = []

    for srv in servers_data:
        public_ips = srv.get("public_ips", [])
        ipv4 = next((ip["address"] for ip in public_ips if ip.get("family") == "inet"), "")
        ipv6 = next((ip["address"] for ip in public_ips if ip.get("family") == "inet6"), "")

        export_rows.append({
            "ID": srv.get("id"),
            "Name": srv.get("name"),
            "State": srv.get("state"),
            "Zone": srv.get("zone"),
            "Type": srv.get("commercial_type"),
            "IPv4": ipv4,
            "IPv6": ipv6,
            "Created At": srv.get("creation_date"),
            "Image": srv.get("image", {}).get("name"),
            "Security Group": srv.get("security_group", {}).get("name"),
        })

    df = pd.DataFrame(export_rows)
    df.to_excel(writer, sheet_name="Servers", index=False)

def export_to_json(data, filename):
    # Enrichissement pour les serveurs
    if filename == "servers.json":
        for srv in data:
            public_ips = srv.get("public_ips", [])
            srv["ipv4"] = next((ip["address"] for ip in public_ips if ip.get("family") == "inet"), "")
            srv["ipv6"] = next((ip["address"] for ip in public_ips if ip.get("family") == "inet6"), "")

    output_path = Path(filename)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"✅ JSON exported to: {output_path.resolve()}")

def export_selected_data(output_excel, output_json, export_sg, export_sv):
    if output_excel:
        writer = pd.ExcelWriter("scaleway_export.xlsx", engine="openpyxl")
    
    if export_sg:
        security_groups = get_security_groups()
        if output_excel:
            export_security_groups_to_excel(security_groups, writer)
        if output_json:
            export_to_json(security_groups, "security_groups.json")
    
    if export_sv:
        servers = get_servers()
        if output_excel:
            export_servers_to_excel(servers, writer)
        if output_json:
            export_to_json(servers, "servers.json")

    if output_excel:
        writer.close()
        print(f"✅ Excel exported to: {Path('scaleway_export.xlsx').resolve()}")

def prompt_user():
    print("What do you want to export?")
    print("1. Security Groups")
    print("2. Servers")
    print("3. Both")
    choice = input("Enter choice [1/2/3]: ").strip()

    export_sg = choice in ("1", "3")
    export_sv = choice in ("2", "3")

    print("\nChoose output format:")
    print("1. Excel")
    print("2. JSON")
    print("3. Both")
    fmt = input("Enter format [1/2/3]: ").strip()

    output_excel = fmt in ("1", "3")
    output_json = fmt in ("2", "3")

    return output_excel, output_json, export_sg, export_sv

def main():
    check_requirements()
    output_excel, output_json, export_sg, export_sv = prompt_user()
    export_selected_data(output_excel, output_json, export_sg, export_sv)

if __name__ == "__main__":
    main()
