"""
Email notification service.
Sends booking confirmations, reminders, and promotional emails.
Works in TESTING MODE (prints to console) and PRODUCTION MODE (sends real emails).
DEBUG VERSION - Shows credential loading
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from datetime import datetime
import config


class EmailService:
    """Handles email notifications with testing mode support."""
    
    @staticmethod
    def _get_smtp_connection():
        """Establish SMTP connection."""
        # Skip SMTP in testing mode
        if not config.EMAIL_ENABLED:
            return None
        
        # 🔍 DEBUG: Show what's being loaded
        print("\n" + "🔍" * 35)
        print("DEBUG: Email Configuration")
        print("🔍" * 35)
        print(f"EMAIL_ENABLED: {config.EMAIL_ENABLED}")
        print(f"EMAIL_HOST: {config.EMAIL_HOST}")
        print(f"EMAIL_PORT: {config.EMAIL_PORT}")
        print(f"EMAIL_USER: {config.EMAIL_USER}")
        print(f"EMAIL_USER length: {len(config.EMAIL_USER)} chars")
        print(f"EMAIL_USER bytes: {config.EMAIL_USER.encode('utf-8')}")
        print(f"EMAIL_PASSWORD length: {len(config.EMAIL_PASSWORD)} chars")
        print(f"EMAIL_PASSWORD (masked): {'*' * len(config.EMAIL_PASSWORD)}")
        print(f"EMAIL_PASSWORD bytes: {config.EMAIL_PASSWORD.encode('utf-8')}")
        print("🔍" * 35 + "\n")
            
        try:
            print("📡 Connecting to SMTP server...")
            smtp = smtplib.SMTP(config.EMAIL_HOST, config.EMAIL_PORT, local_hostname='localhost', timeout=10)
            print("✅ SMTP connection established")
            
            print("🔒 Starting TLS...")
            smtp.starttls()
            print("✅ TLS started")
            
            print(f"🔑 Logging in as: {config.EMAIL_USER}")
            smtp.login(config.EMAIL_USER, config.EMAIL_PASSWORD)
            print("✅ Login successful!")
            
            return smtp
        except Exception as e:
            print(f"❌ SMTP connection failed: {str(e)}")
            print(f"❌ Error type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def send_email(to_email, subject, html_content, plain_text=None):
        """
        Send HTML email (or print to console in testing mode).
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML email body
            plain_text: Plain text version (optional)
        
        Returns:
            bool: True if successful, False otherwise
        """
        
        # TESTING MODE: Print to console
        if not config.EMAIL_ENABLED:
            print("\n" + "=" * 70)
            print("📧 EMAIL (Testing Mode - Not Actually Sent)")
            print("=" * 70)
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print(f"From: {config.EMAIL_FROM_NAME} <{config.EMAIL_FROM_ADDRESS}>")
            print("-" * 70)
            if plain_text:
                print(plain_text)
            else:
                print("(HTML email - see template for full content)")
            print("=" * 70)
            print("✅ Email logged successfully (testing mode)")
            print()
            return True
        
        # PRODUCTION MODE: Send real email
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{config.EMAIL_FROM_NAME} <{config.EMAIL_FROM_ADDRESS}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            msg['Reply-To'] = config.EMAIL_REPLY_TO
            
            # Add plain text version if provided
            if plain_text:
                text_part = MIMEText(plain_text, 'plain')
                msg.attach(text_part)
            
            # Add HTML version
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            smtp = EmailService._get_smtp_connection()
            if smtp:
                smtp.send_message(msg)
                smtp.quit()
                print(f"✅ Email sent to {to_email}")
                return True
            else:
                print(f"❌ Could not establish SMTP connection")
                return False
                
        except Exception as e:
            print(f"❌ Email send failed: {str(e)}")
            return False
    
    @staticmethod
    def send_booking_confirmation(to_email, booking_data):
        """Send booking confirmation email."""
        template_path = Path(__file__).parent / 'templates' / 'booking_confirmation.html'
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            check_in = booking_data.get('check_in', '')
            check_out = booking_data.get('check_out', '')
            
            if hasattr(check_in, 'strftime'):
                check_in = check_in.strftime('%B %d, %Y')
            if hasattr(check_out, 'strftime'):
                check_out = check_out.strftime('%B %d, %Y')
            
            html_content = html_content.format(
                guest_name=booking_data.get('guest_name', ''),
                booking_reference=booking_data.get('booking_reference', ''),
                room_type=booking_data.get('room_type', ''),
                room_number=booking_data.get('room_number', ''),
                check_in=check_in,
                check_out=check_out,
                num_guests=booking_data.get('num_guests', ''),
                total_amount=f"{config.CURRENCY_SYMBOL}{booking_data.get('total_amount', 0):.2f}",
                nights=booking_data.get('nights', ''),
                company_name=config.COMPANY_NAME,
                company_address=config.COMPANY_ADDRESS,
                company_phone=config.COMPANY_PHONE,
                support_email=config.EMAIL_SUPPORT_EMAIL,
                support_phone=config.EMAIL_SUPPORT_PHONE
            )
            
            plain_text = f"""
BOOKING CONFIRMED

Dear {booking_data.get('guest_name', '')},

Your booking has been confirmed!

BOOKING DETAILS:
Booking Reference: {booking_data.get('booking_reference', '')}
Room: {booking_data.get('room_number', '')} - {booking_data.get('room_type', '')}
Check-in: {check_in}
Check-out: {check_out}
Guests: {booking_data.get('num_guests', '')}
Duration: {booking_data.get('nights', '')} night(s)
Total Amount: {config.CURRENCY_SYMBOL}{booking_data.get('total_amount', 0):.2f}

We look forward to welcoming you!

{config.COMPANY_NAME}
{config.COMPANY_PHONE}
            """
            
            subject = f"✅ Booking Confirmed - {booking_data.get('booking_reference', '')}"
            return EmailService.send_email(to_email, subject, html_content, plain_text)
            
        except FileNotFoundError:
            print(f"❌ Template not found: {template_path}")
            return False
        except Exception as e:
            print(f"❌ Confirmation email failed: {str(e)}")
            return False
    
    @staticmethod
    def send_cancellation_notice(to_email, cancellation_data):
        """Send booking cancellation notice."""
        template_path = Path(__file__).parent / 'templates' / 'cancellation_notice.html'
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            cancel_date = cancellation_data.get('cancellation_date', datetime.now())
            if hasattr(cancel_date, 'strftime'):
                cancel_date = cancel_date.strftime('%B %d, %Y')
            
            html_content = html_content.format(
                guest_name=cancellation_data.get('guest_name', ''),
                booking_reference=cancellation_data.get('booking_reference', ''),
                refund_amount=f"{config.CURRENCY_SYMBOL}{cancellation_data.get('refund_amount', 0):.2f}",
                cancellation_date=cancel_date,
                company_name=config.COMPANY_NAME,
                company_address=config.COMPANY_ADDRESS,
                company_phone=config.COMPANY_PHONE,
                support_email=config.EMAIL_SUPPORT_EMAIL,
                support_phone=config.EMAIL_SUPPORT_PHONE
            )
            
            plain_text = f"""
BOOKING CANCELLED

Dear {cancellation_data.get('guest_name', '')},

Your booking has been cancelled as requested.

CANCELLATION DETAILS:
Booking Reference: {cancellation_data.get('booking_reference', '')}
Refund Amount: {config.CURRENCY_SYMBOL}{cancellation_data.get('refund_amount', 0):.2f}
Cancellation Date: {cancel_date}

The refund will be processed within 5-7 business days.

{config.COMPANY_NAME}
{config.COMPANY_PHONE}
            """
            
            subject = f"❌ Booking Cancelled - {cancellation_data.get('booking_reference', '')}"
            return EmailService.send_email(to_email, subject, html_content, plain_text)
            
        except FileNotFoundError:
            print(f"❌ Template not found: {template_path}")
            return False
        except Exception as e:
            print(f"❌ Cancellation email failed: {str(e)}")
            return False
    
    @staticmethod
    def send_payment_receipt(to_email, payment_data):
        """Send payment receipt email."""
        try:
            payment_date = payment_data.get('payment_date', datetime.now())
            if hasattr(payment_date, 'strftime'):
                payment_date = payment_date.strftime('%B %d, %Y at %I:%M %p')
            
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Payment Receipt</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif;">
    <h2>💳 Payment Receipt</h2>
    <p>Dear <strong>{payment_data.get('guest_name', '')}</strong>,</p>
    <p>Thank you for your payment!</p>
    <p><strong>Booking Reference:</strong> {payment_data.get('booking_reference', '')}</p>
    <p><strong>Amount:</strong> {config.CURRENCY_SYMBOL}{payment_data.get('amount', 0):.2f}</p>
    <p><strong>Transaction ID:</strong> {payment_data.get('transaction_id', 'N/A')}</p>
</body>
</html>
            """
            
            plain_text = f"""
PAYMENT RECEIPT

Dear {payment_data.get('guest_name', '')},

Booking Reference: {payment_data.get('booking_reference', '')}
Amount Paid: {config.CURRENCY_SYMBOL}{payment_data.get('amount', 0):.2f}

{config.COMPANY_NAME}
            """
            
            subject = f"💳 Payment Receipt - {payment_data.get('booking_reference', '')}"
            return EmailService.send_email(to_email, subject, html_content, plain_text)
            
        except Exception as e:
            print(f"❌ Payment receipt email failed: {str(e)}")
            return False
