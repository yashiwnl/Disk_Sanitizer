import os
import smtplib

from email.message import EmailMessage


def send_mail(receiver, log_path, body):

    # ------------------------------------------------------------------
    # Create the email message.
    # ------------------------------------------------------------------

    mail = EmailMessage()

    mail["From"] = "your_email"
    mail["To"] = receiver
    mail["Subject"] = "your_subject"

    mail.set_content(body)

    server = None

    try:

        # ------------------------------------------------------------------
        # Connect to Gmail SMTP Server.
        # ------------------------------------------------------------------

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        # ------------------------------------------------------------------
        # Login using Gmail App Password.
        #
        # Note:
        # This is NOT your Gmail account password.
        #
        # Steps:
        # 1. Enable Two-Factor Authentication.
        # 2. Open Google Account → Security.
        # 3. Generate an App Password.
        # 4. Use the generated 16-character password below.
        # ------------------------------------------------------------------

        server.login("your_gmail", "app_password")

        # ------------------------------------------------------------------
        # Read and attach the log file.
        # ------------------------------------------------------------------

        with open(log_path, "rb") as attachment:

            data = attachment.read()

            mail.add_attachment(
                data,
                maintype="text",
                subtype="plain",
                filename=os.path.basename(log_path)
            )

        server.send_message(mail)

    except Exception as e:

        # ------------------------------------------------------------------
        # Write email errors to the log file.
        # ------------------------------------------------------------------

        with open(log_path, "a") as log_file:
            log_file.write(f"\nEmail Error: {e}\n")

        return False

    finally:

        if server is not None:
            server.quit()

    return True