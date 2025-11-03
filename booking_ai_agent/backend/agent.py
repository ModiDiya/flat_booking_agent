import os
import datetime
import dateparser
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ---------------------------
# Load environment variables
# ---------------------------
load_dotenv()
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")

# ---------------------------
# Google Calendar Setup
# ---------------------------
SCOPES = ["https://www.googleapis.com/auth/calendar"]
credentials = service_account.Credentials.from_service_account_file(
    GOOGLE_CREDENTIALS_FILE, scopes=SCOPES
)
service = build("calendar", "v3", credentials=credentials)

# ---------------------------
# Add Event Function
# ---------------------------
def add_event(event_desc, recipient_email):
    # Parse natural language date/time with better settings
    event_datetime = dateparser.parse(
        event_desc,
        settings={
            "PREFER_DATES_FROM": "future",
            "RELATIVE_BASE": datetime.datetime.now(),
            "PREFER_DAY_OF_MONTH": "first",
        }
    )

    if not event_datetime:
        print("❌ Could not parse date/time from text.")
        return

    event = {
        "summary": event_desc.split(" at ")[0],  # Take description before "at"
        "start": {"dateTime": event_datetime.isoformat(), "timeZone": "Asia/Kolkata"},
        "end": {
            "dateTime": (event_datetime + datetime.timedelta(hours=1)).isoformat(),
            "timeZone": "Asia/Kolkata",
        },
        "attendees": [{"email": recipient_email}],
    }

    event = service.events().insert(calendarId="primary", body=event).execute()
    print(f"✅ Event created: {event.get('htmlLink')}")

# ---------------------------
# Show Upcoming Events
# ---------------------------
def show_events():
    now = datetime.datetime.utcnow().isoformat() + "Z"
    events_result = service.events().list(
        calendarId="primary", timeMin=now, maxResults=10, singleEvents=True, orderBy="startTime"
    ).execute()
    events = events_result.get("items", [])

    print("\n📌 Upcoming events:")
    if not events:
        print("No upcoming events found.")
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(f" - {event['summary']} at {start}")

# ---------------------------
# Main CLI Loop
# ---------------------------
if __name__ == "__main__":
    print(">>")
    print("📌 Welcome to Google Calendar Agent")
    print("👉 Type your event and recipient email in this format:")
    print("   <event description> | <recipient_email>\n")

    user_input = input("Enter event & email: ").strip()

    if "|" in user_input:
        event_desc, recipient_email = [part.strip() for part in user_input.split("|", 1)]
        add_event(event_desc, recipient_email)
    else:
        print("❌ Invalid format. Use: <event description> | <recipient_email>")

    show_events()
