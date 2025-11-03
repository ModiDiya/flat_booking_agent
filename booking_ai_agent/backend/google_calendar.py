import os
import pickle
import csv
from datetime import datetime, timedelta, timezone
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# -----------------------------
# Configuration
# -----------------------------
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
TOKEN_FILE = "token.pickle"
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "credentials1.json")  # OAuth client JSON
BOOKINGS_FILE = os.path.join(os.path.dirname(__file__), "bookings.csv")  # Local booking record

# -----------------------------
# Google Calendar Service
# -----------------------------
def get_calendar_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)
    return service

# -----------------------------
# Fetch booked events for a day
# -----------------------------
def get_booked_slots(day):
    service = get_calendar_service()
    start_day = datetime.combine(day, datetime.min.time()).astimezone(timezone.utc)
    end_day = datetime.combine(day, datetime.max.time()).astimezone(timezone.utc)
    events_result = service.events().list(
        calendarId="primary",
        timeMin=start_day.isoformat(),
        timeMax=end_day.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute()
    booked_slots = []
    for event in events_result.get("items", []):
        start = datetime.fromisoformat(event['start'].get('dateTime')).astimezone(timezone.utc)
        end = datetime.fromisoformat(event['end'].get('dateTime')).astimezone(timezone.utc)
        booked_slots.append((start, end))
    return booked_slots

# -----------------------------
# Get available slots
# -----------------------------
def get_available_slots(day):
    booked_slots = get_booked_slots(day)
    slots = []
    start_time = datetime.combine(day, datetime.strptime("09:00", "%H:%M").time()).astimezone(timezone.utc)
    end_time = datetime.combine(day, datetime.strptime("17:00", "%H:%M").time()).astimezone(timezone.utc)
    delta = timedelta(minutes=30)

    while start_time + delta <= end_time:
        slot_start = start_time
        slot_end = start_time + delta
        # Check overlap
        overlap = False
        for booked_start, booked_end in booked_slots:
            if slot_start < booked_end and slot_end > booked_start:
                overlap = True
                break
        if not overlap:
            slots.append((slot_start, slot_end))
        start_time += delta
    return slots

# -----------------------------
# Create Event + Send Email
# -----------------------------
def create_event(summary, start_time, end_time, client_email, description="", recurring=False):
    service = get_calendar_service()
    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_time.isoformat(), "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_time.isoformat(), "timeZone": "Asia/Kolkata"},
        "attendees": [{"email": client_email}],
    }
    if recurring:
        event["recurrence"] = ["RRULE:FREQ=WEEKLY;COUNT=10"]  # Example: weekly 10 times

    created_event = service.events().insert(
        calendarId="primary",
        body=event,
        sendUpdates="all"
    ).execute()

    # Save locally
    save_booking(client_email, start_time, end_time, description)

    return created_event.get("htmlLink")

# -----------------------------
# Save booking locally
# -----------------------------
def save_booking(email, start_time, end_time, description):
    file_exists = os.path.exists(BOOKINGS_FILE)
    with open(BOOKINGS_FILE, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Email", "Start Time", "End Time", "Description"])
        writer.writerow([email, start_time.isoformat(), end_time.isoformat(), description])

# -----------------------------
# Main Booking Flow
# -----------------------------
def main():
    print("📌 Welcome to the AI Appointment Booking System!")
    client_email = input("Enter your email: ")

    # Select date
    while True:
        date_str = input("Enter appointment date (YYYY-MM-DD): ")
        try:
            selected_day = datetime.strptime(date_str, "%Y-%m-%d").date()
            if selected_day < datetime.now().date():
                print("❌ Date must be today or in the future.")
                continue
            break
        except ValueError:
            print("❌ Invalid date format. Try again.")

    # Show available slots
    available_slots = get_available_slots(selected_day)
    if not available_slots:
        print("❌ No slots available for this date.")
        return

    print("\n📅 Available Slots:")
    for i, (start, end) in enumerate(available_slots, 1):
        start_local = start.astimezone(timezone(timedelta(hours=5, minutes=30)))
        end_local = end.astimezone(timezone(timedelta(hours=5, minutes=30)))
        print(f"{i}. {start_local.strftime('%H:%M')} - {end_local.strftime('%H:%M')}")

    while True:
        try:
            choice = int(input("Select a slot number to book: ")) - 1
            if 0 <= choice < len(available_slots):
                break
            else:
                print("❌ Invalid choice.")
        except ValueError:
            print("❌ Enter a number.")

    start_time, end_time = available_slots[choice]

    description = input("Enter a description or note for this appointment: ")

    recurring_input = input("Do you want this appointment to be recurring weekly? (y/n): ").lower()
    recurring = recurring_input == "y"

    # Create event
    event_link = create_event(
        summary="Real Estate Consultation",
        start_time=start_time,
        end_time=end_time,
        client_email=client_email,
        description=description,
        recurring=recurring
    )

    print("✅ Event created! Client will receive email:", event_link)

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    main()
