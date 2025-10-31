"""
Invoice and receipt generation.
Creates PDF invoices for bookings.
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import config
from utils.helpers import format_currency, format_datetime


class InvoiceGenerator:
    """Generates invoices and receipts."""
    
    @staticmethod
    def generate_booking_invoice(booking, payment, user, room, output_path):
        """
        Generate PDF invoice for booking.
        Returns: (success, file_path)
        """
        try:
            c = canvas.Canvas(output_path, pagesize=letter)
            width, height = letter
            
            # Header
            c.setFont("Helvetica-Bold", 24)
            c.drawString(50, height - 50, config.COMPANY_NAME)
            
            c.setFont("Helvetica", 10)
            c.drawString(50, height - 70, config.COMPANY_ADDRESS)
            c.drawString(50, height - 85, f"Phone: {config.COMPANY_PHONE}")
            
            # Invoice title
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 130, "BOOKING INVOICE")
            
            # Booking details
            c.setFont("Helvetica", 11)
            y = height - 170
            
            c.drawString(50, y, f"Booking Reference: {booking.booking_reference}")
            c.drawString(50, y - 20, f"Invoice Date: {datetime.now().strftime('%Y-%m-%d')}")
            c.drawString(50, y - 40, f"Customer: {user.first_name} {user.last_name}")
            c.drawString(50, y - 60, f"Email: {user.email}")
            
            # Booking info
            y = y - 100
            c.drawString(50, y, f"Room: {room.room_number} - {room.room_type}")
            c.drawString(50, y - 20, f"Check-in: {format_datetime(booking.check_in_date)}")
            c.drawString(50, y - 40, f"Check-out: {format_datetime(booking.check_out_date)}")
            c.drawString(50, y - 60, f"Guests: {booking.num_guests}")
            
            # Payment details
            y = y - 100
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Payment Details")
            
            c.setFont("Helvetica", 11)
            c.drawString(50, y - 25, f"Amount Paid: {format_currency(payment.amount)}")
            c.drawString(50, y - 45, f"Payment Method: {payment.payment_method}")
            c.drawString(50, y - 65, f"Transaction ID: {payment.transaction_id}")
            c.drawString(50, y - 85, f"Payment Date: {format_datetime(payment.payment_date)}")
            
            # Footer
            c.setFont("Helvetica", 9)
            c.drawString(50, 50, "Thank you for choosing us!")
            
            c.save()
            
            return True, output_path
            
        except Exception as e:
            return False, str(e)
