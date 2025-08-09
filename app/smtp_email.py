import os
from threading import Thread

from flask import current_app
from flask_mail import Message
from mailersend import emails

# --- SMTP Setup ---
from app import mail

# --- MailerSend Setup ---
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "smtp")  # 'smtp' or 'http'
http_mailer = emails.NewEmail(os.getenv("MAILERSEND_API_KEY"))


# --- Async SMTP Send ---
def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
            print(f"SMTP email sent to {msg.recipients}")
        except Exception as e:
            print("SMTP email failed:", e)


# --- Unified Send Entry Point ---
def send_email(subject, sender, recipients, text_body, html_body, recipient_names=None):
    """
    Sends email using selected backend.
    - SMTP: uses Flask-Mail
    - HTTP: uses MailerSend API
    """
    if EMAIL_BACKEND == "http":
        # Assuming single recipient for HTTP
        to_email = recipients[0]
        to_name = recipient_names[0] if recipient_names else "Recipient"
        send_via_http(subject, to_email, to_name, text_body, html_body)
    elif EMAIL_BACKEND == "smtp":
        send_via_smtp(subject, sender, recipients, text_body, html_body)


# --- HTTP Send via MailerSend ---
def send_via_http(subject, to_email, to_name, text, html):
    body = {}

    # Set sender and recipient
    http_mailer.set_mail_from(
        {"name": "Microblog", "email": "noreply@test-z0vklo60zk1l7qrx.mlsender.net"},
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


# --- SMTP Send via Flask-Mail ---
def send_via_smtp(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    Thread(
        target=send_async_email,
        args=(current_app._get_current_object(), msg),
        name="SMTPEmailThread",
    ).start()
