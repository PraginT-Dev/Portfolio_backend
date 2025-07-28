import requests
from decouple import config

def send_email_via_brevo(to_email, subject, html_content):
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": config("BREVO_API_KEY"),
        "content-type": "application/json"
    }
    data = {
        "sender": {
            "name": "Portfolio Contact",
            "email": config("EMAIL_HOST_USER")  # must match verified sender
        },
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": html_content
    }

    response = requests.post(url, headers=headers, json=data)
    return response.status_code, response.json()
