import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json',  # Path to the downloaded JSON file
        SCOPES
    )
    credentials = flow.run_local_server(port=0)
    return credentials

def extract_emails(credentials):
    service = build('gmail', 'v1', credentials=credentials)
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    extracted_emails = []

    if not messages:
        print('No emails found.')
    else:
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            email_data = msg['payload']['headers']
            email_info = {}

            for values in email_data:
                name = values['name']
                if name == 'From':
                    email_info['From'] = values['value']
                elif name == 'Subject':
                    email_info['Subject'] = values['value']

            email_info['Snippet'] = msg['snippet']

            extracted_emails.append(email_info)

            # Extract the email content
            parts = msg['payload'].get('parts', [])
            for part in parts:
                mimeType = part.get('mimeType')
                body = part.get('body', {})
                data = body.get('data')
                if part['mimeType'] == 'text/plain' and data:
                    text = base64.urlsafe_b64decode(data).decode('utf-8')
                    print('Email Content:')
                    print(text)
                    print('-------------------')
    return extracted_emails

# credentials = authenticate()
# extract_emails(credentials)