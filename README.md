Here's a clean and informative `README.md` for your security group export script:

---

````markdown
# 🔐 Scaleway Security Group Exporter

This Python script retrieves **Scaleway instance security groups and their rules**, then exports them into a structured **Excel file** — with **one sheet per security group** for clarity.

---

## 📦 Features

- ✅ Validates Scaleway CLI is installed and initialized
- ✅ Retrieves all security group IDs and names
- ✅ Fetches **all rules** per security group (inbound & outbound)
- ✅ Exports rules to `security_group_rules.xlsx`
- ✅ One Excel **sheet per security group**

---

## 🚀 Requirements

- Python 3.7+
- Scaleway CLI (`scw`) installed and configured via `scw init`
- Python packages:
  ```bash
  pip install pandas openpyxl
````

---

## 🛠 Setup

### 1. Install Scaleway CLI

Follow the instructions:
[https://www.scaleway.com/en/docs/cli/install/](https://www.scaleway.com/en/docs/cli/install/)

Or via script:

```bash
curl -sL https://install.scaleway.com | bash
```

### 2. Initialize CLI

```bash
scw init
```

Make sure it sets:

* `access_key`
* `secret_key`
* `default_project_id`
* `default_organization_id`

You can verify with:

```bash
scw info
```

---

## 📜 Usage

```bash
python export_sg_rules.py
```

If everything is configured correctly, you'll get:

```bash
✅ Exported to: /absolute/path/security_group_rules.xlsx
```

---

## 🧾 Output Format

* File: `security_group_rules.xlsx`
* Each **sheet** represents a single security group
* Columns include:

  * ID
  * Direction
  * Protocol
  * Action
  * IP Range
  * Port From
  * Port To

---

## 🧹 Cleanup (optional)

To remove old output:

```bash
rm security_group_rules.xlsx
```

---

## ❓ Troubleshooting

* ❌ **Missing `scw` command**:
  → Install the CLI via instructions above.

* ❌ **Missing credentials**:
  → Run `scw init` and ensure `scw info` shows your credentials properly.

---

## 📄 License

MIT

---

## 🤝 Contributions

PRs and suggestions welcome!

```

---

Let me know if you'd like a badge (`Made with Python`, etc.), Docker instructions, or a CLI wrapper (`argparse`) added to this project.
```
