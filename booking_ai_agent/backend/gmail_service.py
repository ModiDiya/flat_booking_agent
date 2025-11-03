from google.oauth2 import service_account
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
from config import GOOGLE_CREDENTIALS_FILE

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def send_email(to: str, subject: str, body: str) -> str:
    """
    Sends an email using Gmail API via a service account.

    Args:
        to (str): Recipient email address
        subject (str): Email subject
        body (str): Email body content

    Returns:
        str: Success message with email ID or error message
    """
    try:
        # Load credentials
        creds = service_account.Credentials.from_service_account_file(
            GOOGLE_CREDENTIALS_FILE, scopes=SCOPES
        )

        # Build Gmail service
        service = build("gmail", "v1", credentials=creds)

        # Create MIME message
        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Send email
        sent_message = service.users().messages().send(
            userId="me", body={"raw": raw_message}
        ).execute()

        return f"Email sent successfully, ID: {sent_message.get('id')}"

    except FileNotFoundError:
        return "Error: Google credentials file not found."
    except Exception as e:
        return f"Error sending email: {str(e)}"
