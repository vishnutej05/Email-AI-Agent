import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request  # ✅ Correct
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from twilio.rest import Client
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Set your Gemini API key
genai.configure(api_key=os.getenv("YOUR_GEMINI_API_KEY")) 
# print(os.getenv("YOUR_GEMINI_API_KEY"))

# models = list(genai.list_models())
# print(models)

# Load environment variables
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_FROM")
TWILIO_TO = os.getenv("TWILIO_TO")

# Gmail API setup
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def fetch_unread_emails(service):
    """Fetch unread emails from the Gmail inbox."""
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    messages = results.get('messages', [])
    emails = []

    for msg in messages[:5]:  # Limit to the latest 5 unread emails
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        for part in msg_data['payload'].get('headers', []):
            if part['name'] == 'Subject':
                subject = part['value']
        snippet = msg_data.get('snippet', '')
        emails.append(f"Subject: {subject}\nSnippet: {snippet}")

    return "\n\n".join(emails)

def summarize_emails(emails):
    model = genai.GenerativeModel("gemini-2.0-flash-lite")

    # Combine emails into a single string
    combined_text = "\n\n".join(emails)

    # Define the prompt with a more concise instruction
    prompt = f"""
    Summarize the following emails in 2-3 minimal to concise points per email. Provide the most important information, focusing on the main subject and key details. Avoid excessive details. And good presentation is important.

    Emails:
    {combined_text}
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error during summarization: {e}"

def send_to_whatsapp(message):
    """Send the message via WhatsApp using Twilio."""
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    msg = client.messages.create(
        from_=TWILIO_FROM,
        body=message,
        to=TWILIO_TO
    )
    return msg.sid

def run_agent():
    """Run the full agent to fetch emails, summarize, and send to WhatsApp."""
    print("🔐 Authenticating Gmail...")
    gmail_service = authenticate_gmail()

    print("📥 Fetching emails...")
    raw_emails = fetch_unread_emails(gmail_service)

    print("🧠 Summarizing...")
    summary = summarize_emails(raw_emails)

    print("📲 Sending WhatsApp...")
    sid = send_to_whatsapp(f"📬 *Your Daily Email Summary:*\n\n{summary}")
    print("✅ Sent! SID:", sid)


run_agent()
