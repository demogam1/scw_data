
````markdown
# 🔐 Scaleway Security Group Rule Exporter

A Python tool that connects to your **Scaleway account**, retrieves all **security groups and their rules**, and exports the data into a structured **Excel file** — with one worksheet per security group for clarity and simplicity.

---

## 📦 Features

- ✅ Validates that **Scaleway CLI** is installed and initialized
- ✅ Lists all security groups for your account
- ✅ Retrieves all **inbound/outbound rules** for each group
- ✅ Exports data to an Excel file: `security_group_rules.xlsx`
- ✅ Creates one **sheet per security group**

---

## 🧰 Requirements

- Python **3.7+**
- Scaleway CLI (`scw`) installed and initialized
- Python packages:
  ```bash
  pip install pandas openpyxl
````

---

## 🧱 Installation

### 1. Install Scaleway CLI

👉 Official install guide: [Scaleway CLI Docs](https://www.scaleway.com/en/docs/cli/install/)

Or run:

```bash
curl -sL https://install.scaleway.com | bash
```

### 2. Authenticate with Scaleway

```bash
scw init
```

You’ll be prompted for:

* Access key
* Secret key
* Project ID
* Region/zone

Then confirm everything is correctly configured:

```bash
scw info
```

You must **not** see any `-` values for:

* `access_key`
* `secret_key`
* `default_project_id`
* `default_organization_id`

---

## 🚀 Usage

Run the script from the root of the project:

```bash
python export_sg_rules.py
```

If the CLI is properly initialized and permissions are correct, the script will generate:

```
✅ Exported to: /absolute/path/security_group_rules.xlsx
```

---

## 📁 Output

### 🔸 File: `security_group_rules.xlsx`

* Each **worksheet = 1 security group**
* Columns included:

  * `ID`
  * `Direction`
  * `Protocol`
  * `Action`
  * `IP Range`
  * `Port From`
  * `Port To`

Perfect for auditing, documentation, or visual review.

---

## ❌ Troubleshooting

| Issue                    | Fix                                |
| ------------------------ | ---------------------------------- |
| `scw: command not found` | Install Scaleway CLI               |
| `Missing credentials`    | Run `scw init` again               |
| Excel file not created   | Check for permission or CLI errors |

---

## 🧹 Cleanup

Remove the generated file:

```bash
rm security_group_rules.xlsx
```

---

## 🪪 Adrasys
