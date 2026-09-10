"""
Sends email via Brevo's transactional HTTPS API instead of SMTP.

Render's free tier blocks all outbound SMTP traffic (ports 25, 465, 587),
so the standard django.core.mail.backends.smtp.EmailBackend can never
actually connect — it just hangs until it times out. Brevo's REST API
runs over plain HTTPS (port 443), which isn't blocked, so this backend
gets the same emails through Brevo without needing SMTP at all.

Existing code (send_mail, EmailMultiAlternatives, etc.) doesn't need to
change — only EMAIL_BACKEND in settings.py needs to point here.
"""
import requests
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


class BrevoAPIEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        api_key = getattr(settings, "BREVO_API_KEY", "")
        if not api_key:
            if not self.fail_silently:
                raise ValueError("BREVO_API_KEY is not set")
            return 0

        sent_count = 0
        for message in email_messages:
            try:
                self._send_one(message, api_key)
                sent_count += 1
            except Exception:
                if not self.fail_silently:
                    raise
        return sent_count

    def _send_one(self, message, api_key):
        html_body = None
        for content, mimetype in getattr(message, "alternatives", []) or []:
            if mimetype == "text/html":
                html_body = content
                break

        payload = {
            "sender": {"email": message.from_email},
            "to": [{"email": addr} for addr in message.to],
            "subject": message.subject,
            "textContent": message.body,
        }
        if html_body:
            payload["htmlContent"] = html_body
        if message.cc:
            payload["cc"] = [{"email": addr} for addr in message.cc]
        if message.bcc:
            payload["bcc"] = [{"email": addr} for addr in message.bcc]

        response = requests.post(
            BREVO_API_URL,
            json=payload,
            headers={
                "api-key": api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=10,
        )
        response.raise_for_status()