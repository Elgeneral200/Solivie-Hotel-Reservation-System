"""
Email notification service.
Sends booking confirmations, reminders, and promotional emails.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import config


class EmailService:
    """Handles email notifications."""
    
    @staticmethod
    def _get_smtp_connection():
        """Establish SMTP connection."""
        try:
            smtp = smtplib.SMTP(config.EMAIL_HOST, config.EMAIL_PORT)
            smtp.starttls()
            smtp.login(config.EMAIL_USER, config.EMAIL_PASSWORD)
            return smtp
        except Exception as e:
            print(f"SMTP connection failed: {str(e)}")
            return None
    
    @staticmethod
    def send_email(to_email, subject, html_content):
        """Send HTML email."""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = config.EMAIL_FROM
            msg['To'] = to_email
            msg['Subject'] = subject
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            smtp = EmailService._get_smtp_connection()
            if smtp:
                smtp.send_message(msg)
                smtp.quit()
                return True
            return False
        except Exception as e:
            print(f"Email send failed: {str(e)}")
            return False
    
    @staticmethod
    def send_booking_confirmation(to_email, booking_data):
        """Send booking confirmation email."""
        template_path = Path(__file__).parent / 'templates' / 'booking_confirmation.html'
        
        try:
            with open(template_path, 'r') as f:
                html_content = f.read()
            
            # Replace placeholders
            html_content = html_content.format(
                guest_name=booking_data.get('guest_name', ''),
                booking_reference=booking_data.get('booking_reference', ''),
                room_type=booking_data.get('room_type', ''),
                check_in=booking_data.get('check_in', ''),
                check_out=booking_data.get('check_out', ''),
                num_guests=booking_data.get('num_guests', ''),
                total_amount=booking_data.get('total_amount', ''),
                company_name=config.COMPANY_NAME
            )
            
            subject = f"Booking Confirmation - {booking_data.get('booking_reference', '')}"
            return EmailService.send_email(to_email, subject, html_content)
        except Exception as e:
            print(f"Confirmation email failed: {str(e)}")
            return False
    
    @staticmethod
    def send_cancellation_notice(to_email, cancellation_data):
        """Send booking cancellation notice."""
        template_path = Path(__file__).parent / 'templates' / 'cancellation_notice.html'
        
        try:
            with open(template_path, 'r') as f:
                html_content = f.read()
            
            html_content = html_content.format(
                guest_name=cancellation_data.get('guest_name', ''),
                booking_reference=cancellation_data.get('booking_reference', ''),
                refund_amount=cancellation_data.get('refund_amount', ''),
                company_name=config.COMPANY_NAME
            )
            
            subject = f"Booking Cancelled - {cancellation_data.get('booking_reference', '')}"
            return EmailService.send_email(to_email, subject, html_content)
        except:
            return False
