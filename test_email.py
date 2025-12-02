import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

sender_email = os.getenv('GMAIL_USER')
password = os.getenv('GMAIL_PASSWORD')

print(f"User: {sender_email}")
print(f"Password (raw): '{password}'")

# Try stripping spaces
password_stripped = password.replace(" ", "")
print(f"Password (stripped): '{password_stripped}'")

recipient_email = sender_email # Send to self

msg = MIMEText("This is a test email from the CV Adapter debugger.")
msg['Subject'] = "Test Email"
msg['From'] = sender_email
msg['To'] = recipient_email

try:
    print("Attempting to connect to SMTP_SSL (465)...")
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # server.starttls() # Not needed for SMTP_SSL
    
    print("Attempting login with STRIPPED password...")
    server.login(sender_email, password_stripped)
    print("Login SUCCESS!")
    
    server.sendmail(sender_email, recipient_email, msg.as_string())
    print("Email SENT!")
    server.quit()
except Exception as e:
    print(f"Login/Send FAILED: {e}")
    
    # Optional: Try with raw password if stripped failed?
    # Usually stripped is the correct way.
