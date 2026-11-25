import os
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = os.getenv("YOUTUBE_TOKEN_FILE", "token.json")

flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
credentials = flow.run_local_server(port=0)
with open(TOKEN_FILE, "w", encoding="utf-8") as f:
    f.write(credentials.to_json())
print(f"YouTube OAuth saved to {TOKEN_FILE}. Keep this file private!")
