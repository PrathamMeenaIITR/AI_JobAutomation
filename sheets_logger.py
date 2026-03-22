import subprocess, json, os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime

def get_bw_item(item_name):
    """Fetch a vault item from Bitwarden by name"""
    session = os.getenv("BW_SESSION")
    if not session:
        raise RuntimeError("BW_SESSION not set. Run 'bw unlock' and export the session key.")
    result = subprocess.run(
        ["bw", "get", "item", item_name, "--session", session],
        capture_output=True, text=True, check=True, timeout=10
    )
    return json.loads(result.stdout)

# --- Fetch Google Sheets credentials and Sheet ID from Bitwarden ---
# Vault item "GoogleSheets" should contain:
#   - Secure note: full JSON of credentials.json
#   - Custom field: "SHEET_ID" with your sheet ID
google_item = get_bw_item("GoogleSheets")

# Parse credentials.json from secure note
credentials_json = google_item["notes"]
with open("temp_credentials.json", "w") as f:
    f.write(credentials_json)

# Extract Sheet ID from custom field
sheet_id = None
for field in google_item.get("fields", []):
    if field["name"] == "SHEET_ID":
        sheet_id = field["value"]

def log_application(job_title, job_url, status, company="N/A",
                    match_percent=0, missingSkills="", matchedSkills="", notes=""):

    creds = service_account.Credentials.from_service_account_file(
        "temp_credentials.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        company,
        job_title,
        job_url,
        status,
        match_percent,
        missingSkills,
        matchedSkills,
        notes
    ]
    sheet.values().append(
        spreadsheetId=sheet_id,
        range="Sheet1!A:I",   # <-- 9 columns now
        valueInputOption="RAW",
        body={"values": [row]}
    ).execute()
