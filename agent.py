import os
import openai
from dotenv import load_dotenv

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Path to the file where your access token will be stored
TOKEN_FILE = 'token.json'

# Gmail API scopes and credentials file
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
GMAIL_CREDENTIALS_FILE = os.getenv("GMAIL_CREDENTIALS_FILE")

# --- Gmail API Setup and Authentication ---
def get_gmail_service():
    """Authenticates with the Gmail API and returns the service object."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GMAIL_CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
            
    return build('gmail', 'v1', credentials=creds)

# --- OpenAI LLM Functions ---
def classify_email(email_body):
    """Uses OpenAI to classify an email's urgency and type."""
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt_content = f"""
    You are an AI email assistant. Classify the following email into one of these categories:
    - Urgent: The email requires an immediate response or action.
    - Follow-up: The email requires a non-urgent response or a follow-up task.
    - Spam: The email is unsolicited and likely promotional or unwanted.

    Email content:
    "{email_body[:1000]}"

    Classification:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that classifies emails with a single word."},
                {"role": "user", "content": prompt_content}
            ],
            max_tokens=10,
            temperature=0.0
        )
        classification = response.choices[0].message.content.strip()
        return classification
    except Exception as e:
        print(f"Error classifying email: {e}")
        return "Unknown"

def draft_response(email_body, classification):
    """Uses OpenAI to draft a response based on the email and its classification."""
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    system_prompt = ""
    if classification.lower() == "urgent":
        system_prompt = "Draft a professional, polite, and brief response to an urgent email, acknowledging receipt and stating you will get back to them as soon as possible."
    elif classification.lower() == "follow-up":
        system_prompt = "Draft a professional, polite response to an email, acknowledging receipt and stating you will look into it soon."
    else:
        return None

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": email_body[:1000]}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error drafting response: {e}")
        return None

# --- Gmail Actions ---
def get_unread_emails(service):
    """Fetches unread emails from the inbox."""
    results = service.users().messages().list(userId='me', q='is:unread').execute()
    messages = results.get('messages', [])
    return messages

def get_email_body(service, message_id):
    """Gets the body of a specific email."""
    try:
        message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
        
        # This function is simplified to find the email body
        payload = message.get('payload')
        if payload and payload.get('parts'):
            parts = payload['parts']
            for part in parts:
                if part.get('mimeType') == 'text/plain':
                    data = part.get('body', {}).get('data')
                    if data:
                        return part['body']['data']

        return ""
    except Exception as e:
        print(f"Error getting email body for message {message_id}: {e}")
        return ""

def send_reply(service, thread_id, to_email, subject, body):
    """Sends a reply to an email thread."""
    message = {
        'raw': f'From: me\r\nTo: {to_email}\r\nSubject: Re: {subject}\r\n\r\n{body}'.encode('utf-8')
    }
    service.users().messages().send(userId='me', body=message).execute()

# --- Main Logic Loop ---
def main():
    service = get_gmail_service()
    
    unread_emails = get_unread_emails(service)
    
    if not unread_emails:
        print("No new unread emails found.")
        return

    print(f"Found {len(unread_emails)} unread emails. Processing...")

    for message in unread_emails:
        msg_id = message['id']
        email_body = get_email_body(service, msg_id)
        
        if not email_body:
            print(f"Could not retrieve email body for message {msg_id}. Skipping.")
            continue

        # Classify the email
        classification = classify_email(email_body)
        print(f"Email classified as: {classification}")
        
        # Draft a response if needed
        response_body = draft_response(email_body, classification)
        
        if response_body:
            # You would need to extract recipient and subject from the email here
            # This is a simplified placeholder
            to_email = "recipient@example.com"
            subject = "Placeholder Subject"
            
            # Send the reply
            # send_reply(service, message['threadId'], to_email, subject, response_body)
            print("Drafted response (not sent):")
            print(response_body)
        else:
            print("No response needed for this email.")

        # Mark the email as read after processing
        # service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()
        # print(f"Email with ID {msg_id} marked as read.")
        print("-" * 20)

if __name__ == '__main__':
    main()