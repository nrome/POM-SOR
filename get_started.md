# 🧭 GIS Polaris | Policy Origin Metadata for Platform Engineering

> A structured System of Record (SoR) for managing security policy metadata across cloud and infrastructure platforms.

---

## Table of Contents

- [What This Program Includes](#what-this-program-includes)
  - [Core System of Record Capabilities](#-core-system-of-record-capabilities)
  - [Controlled User Access](#-controlled-user-access)
  - [Data Persistence](#-data-persistence)
  - [Executive Reporting](#-executive-reporting)
  - [JSON API Output](#-json-api-output)
  - [Modern UI](#-modern-ui)
- [How to Run It](#how-to-run-it)
- [Dependencies](#-make-sure-dependencies-are-installed)
- [How JSON Files Are Reloaded](#how-do-you-reload-saved-json-files)
- [What Happens When the App Starts](#what-happens-when-the-app-starts)
- [Recovering From a Corrupted JSON File](#if-the-main-json-gets-corrupted)
- [Architecture Overview](#architecture-overview-sor-structure)

---

## What This Program Includes

### 🧭 Core System of Record Capabilities

The platform provides full lifecycle management of security policy definition metadata:

- **Create, update, and delete** security policy definition metadata
- **Automatic UUID** policy ID generation
- **Mandatory fields:**

| Field | Accepted Values |
|---|---|
| **Platform** | `AWS`, `Azure`, `Wiz`, `Hashicorp Sentinel`, `OPA` |
| **Environment** | `DEV`, `UAT`, `PROD` |
| **Standardized Policy Name** | Free text (standardized format) |
| **Business Owner** | Free text |
| **Business Detail** | Free text *(500 character limit)* |

---

### 👤 Controlled User Access

Only authorized usernames may interact with the system:

```
admin
platform_engineer
security_architect
policy_admin
```

> **Note:** You can easily expand this list to include additional authorized users.

---

### 🗂 Data Persistence

The system produces two JSON output files that serve as a lightweight, API-ready catalog for engineering teams:

| File | Purpose |
|---|---|
| `policy_catalog.json` | Primary system of record |
| `policy_catalog_backup.json` | Backup copy |

---

### 📊 Executive Reporting

One-click export generates a spreadsheet for leadership reporting and audit visibility:

```
policy_catalog_export.xlsx
```

---

### 🔌 JSON API Output

Each policy record produces the following structured JSON:

```json
{
  "policy_id": "uuid",
  "policy_name": "AWS-S3-Encryption-Required",
  "platform": "AWS",
  "environment": "PROD",
  "business_owner": "Cloud Security",
  "details": "All S3 buckets must enforce SSE encryption.",
  "created_by": "platform_engineer",
  "created_date": "timestamp"
}
```

Engineering teams can ingest this output into:

- CI/CD policy pipelines
- Sentinel / OPA evaluation engines
- Compliance automation
- Platform governance frameworks

---

### 🎨 Modern UI

The interface includes:

- Sidebar navigation
- Card-style UI layout
- Clean form-based workflows
- Embedded JSON viewers
- Interactive data tables
- Excel export download button

---

## How to Run It

**1. Install dependencies:**

```bash
pip install streamlit pandas openpyxl
```

**2. Run the app:**

```bash
streamlit run gis_polaris_platform_engineering.py
```

The UI will launch automatically in your browser or you can launch the URL:

```bash
http://localhost:8501
```
---

## 🧰 Make Sure Dependencies Are Installed

If needed, run:

```bash
pip install streamlit pandas openpyxl
```

---

## How Do You Reload Saved JSON Files?

The application **automatically loads JSON at startup**. This function runs when the program starts:

```python
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
```

---

## What Happens When the App Starts

1. The app looks for:
   ```
   policy_catalog.json
   ```

2. If the file exists:
   - All policies automatically load into memory

3. They appear inside:
   ```
   View / Edit Policies
   ```

> ✅ No manual reload is needed.

---

## If the Main JSON Gets Corrupted

You can restore using the backup file. Follow these steps:

**Step 1** — Delete the corrupted file:
```
policy_catalog.json
```

**Step 2** — Rename the backup file:
```
policy_catalog_backup.json  →  policy_catalog.json
```

**Step 3** — Restart the application.

> ✅ All policies will be restored.

---

## Architecture Overview (SoR Structure)

The JSON store holds two object collections:

```json
{
  "policies": [],
  "exceptions": []
}
```

### System Architecture

```
GIS Polaris | Policy Origin Metadata

    Policies
        ├─ policy_id
        ├─ platform scope
        ├─ environment scope
        └─ governance metadata

    Exceptions
        ├─ workspace metadata
        ├─ platform scope
        ├─ environment scope
        ├─ approval state
        └─ expiration tracking

    System of Record
        ├─ policy_catalog.json
        └─ policy_catalog_backup.json
```

---

*GIS Polaris | Policy Origin Metadata for Platform Engineering — Internal Documentation*
