import os

import firebase_admin
from firebase_admin import messaging, credentials
import environ

env = environ.Env()

environ.Env.read_env(os.path.join(os.getcwd(), ".env"))

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
]


class SendPushNotifications:

    def __init__(self):
        cred = credentials.Certificate(FIREBASE_CONF_DATA)
        self.app = firebase_admin.initialize_app(cred)

    def close_app(self):
        firebase_admin.delete_app(self.app)

    @staticmethod
    def send_push():
        message = messaging.MulticastMessage(
            tokens=REGISTRATION_TOKENS,
            data={"score": "850", "time": "3:51"},
            notification=messaging.Notification(title="Hello test notification", body="Notification test"),
        )

        response = messaging.send_multicast(message)
        print(f"SUCCESS: {response.success_count}")
        print(f"FAILED:  {response.failure_count}")
        return response


if __name__ == "__main__":
    init_push = SendPushNotifications()
    init_push.send_push()
    init_push.close_app()
