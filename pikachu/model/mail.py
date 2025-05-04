from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os, pickle
from dotenv import load_dotenv
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from rich.console import Console
from rich.panel import Panel
console = Console()
load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",".."))


to=os.getenv("to")
my=os.getenv("my")

def get_gmail_service():
    creds=None

    #  load token if exists
    if os.path.exists(os.path.join(root_dir,"token.pickle")):
        print("Found token.pickle...")
        with open(os.path.join(root_dir,"token.pickle"),"rb") as token:
            creds = pickle.load(token)


    # authenticate if cred are invalid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token....")
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(root_dir,"credentials.json"), SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save credentials for future use
        with open(os.path.join(root_dir,"token.pickle"), "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)


# Send Email Reply
def send_email_reply(service,recipient,owner):

    subject = "Emergency Alert"
    body = "Alert !!! Panic situation."
    message = MIMEMultipart()
    message["Subject"] = subject
    message["To"] = recipient  # Replace with actual recipient
    message["From"] = owner  # Replace with your email
    # Attach email body
    message.attach(MIMEText(body, "plain"))

    # Encode email in Base64
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    message_data={"raw":raw_message}
    # Send email using Gmail API
    try:
        service.users().messages().send(userId="me", body=message_data).execute()
        console.print(Panel(f"[bold green]Reply sent to {recipient}[/bold green]", title="Success", style="green"))
    except Exception as e:
        console.print(Panel(f"[bold red]Failed to send email.[/bold red]\nError: {str(e)}", title="Error", style="red"))

def main():
    service=get_gmail_service()
    send_email_reply(service,to,my)


