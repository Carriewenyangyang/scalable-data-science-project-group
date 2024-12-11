import re
import csv
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Authenticate using the service account key
SERVICE_ACCOUNT_FILE = "scalable-data-science-project-4beb91edbff3.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Drive API service
service = build("drive", "v3", credentials=creds)

# file names
yaml_file_name = "client"
data_file_name = "packet"

# List files in the root folder
results = service.files().list(
    pageSize=1000, fields="files(id, name)"
).execute()

files = results.get("files", [])

client_files = {}
packet_files = {}

# Regex patterns for extracting numbers
client_pattern = re.compile(r"client-(\d+)\.yaml")
packet_pattern = re.compile(r"packet-(\d+)\.zip")

# Categorize files by type and number
for file in files:
    print(f"{file['name']} ({file['id']})")
    client_match = client_pattern.match(file["name"])
    packet_match = packet_pattern.match(file["name"])
    
    if client_match:
        number = int(client_match.group(1))
        client_files[number] = file["id"]
    elif packet_match:
        number = int(packet_match.group(1))
        packet_files[number] = file["id"]

# Combine data into rows for the CSV
rows = []
for number in sorted(set(client_files.keys()).union(packet_files.keys())):
    client_id = client_files.get(number, "")
    packet_id = packet_files.get(number, "")
    rows.append({"Number": number, "Packet_id": packet_id, "Client_id": client_id})

# Write to a CSV file
csv_file = "file_mapping.csv"
with open(csv_file, mode="w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Number", "Packet_id", "Client_id"])
    writer.writeheader()
    writer.writerows(rows)

print(f"File mapping saved to {csv_file}")