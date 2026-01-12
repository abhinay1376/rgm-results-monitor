import requests
import hashlib
import os
import smtplib
from email.mime.text import MIMEText

URL = "https://rgmexams.co.in/Results.php"
HASH_FILE = "page_hash.txt"

def get_page_hash():
    r = requests.get(URL, timeout=30)
    r.raise_for_status()
    return hashlib.sha256(r.text.encode()).hexdigest()

def send_email():
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    receiver = os.getenv("EMAIL_TO")

    msg = MIMEText(
        "🚨 RGM Results Page Updated!\n\n"
        "Check here:\nhttps://rgmexams.co.in/Results.php"
    )
    msg["Subject"] = "RGM Results Update Alert"
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)

def main():
    new_hash = get_page_hash()

    old_hash = ""
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            old_hash = f.read()

    if new_hash != old_hash:
        send_email()
        with open(HASH_FILE, "w") as f:
            f.write(new_hash)
    else:
        print("No change detected")

if __name__ == "__main__":
    main()
