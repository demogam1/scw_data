---
# 🔐 Scaleway Exporter — Security Groups & Servers

This Python script connects to your **Scaleway account**, retrieves **security groups** and/or **instance servers**, and exports the data in **Excel and/or JSON format** — depending on your choice.

---

## 📦 Features

- ✅ Checks if **Scaleway CLI** is installed and initialized
- ✅ Lets you choose what to export:
  - 🔹 Security Groups (with rules)
  - 🔹 Servers
  - 🔹 Both
- ✅ Lets you choose output format(s):
  - 📊 Excel (`.xlsx`)
  - 🧾 JSON (`.json`)
- ✅ Clean Excel structure:
  - One sheet per security group
  - One sheet for all servers
- ✅ Easy to run, no config file needed

---

## 🧰 Requirements

- Python **3.7+**
- Scaleway CLI (`scw`) installed and configured
- Python dependencies -> requirements.txt

---

## ⚙️ Setup

### 1. Install Scaleway CLI

[Official Guide →](https://cli.scaleway.com/)

Or via terminal:

```bash
curl -s https://raw.githubusercontent.com/scaleway/scaleway-cli/master/scripts/get.sh | sh
```

### 2. Initialize the CLI

```bash
scw init
```

You will need the following credentials to set up the Scaleway CLI:

- access_key
- secret_key
- default_organization_id


---

## 🚀 Usage

Simply run the script:

```bash
python export_scaleway_data.py
```

You’ll be prompted to choose:

1. What you want to export:

   ```
   1. Security Groups
   2. Servers
   3. Both
   ```

2. In which format:

   ```
   1. Excel
   2. JSON
   3. Both
   ```

### 📂 Example output files:

* `scaleway_export.xlsx`
* `security_groups.json`
* `servers.json`

---

## 📁 Excel Export Format

### 🔹 Security Group Sheets

Each security group gets its **own sheet** with the following columns:

| ID | Direction | Protocol | Action | IP Range | Port From | Port To |
| -- | --------- | -------- | ------ | -------- | --------- | ------- |

### 🔹 Servers Sheet

One sheet named **"Servers"** with raw server details (all fields from the API).

---

## ❌ Troubleshooting

| Problem                      | Solution                                 |
| ---------------------------- | ---------------------------------------- |
| `scw: command not found`     | Install the Scaleway CLI                 |
| `Missing credentials` error  | Run `scw init` again                     |
| Empty Excel/JSON             | Check if resources exist                 |
| `Permission denied` on write | Try running as sudo or in another folder |

---

## 🧹 Cleanup

To remove generated files:

```bash
rm *.json scaleway_export.xlsx
```

---

## 🪪 Adrasys
