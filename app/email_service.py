#app/email_service.py
from flask import current_app
import smtplib
import ssl


def send_gmail(receiver_email, subject, body, sender_email=None):
    """
    Send email using Gmail SMTP with our application's configuration
    Args:
        receiver_email: To address
        subject: Email subject
        body: Email body content
        sender_email: Optional from address (defaults to config DEFAULT_SENDER)
    Returns:
        bool: True if sent successfully, False otherwise
    """
    if not sender_email:
        sender_email = current_app.config['DEFAULT_SENDER']

    try:
        # Get configuration from Flask app
        password = current_app.config['GMAIL_APP_PASSWORD']
        smtp_server = "smtp.gmail.com"
        port = 465  # SSL port

        # Create message with proper headers
        message = f"Subject: {subject}\n\n{body}"

        # Create secure SSL context
        context = ssl.create_default_context()

        # Connect and send
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

        current_app.logger.info(f"Email sent successfully to {receiver_email}")
        return True

    except smtplib.SMTPAuthenticationError as e:
        error_msg = (
            f"SMTP Authentication Error: {e}\n"
            "Possible solutions:\n"
            "1. Ensure you're using an App Password (if 2FA enabled)\n"
            "2. Check 'Less secure app access' is ON (if no 2FA)\n"
            "3. Verify sender_email matches the authenticated account\n"
            "More info: https://support.google.com/mail/?p=BadCredentials"
        )
        current_app.logger.error(error_msg)
        return False

    except Exception as e:
        current_app.logger.error(f"Email sending failed: {str(e)}")
        return False