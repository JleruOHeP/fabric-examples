import requests
from azure.identity import DefaultAzureCredential

workspace_id = "8079997d-da47-4f69-8fcd-d52baa4dddd6"

# ------------------------------------------
# Step 1: Authenticate with Fabric API
# ------------------------------------------
credential = DefaultAzureCredential()
token = credential.get_token("https://api.fabric.microsoft.com/.default")
headers = {
    "Authorization": f"Bearer {token.token}",
    "Content-Type": "application/json"
}

# ------------------------------------------
# Step 2: List all items in workspace
# ------------------------------------------
list_url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/items"

resp = requests.get(list_url, headers=headers)
if resp.status_code != 200:
    print(f"Failed to list items. HTTP {resp.status_code}: {resp.text}")
    exit(1)

items = resp.json().get("value", [])

# ------------------------------------------
# Step 3: Find item ID by name
# ------------------------------------------
item_name = "silver_views"
notebook_item = next(
    (item for item in items if item["displayName"] == item_name and item["type"] == "Notebook"),
    None
)

if not notebook_item:
    print(f"Notebook '{item_name}' not found in workspace '{workspace_id}'")
    exit(1)

notebook_item_id = notebook_item["id"]
print(f"Found notebook: {notebook_item_id}")

# ------------------------------------------
# Step 4: Trigger notebook
# ------------------------------------------
trigger_url = (
    f"https://api.fabric.microsoft.com/v1/"
    f"workspaces/{workspace_id}/items/{notebook_item_id}/jobs/instances?jobType=RunNotebook"
)

trigger_resp = requests.post(trigger_url, headers=headers, json={})

print(f"🔄 Trigger status: {trigger_resp.status_code}")
print(f"🔍 Trigger response: {trigger_resp.text}")

if trigger_resp.status_code in (200, 202):
    try:
        run_info = trigger_resp.json()
        run_id = run_info.get("id") or run_info.get("runId")
        print(f"Notebook triggered successfully. Run ID: {run_id}")
    except requests.exceptions.JSONDecodeError:
        print("Trigger succeeded but response is not valid JSON.")
else:
    print(f"Failed to trigger. HTTP {trigger_resp.status_code}:")
    print(trigger_resp.text)