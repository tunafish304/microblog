import os
from threading import Thread

from dotenv import load_dotenv
from mailersend import emails

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

http_mailer = emails.NewEmail(os.getenv("MAILERSEND_API_KEY"))
print("API Key:", os.getenv("MAILERSEND_API_KEY"))


# --- HTTP Send via MailerSend ---
def send_via_http(subject, to_email, to_name, text, html):
    body = {}

    # Set sender and recipient
    http_mailer.set_mail_from(
        {"name": "Microblog", "email": "noreply@cs210microblog.me"},  # ✅ update domain
        body,
    )
    http_mailer.set_mail_to([{"name": to_name, "email": to_email}], body)

    # Set content
    http_mailer.set_subject(subject, body)
    http_mailer.set_html_content(html, body)
    http_mailer.set_plaintext_content(text, body)

    # Send asynchronously
    def send_async_http():
        try:
            response = http_mailer.send(body)
            print("MailerSend response:", response)
        except Exception as e:
            print("HTTP email failed:", e)
            # TODO: Add retry logic or queueing for failed sends

    Thread(target=send_async_http, name="HTTPEmailThread").start()


# --- CLI Test Block ---
if __name__ == "__main__":
    send_via_http(
        subject="Test from CLI",
        to_email="tunafish304@gmail.com",  # "DWatson@hcc-nd.edu",
        to_name="David",
        text="This is a plain text fallback.",
        html="<p>This is a <strong>test email</strong> sent from the command line.</p>",
    )
