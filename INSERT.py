import sqlite3
import json

filepath = "/app/langflow2/flows/Basic Prompting Custom copy.json"
DB_FILE = "/app/langflow2/langflow.db"
TABLE_NAME = "flow"

conn = sqlite3.connect(DB_FILE)
crsr = conn.cursor()

columns = [
    'name', 'description', 'icon_bg_color', 'gradient', 'is_component',
    'updated_at', 'webhook', 'endpoint_name', 'data', 'mcp_enabled',
    'action_name', 'action_description', 'access_type', 'id', 'user_id',
    'icon', 'tags', 'locked', 'folder_id', 'fs_path'
]

with open(filepath, "r") as f:
    record = json.load(f)

values = [json.dumps(record.get(col)) if col in ['data', 'tags'] else record.get(col) for col in columns]
placeholders = ', '.join('?' for _ in columns)
query = f"INSERT OR REPLACE INTO flow ({', '.join(columns)}) VALUES ({placeholders});"
crsr.execute(query,values)