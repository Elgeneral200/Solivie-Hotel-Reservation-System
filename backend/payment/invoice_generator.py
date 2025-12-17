"""
Invoice and receipt generation.
Creates professional PDF invoices for bookings.
UPDATED: Enhanced design with tables, colors, and proper formatting
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from datetime import datetime
import config
from utils.helpers import format_currency, format_datetime
import os


class InvoiceGenerator:
    """Generates professional invoices and receipts."""
    
    @staticmethod
    def generate_booking_invoice(booking, payment, user, room, output_path):
        """
        Generate professional PDF invoice for booking.
        
        Args:
            booking: Booking object (or dict)
            payment: Payment object (or dict)
            user: User object (or dict)
            room: Room object (or dict)
            output_path: Where to save the PDF
        
        Returns:
            (success: bool, file_path_or_error: str)
        """
        try:
            c = canvas.Canvas(output_path, pagesize=letter)
            width, height = letter
            
            # Helper to handle both objects and dictionaries
            def get_value(obj, key, default='N/A'):
                if isinstance(obj, dict):
                    return obj.get(key, default)
                return getattr(obj, key, default)
            
            # ===== HEADER =====
            # Company name with colored background
            c.setFillColorRGB(0.4, 0.49, 0.92)  # Purple-blue color
            c.rect(0, height - 100, width, 100, fill=True, stroke=False)
            
            c.setFillColorRGB(1, 1, 1)  # White text
            c.setFont("Helvetica-Bold", 28)
            c.drawString(50, height - 50, f"🏨 {config.COMPANY_NAME}")
            
            c.setFont("Helvetica", 11)
            c.drawString(50, height - 70, config.COMPANY_ADDRESS)
            c.drawString(50, height - 85, f"Phone: {config.COMPANY_PHONE} | Email: {config.ADMIN_EMAIL}")
            
            # Invoice title
            c.setFillColorRGB(0, 0, 0)  # Black text
            c.setFont("Helvetica-Bold", 20)
            c.drawString(50, height - 130, "INVOICE / RECEIPT")
            
            # Invoice info box (right side)
            c.setFont("Helvetica-Bold", 11)
            c.drawString(400, height - 130, "Invoice Details:")
            c.setFont("Helvetica", 10)
            c.drawString(400, height - 145, f"Invoice #: {get_value(booking, 'booking_reference')}")
            c.drawString(400, height - 160, f"Date: {datetime.now().strftime('%B %d, %Y')}")
            c.drawString(400, height - 175, f"Status: PAID ✓")
            
            # ===== CUSTOMER INFORMATION =====
            y = height - 210
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Bill To:")
            
            c.setFont("Helvetica", 10)
            c.drawString(50, y - 20, f"{get_value(user, 'first_name')} {get_value(user, 'last_name')}")
            c.drawString(50, y - 35, f"Email: {get_value(user, 'email')}")
            c.drawString(50, y - 50, f"Phone: {get_value(user, 'phone_number', 'N/A')}")
            
            # ===== BOOKING DETAILS TABLE =====
            y = y - 90
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Booking Details:")
            
            y = y - 15
            
            # Calculate nights
            check_in = get_value(booking, 'check_in_date')
            check_out = get_value(booking, 'check_out_date')
            if hasattr(check_in, 'date'):
                check_in_str = check_in.strftime('%B %d, %Y')
                check_out_str = check_out.strftime('%B %d, %Y')
                nights = (check_out - check_in).days
            else:
                check_in_str = str(check_in)
                check_out_str = str(check_out)
                nights = 'N/A'
            
            booking_table_data = [
                ['Booking Reference', get_value(booking, 'booking_reference')],
                ['Room', f"{get_value(room, 'room_number')} - {get_value(room, 'room_type')}"],
                ['Check-in Date', check_in_str],
                ['Check-out Date', check_out_str],
                ['Number of Nights', str(nights)],
                ['Number of Guests', str(get_value(booking, 'num_guests'))],
            ]
            
            # Special requests if any
            special_requests = get_value(booking, 'special_requests', None)
            if special_requests:
                booking_table_data.append(['Special Requests', special_requests])
            
            # Draw booking details table
            c.setFont("Helvetica", 10)
            for i, (label, value) in enumerate(booking_table_data):
                c.setFont("Helvetica-Bold", 10)
                c.drawString(50, y - (i * 18), f"{label}:")
                c.setFont("Helvetica", 10)
                c.drawString(200, y - (i * 18), str(value))
            
            # ===== PAYMENT BREAKDOWN TABLE =====
            y = y - (len(booking_table_data) * 18) - 40
            
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Payment Summary:")
            
            y = y - 20
            
            # Calculate breakdown
            total_amount = get_value(booking, 'total_amount', 0)
            if isinstance(total_amount, (int, float)):
                tax_rate = config.TAX_PERCENTAGE / 100
                subtotal = total_amount / (1 + tax_rate)
                tax_amount = total_amount - subtotal
            else:
                subtotal = 0
                tax_amount = 0
                total_amount = 0
            
            # Draw line items
            c.setFont("Helvetica", 10)
            c.drawString(50, y, "Description")
            c.drawString(400, y, "Amount")
            
            # Draw separator line
            c.setStrokeColorRGB(0.7, 0.7, 0.7)
            c.line(50, y - 5, width - 50, y - 5)
            
            y = y - 25
            
            # Subtotal
            c.setFont("Helvetica", 10)
            c.drawString(50, y, f"Room Charges ({nights} night(s))")
            c.drawString(400, y, format_currency(subtotal))
            
            # Tax
            y = y - 20
            c.drawString(50, y, f"Tax ({config.TAX_PERCENTAGE}%)")
            c.drawString(400, y, format_currency(tax_amount))
            
            # Draw separator line
            y = y - 10
            c.setStrokeColorRGB(0, 0, 0)
            c.setLineWidth(2)
            c.line(50, y, width - 50, y)
            
            # Total
            y = y - 25
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "TOTAL AMOUNT")
            c.drawString(400, y, format_currency(total_amount))
            
            # ===== PAYMENT INFORMATION =====
            y = y - 40
            
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "Payment Information:")
            
            c.setFont("Helvetica", 10)
            y = y - 20
            c.drawString(50, y, f"Payment Method: {get_value(payment, 'payment_method')}")
            
            y = y - 18
            c.drawString(50, y, f"Transaction ID: {get_value(payment, 'transaction_id')}")
            
            y = y - 18
            payment_date = get_value(payment, 'payment_date')
            if hasattr(payment_date, 'strftime'):
                payment_date_str = payment_date.strftime('%B %d, %Y at %I:%M %p')
            else:
                payment_date_str = str(payment_date)
            c.drawString(50, y, f"Payment Date: {payment_date_str}")
            
            y = y - 18
            c.setFont("Helvetica-Bold", 10)
            c.setFillColorRGB(0.13, 0.55, 0.13)  # Green
            c.drawString(50, y, "Payment Status: PAID ✓")
            
            # ===== FOOTER =====
            c.setFillColorRGB(0, 0, 0)
            c.setFont("Helvetica", 9)
            
            footer_y = 80
            c.drawString(50, footer_y, "Thank you for choosing Solivie Hotel!")
            c.drawString(50, footer_y - 15, "For inquiries, please contact us at support@solivie.com or +1 234 567 8900")
            
            # Draw footer line
            c.setStrokeColorRGB(0.7, 0.7, 0.7)
            c.setLineWidth(1)
            c.line(50, footer_y - 30, width - 50, footer_y - 30)
            
            c.setFont("Helvetica", 8)
            c.drawString(50, footer_y - 45, f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
            c.drawString(50, footer_y - 60, "This is a computer-generated invoice and does not require a signature.")
            
            # Save PDF
            c.save()
            
            return True, output_path
            
        except Exception as e:
            print(f"❌ Invoice generation failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return False, str(e)
    
    @staticmethod
    def get_invoice_filename(booking_reference):
        """Generate standardized invoice filename."""
        timestamp = datetime.now().strftime('%Y%m%d')
        return f"Invoice_{booking_reference}_{timestamp}.pdf"
    
    @staticmethod
    def ensure_invoice_directory():
        """Ensure invoice directory exists."""
        invoice_dir = os.path.join(os.getcwd(), 'invoices')
        if not os.path.exists(invoice_dir):
            os.makedirs(invoice_dir)
        return invoice_dir
