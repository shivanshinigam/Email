import csv
import smtplib
from email.mime.text import MIMEText
from pathlib import Path
from typing import Dict, List

# ==========================
# CONFIGURATION
# ==========================

# CSV file with recipients
CSV_PATH = Path("contacts.csv")

# Amazon WorkMail SMTP settings
WORKMAIL_SMTP_SERVER = "smtp.mail.ap-south-1.awsapps.com"  # TODO: confirm region
WORKMAIL_SMTP_PORT = 587

# WorkMail credentials
WORKMAIL_EMAIL = "your_workmail_address@yourdomain.com"    # e.g. rahul.sharma@yourdomain.com
WORKMAIL_PASSWORD = "YOUR_WORKMAIL_PASSWORD"               # do NOT commit to GitHub

# Dry-run mode: if True -> do NOT actually send, only print
DRY_RUN = True

# Email templates
SUBJECT_TEMPLATE = "Welcome to {company}, {name}!"

BODY_TEMPLATE = """Hi {name},

Thank you for signing up for {product} on {signup_date}.

We are excited to have you and your team at {company} with us.

Best regards,
The {company} Team
"""


# ==========================
# CORE LOGIC
# ==========================

def load_contacts(csv_path: Path) -> List[Dict[str, str]]:
    """Load contacts from CSV into a list of dictionaries."""
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Basic validation: check required columns
    required_cols = {"email", "name", "company", "product", "signup_date"}
    missing = required_cols - set(reader.fieldnames or [])
    if missing:
        raise ValueError(f"CSV is missing required columns: {', '.join(missing)}")

    return rows


def build_email(row: Dict[str, str]) -> MIMEText:
    """Build a MIMEText email object from one CSV row."""
    to_email = (row.get("email") or "").strip()
    name = (row.get("name") or "").strip()
    company = (row.get("company") or "").strip()
    product = (row.get("product") or "").strip()
    signup_date = (row.get("signup_date") or "").strip()

    if not to_email:
        raise ValueError("Missing email address in row")

    subject = SUBJECT_TEMPLATE.format(
        name=name,
        company=company,
        product=product,
        signup_date=signup_date,
    )

    body = BODY_TEMPLATE.format(
        name=name,
        company=company,
        product=product,
        signup_date=signup_date,
    )

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = WORKMAIL_EMAIL
    msg["To"] = to_email

    return msg


def send_emails_via_workmail(contacts: List[Dict[str, str]]) -> None:
    """Send emails for all contacts using a single SMTP connection."""
    if DRY_RUN:
        print("DRY_RUN is enabled → no emails will actually be sent.\n")

    # Reuse one SMTP connection for all emails (more efficient)
    with smtplib.SMTP(WORKMAIL_SMTP_SERVER, WORKMAIL_SMTP_PORT) as server:
        server.starttls()

        if not DRY_RUN:
            server.login(WORKMAIL_EMAIL, WORKMAIL_PASSWORD)

        for row in contacts:
            try:
                msg = build_email(row)
                to_email = msg["To"]

                # Preview
                print("=" * 80)
                print(f"TO      : {to_email}")
                print(f"SUBJECT : {msg['Subject']}")
                print("-" * 80)
                print(msg.get_payload())
                print("=" * 80)
                print()

                if not DRY_RUN:
                    server.send_message(msg)
                    print(f"Sent email to {to_email}\n")
                else:
                    print(f"[DRY_RUN] Would send email to {to_email}\n")

            except Exception as e:
                # Log error but continue with next recipient
                print(f"Error processing row for {row.get('email')}: {e}\n")


def main():
    try:
        contacts = load_contacts(CSV_PATH)
        print(f"Loaded {len(contacts)} contact(s) from {CSV_PATH}\n")
        send_emails_via_workmail(contacts)
    except Exception as e:
        print(f"Fatal error: {e}")


if __name__ == "__main__":
    main()
