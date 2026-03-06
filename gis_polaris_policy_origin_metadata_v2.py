
# GIS Polaris | Policy Origin Metadata
# Updated Prototype with Enhanced Exception Criteria + View/Edit Exceptions

import streamlit as st
import json
import os
import uuid
import pandas as pd
from datetime import datetime, timezone
from filelock import FileLock

APP_TITLE = "GIS Polaris | Policy Origin Metadata"

DATA_FILE = "policy_catalog.json"
BACKUP_FILE = "policy_catalog_backup.json"
LOCK_FILE = "policy_catalog.lock"

PLATFORMS = ["AWS", "Azure", "Hashicorp Sentinel", "Wiz", "OPA"]
ENVIRONMENTS = ["DEV", "UAT", "PROD"]

APPROVAL_STATUS = ["Approved", "Denied", "Pending", "Audit"]
EXCEPTION_STATUS = ["Active", "Inactive"]

AUTHORIZED_USERS = {
    "admin",
    "platform_engineer",
    "security_architect",
    "policy_admin"
}

def now_utc():
    return datetime.now(timezone.utc).isoformat()

def generate_id():
    return str(uuid.uuid4())

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"policies": [], "exceptions": []}

def save_data(data):
    lock = FileLock(LOCK_FILE)
    with lock:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        with open(BACKUP_FILE, "w") as f:
            json.dump(data, f, indent=4)

def export_excel(data):
    policies_df = pd.DataFrame(data["policies"])
    exceptions_df = pd.DataFrame(data["exceptions"])

    file = "policy_catalog_export.xlsx"
    with pd.ExcelWriter(file) as writer:
        policies_df.to_excel(writer, sheet_name="Policies", index=False)
        exceptions_df.to_excel(writer, sheet_name="Exceptions", index=False)

    return file

def nucleus_logo():
    svg = '''
    <svg width="40" height="40" viewBox="0 0 100 100">
      <circle cx="50" cy="50" r="10" fill="#1f3c88"/>
      <ellipse cx="50" cy="50" rx="35" ry="15" stroke="#1f3c88" fill="none" stroke-width="3"/>
      <ellipse cx="50" cy="50" rx="15" ry="35" stroke="#1f3c88" fill="none" stroke-width="3"/>
      <ellipse cx="50" cy="50" rx="30" ry="30" stroke="#1f3c88" fill="none" stroke-width="3"/>
    </svg>
    '''
    return svg

def login():
    st.sidebar.header("User Authentication")
    username = st.sidebar.text_input("Username")

    if username:
        if username in AUTHORIZED_USERS:
            st.sidebar.success("Authorized")
            return username
        else:
            st.sidebar.error("Unauthorized User")
    return None

def main():
    st.set_page_config(page_title=APP_TITLE, layout="wide")

    st.markdown(
        f'<div style="display:flex;align-items:center;gap:12px;">{nucleus_logo()}'
        f'<span style="font-size:34px;font-weight:700;color:#1f3c88;">{APP_TITLE}</span></div>',
        unsafe_allow_html=True
    )

    user = login()
    if not user:
        st.warning("Enter an authorized username.")
        return

    data = load_data()

    menu = st.sidebar.selectbox(
        "Navigation",
        [
            "Initialize Policy",
            "View / Edit Policies",
            "Initialize Exception",
            "View / Edit Exceptions",
            "Export Reporting"
        ]
    )

    if menu == "Initialize Policy":

        st.header("Initialize Policy Origin Metadata")

        with st.form("policy_form"):

            policy_name = st.text_input("Cross-Platform Standardized Policy Name")

            platforms = st.multiselect(
                "Platform(s) for Release / Deployment Scope",
                PLATFORMS
            )

            environments = st.multiselect(
                "Designated Scope: Environment Tenant(s)",
                ENVIRONMENTS
            )

            owner = st.text_input("Business Owner")

            approval = st.selectbox("Approval Status", APPROVAL_STATUS)

            details = st.text_area(
                "Pertinent Business Detail (max 500 characters)",
                max_chars=500
            )

            submitted = st.form_submit_button("Initialize Policy")

            if submitted:

                policy = {
                    "policy_id": generate_id(),
                    "policy_name": policy_name,
                    "platforms": platforms,
                    "environment_scope": environments,
                    "business_owner": owner,
                    "approval_status": approval,
                    "details": details,
                    "authored_by": user,
                    "created_date": now_utc()
                }

                data["policies"].append(policy)
                save_data(data)

                st.success("Policy Initialized")
                st.json(policy)

    elif menu == "View / Edit Policies":

        if not data["policies"]:
            st.info("No policies available.")
            return

        policy_ids = [p["policy_id"] for p in data["policies"]]
        selected = st.selectbox("Select Policy", policy_ids)

        policy = next(p for p in data["policies"] if p["policy_id"] == selected)

        with st.form("edit_policy"):

            policy["policy_name"] = st.text_input(
                "Cross-Platform Standardized Policy Name",
                policy["policy_name"]
            )

            policy["platforms"] = st.multiselect(
                "Platform(s) for Release / Deployment Scope",
                PLATFORMS,
                default=policy["platforms"]
            )

            policy["environment_scope"] = st.multiselect(
                "Designated Scope: Environment Tenant(s)",
                ENVIRONMENTS,
                default=policy["environment_scope"]
            )

            policy["business_owner"] = st.text_input(
                "Business Owner",
                policy["business_owner"]
            )

            policy["approval_status"] = st.selectbox(
                "Approval Status",
                APPROVAL_STATUS,
                index=APPROVAL_STATUS.index(policy["approval_status"])
            )

            policy["details"] = st.text_area(
                "Pertinent Business Detail",
                policy["details"],
                max_chars=500
            )

            if st.form_submit_button("Update Policy"):

                policy["last_updated"] = now_utc()
                save_data(data)

                st.success("Policy Updated")

    elif menu == "Initialize Exception":

        st.header("Initialize Policy Exception")

        with st.form("exception_form"):

            workspace_alias = st.text_input("Workspace Alias")
            workspace_name = st.text_input("Workspace Name")

            platforms = st.multiselect(
                "Platform(s) for Release / Deployment Scope",
                PLATFORMS
            )

            environments = st.multiselect(
                "Designated Scope: Environment Tenant(s)",
                ENVIRONMENTS
            )

            business_owner = st.text_input("Business Owner")

            approval_status = st.selectbox("Approval Status", APPROVAL_STATUS)

            status = st.selectbox("Status", EXCEPTION_STATUS)

            init_date = st.date_input("Initialization Date")
            exp_date = st.date_input("Expiration Date")

            description = st.text_area("Description")

            inherited_by = st.text_area(
                "Inherited By (multiple filenames separated by commas)"
            )

            submitted = st.form_submit_button("Initialize Exception")

            if submitted:

                exception = {
                    "exception_id": generate_id(),
                    "workspace_alias": workspace_alias,
                    "workspace_name": workspace_name,
                    "platforms": platforms,
                    "environment_scope": environments,
                    "business_owner": business_owner,
                    "approval_status": approval_status,
                    "status": status,
                    "initialization_date": str(init_date),
                    "expiration_date": str(exp_date),
                    "description": description,
                    "inherited_by": [x.strip() for x in inherited_by.split(",") if x],
                    "authored_by": user,
                    "created_date": now_utc()
                }

                data["exceptions"].append(exception)
                save_data(data)

                st.success("Exception Metadata Captured")
                st.json(exception)

    elif menu == "View / Edit Exceptions":

        if not data["exceptions"]:
            st.info("No exceptions recorded.")
            return

        exception_ids = [e["exception_id"] for e in data["exceptions"]]
        selected = st.selectbox("Select Exception", exception_ids)

        exception = next(e for e in data["exceptions"] if e["exception_id"] == selected)

        with st.form("edit_exception"):

            exception["workspace_alias"] = st.text_input(
                "Workspace Alias",
                exception["workspace_alias"]
            )

            exception["workspace_name"] = st.text_input(
                "Workspace Name",
                exception["workspace_name"]
            )

            exception["platforms"] = st.multiselect(
                "Platform(s) for Release / Deployment Scope",
                PLATFORMS,
                default=exception.get("platforms", [])
            )

            exception["environment_scope"] = st.multiselect(
                "Designated Scope: Environment Tenant(s)",
                ENVIRONMENTS,
                default=exception.get("environment_scope", [])
            )

            exception["business_owner"] = st.text_input(
                "Business Owner",
                exception.get("business_owner", "")
            )

            exception["approval_status"] = st.selectbox(
                "Approval Status",
                APPROVAL_STATUS,
                index=APPROVAL_STATUS.index(exception.get("approval_status","Pending"))
            )

            exception["status"] = st.selectbox(
                "Status",
                EXCEPTION_STATUS,
                index=EXCEPTION_STATUS.index(exception["status"])
            )

            exception["initialization_date"] = st.text_input(
                "Initialization Date",
                exception["initialization_date"]
            )

            exception["expiration_date"] = st.text_input(
                "Expiration Date",
                exception["expiration_date"]
            )

            exception["description"] = st.text_area(
                "Description",
                exception["description"]
            )

            inherited = ",".join(exception.get("inherited_by", []))

            new_inherited = st.text_area(
                "Inherited By (comma separated filenames)",
                inherited
            )

            if st.form_submit_button("Update Exception"):

                exception["inherited_by"] = [
                    x.strip() for x in new_inherited.split(",") if x
                ]

                exception["last_updated"] = now_utc()

                save_data(data)

                st.success("Exception Updated")

    elif menu == "Export Reporting":

        st.header("Export Executive Report")

        if st.button("Export Excel Report"):

            file = export_excel(data)

            with open(file, "rb") as f:
                st.download_button(
                    label="Download Excel Report",
                    data=f,
                    file_name=file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        st.subheader("JSON System of Record")
        st.json(data)


if __name__ == "__main__":
    main()
