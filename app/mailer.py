import threading
import requests
import os

# load and sanitize API key
BREVO_API_KEY = os.getenv('BREVO_API_KEY')
BREVO_API_KEY = BREVO_API_KEY.strip() if BREVO_API_KEY else None
print(f"[DEBUG] BREVO_API_KEY 0805: {BREVO_API_KEY}")

BREVO_API_URL = 'https://api.brevo.com/v3/smtp/email'

def send_email(subject, sender, recipients, text_body, html_body):
    """Launch email send in a background thread to avoid blocking the main app."""
    thread = threading.Thread(
        target=send_async_email,
        args=(subject, sender, recipients, text_body, html_body)
    )
    print(f"[DEBUG] starting thread: {BREVO_API_KEY}")
    thread.start()

def build_payload(subject, sender, recipients, text_body, html_body):
    """Construct the JSON payload for Brevo API."""
    return {
        "sender": {"name": sender.split('@')[0], "email": sender},
        "to": [{"email": r} for r in recipients],
        "subject": subject,
        "htmlContent": html_body,
        "textContent": text_body
    }

def send_async_email(subject, sender, recipients, text_body, html_body):
    print("[Email Thread] Started send_async_email", flush=True)

    if not BREVO_API_KEY:
        print("[Email Thread] BREVO_API_KEY is missing.")
        raise RuntimeError("BREVO_API_KEY environment variable not set")

    headers = {
        'accept': 'application/json',
        'api-key': BREVO_API_KEY,
        'content-type': 'application/json'
    }

    payload = build_payload(subject, sender, recipients, text_body, html_body)
    print("entering try statement")

    try:
        response = requests.post(BREVO_API_URL, headers=headers, json=payload)
        print(f"[Email Thread] Status: {response.status_code}")

        if response.status_code >= 400:
            print(f"[Email Thread] Warning: Received error status {response.status_code}")

        try:
            print(f"[Email Thread] Response: {response.json()}")
        except ValueError:
            print(f"[Email Thread] Non-JSON response: {response.text}")

    except Exception as e:
        print(f"[Email Thread] Error sending email: {e}")
