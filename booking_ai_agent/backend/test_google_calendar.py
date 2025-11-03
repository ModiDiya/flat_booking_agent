from google.oauth2 import service_account
from googleapiclient.discovery import build
from config import GOOGLE_CREDENTIALS_FILE

# Load service account credentials
creds = service_account.Credentials.from_service_account_file(
    GOOGLE_CREDENTIALS_FILE,
    scopes=["https://www.googleapis.com/auth/calendar"]
)

# Build calendar service
service = build("calendar", "v3", credentials=creds)

# Get list of calendars
calendar_list = service.calendarList().list().execute()

print("✅ Connected to Google Calendar!")
for calendar in calendar_list["items"]:
    print(calendar["summary"])
