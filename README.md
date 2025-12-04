REPORT
CSV-Based Email Generation Using Amazon WorkMail

------------------------------------------------------------
1) Objective
------------------------------------------------------------

The objective of this mini-project is to build a system that can:

- Read recipient data from a CSV file
- Generate personalized emails for each recipient
- Send these emails automatically using Amazon WorkMail

This removes manual effort and allows scalable, consistent, and personalized communication.

------------------------------------------------------------
2) What Is CSV-Based Email Generation?
------------------------------------------------------------

CSV-based email generation means:

- Using a CSV file as the source of truth for recipients
- Each row = one email to be sent
- Each column = one piece of data used inside the email (name, company, etc.)
- A Python script reads each row, fills an email template, and sends it

So instead of writing 100 emails by hand, we write:

- One CSV file
- One template
- One script

And let the system do the rest.

------------------------------------------------------------
3) CSV File Design
------------------------------------------------------------

We use a simple CSV file named contacts.csv.

Example:

email,name,company,product,signup_date
alice@gmail.com,Alice,Google,Ads,2024-12-01
bob@gmail.com,Bob,Amazon,AWS,2024-12-02
rahul@gmail.com,Rahul,Flipkart,Logistics,2024-12-03

Column meaning:

- email → recipient’s email address (required)
- name → recipient’s name (used in greeting and subject)
- company → company name (used for personalization)
- product → product or service they signed up for
- signup_date → date for contextual reference in the email

The code validates that all required columns exist, so the template variables always have data.

------------------------------------------------------------
4) Email Template
------------------------------------------------------------

Subject template:

Welcome to {company}, {name}!

Body template:

Hi {name},

Thank you for signing up for {product} on {signup_date}.

We are excited to have you and your team at {company} with us.

Best regards,
The {company} Team

The {name}, {company}, {product}, and {signup_date} placeholders are replaced for each row using the data in the CSV.

------------------------------------------------------------
5) Amazon WorkMail as Email Provider
------------------------------------------------------------

Amazon WorkMail is used as the SMTP server to send emails.

We configure:

- SMTP server: smtp.mail.<region>.awsapps.com (e.g. smtp.mail.ap-south-1.awsapps.com)
- Port: 587 (TLS)
- Username: WorkMail email address (e.g. user@yourdomain.com)
- Password: WorkMail password

Python connects to this server using smtplib, logs in with the WorkMail credentials, and sends emails from that mailbox.

------------------------------------------------------------
6) Code Structure (Important Design Points)
------------------------------------------------------------

The script is structured into clear, small functions. Key parts:

1) CONFIGURATION SECTION

At the top of the script, we keep all configuration in one place:

- CSV_PATH → which CSV file to read
- WorkMail SMTP server / port
- WorkMail email and password
- DRY_RUN flag (very important for safe testing)
- Subject and body templates

This makes the script easy to change without touching the core logic.

2) load_contacts(csv_path)

- Reads the CSV using csv.DictReader
- Converts each row into a dictionary
- Validates that required columns are present
- Returns a list of rows

This ensures that before we build any email, the input data is consistent.

3) build_email(row)

- Takes one row (one recipient)
- Extracts fields (email, name, company, product, signup_date)
- Fills the subject and body templates using .format(...)
- Builds a MIMEText email object (which is what SMTP needs)

This keeps email construction separate from CSV reading and sending.

4) send_emails_via_workmail(contacts)

- Opens a single SMTP connection using WorkMail
- Reuses this connection to send all emails (much more efficient than reconnecting for each row)
- If DRY_RUN is True:
  - Does not send emails
  - Only prints preview to the terminal
- If DRY_RUN is False:
  - Logs into WorkMail
  - Sends each email using server.send_message(msg)
- Handles errors per row so one bad row doesn’t stop the whole batch

5) DRY_RUN Flag

This is a very important safety feature:

- DRY_RUN = True → Preview mode, no actual sending
- DRY_RUN = False → Production mode, emails are actually sent

This is useful for:

- Testing templates
- Checking CSV parsing
- Verifying personalization
- Avoiding accidental emails during development

6) Error Handling

- If the CSV file is missing → clear error message
- If required columns are missing → clear error message
- If a row has no email → that row is skipped
- If one row fails (bad data, etc.) → error is printed but loop continues for other recipients

All of this makes the script robust and safe for practical usage.

------------------------------------------------------------
7) How to Use the Script (Step-by-Step)
------------------------------------------------------------

STEP 1: Create the CSV file

Create a file named contacts.csv in your project folder:

email,name,company,product,signup_date
alice@gmail.com,Alice,Google,Ads,2024-12-01
bob@gmail.com,Bob,Amazon,AWS,2024-12-02
rahul@gmail.com,Rahul,Flipkart,Logistics,2024-12-03

STEP 2: Create the Python script

Create a file named send_workmail_from_csv.py and paste the optimized script, with:

- Configuration section at the top
- load_contacts
- build_email
- send_emails_via_workmail
- main()

STEP 3: Configure WorkMail settings

At the top of the script, update:

- WORKMAIL_SMTP_SERVER (e.g. "smtp.mail.ap-south-1.awsapps.com")
- WORKMAIL_EMAIL (e.g. "your_workmail@yourdomain.com")
- WORKMAIL_PASSWORD (your WorkMail password)
- DRY_RUN = True (for testing first)

STEP 4: Run in DRY-RUN mode

In the folder where the script and CSV are located:

python3 send_workmail_from_csv.py

What you will see:

- For each row:
  - "TO" address
  - Subject
  - Email body
- Messages like:
  [DRY_RUN] Would send email to alice@gmail.com

This confirms that:

- CSV is read correctly
- Templates are filled correctly
- Logic is working

STEP 5: Enable real sending

Once everything looks correct, change:

DRY_RUN = False

Now run again:

python3 send_workmail_from_csv.py

This time the script:

- Connects to WorkMail
- Logs in with your WorkMail credentials
- Sends emails for each row

STEP 6: Verify

Check:

- Recipient inboxes (if you used real emails)
- WorkMail "Sent" folder

------------------------------------------------------------
8) Example Scenario
------------------------------------------------------------

Use case:

You have a list of users who signed up for your product, and you want to send each of them a personalized welcome mail through your company’s WorkMail address.

- You export the user list to CSV.
- You drop it into contacts.csv.
- You set up the script and run it.

Result:

- Each user receives a customized mail with:
  - Their name
  - Their company
  - The product they signed up for
  - The date

All with one command.


