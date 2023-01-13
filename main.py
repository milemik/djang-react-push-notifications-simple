import os

import firebase_admin
from firebase_admin import messaging, credentials

from dotenv import load_dotenv

load_dotenv()

FIREBASE_CONF_DATA = {
    "type": "service_account",
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_EMAIL"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL")
}

REGISTRATION_TOKENS = [
    "cXnENuz5QcyKTwpRYidIXy:APA91bGNjj3xdULRNIB6AOXEbnXe8_Re3Q5OK6YaQ-_09K-pw98GLdTin9er25nv0QnShh9Jnu4jd_wbWaJK_e4MXqRGLolNk4AvlB_JnF8JvOuxTZMe7xK-ocs0vJXdGLrs77P1NY6Y",
    "fSXzH6UhBRZeVQJQq1OOIM:APA91bFF5YLuSHZJzf10WvCDP_2_jLIdKym6dHchcfqpJPyiHGSU23ckOmUmR98Dzjf5-72zxrjM5OmTnp-RPULwCK8RkElknpEpn18yvYTvHzWnkRaLjVGI6XSp3G40X-wOszHAil71"
]


class SendPushNotifications:

    def __init__(self):
        cred = credentials.Certificate(FIREBASE_CONF_DATA)
        default_app = firebase_admin.initialize_app(cred)

    def send_push(self):
        message = messaging.MulticastMessage(
            tokens=REGISTRATION_TOKENS,
            data={"score": "850", "time": "3:51"},
            notification=messaging.Notification(title="Hello test notification", body="Notification test"),
        )

        response = messaging.send_multicast(message)
        print(response.success_count)
        print(response.failure_count)
        return response


if __name__ == "__main__":
    SendPushNotifications().send_push()