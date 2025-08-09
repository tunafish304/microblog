import os

import requests

api_key = os.getenv("BREVO_API_KEY")
if not api_key:
    raise ValueError("BREVO_API_KEY not set in environment")

url = "https://api.brevo.com/v3/smtp/email"
headers = {
    "accept": "application/json",
    "api-key": api_key,
    "content-type": "application/json",
}
payload = {
    "sender": {"name": "CS210 Microblog", "email": "noreply@cs210microblog.me"},
    "to": [{"email": "DWatson@hcc-nd.edu", "name": "Test Recipient"}],
    "subject": "✅ Brevo API Test",
    "htmlContent": "<p>This is a test email sent via Brevo API.</p>",
}

response = requests.post(url, headers=headers, json=payload)
print("Status:", response.status_code)
print("Response:", response.json())
