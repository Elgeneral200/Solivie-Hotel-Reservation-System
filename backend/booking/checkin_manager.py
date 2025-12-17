"""
Check-in and Check-out management.
Handles guest arrival, departure, and room status updates.
"""

from database.db_manager import get_db_session
from database.models import Booking, Room, User
from datetime import datetime, date, timedelta


class CheckInManager:
    """Manages check-in and check-out operations."""
    
    @staticmethod
    def get_todays_arrivals():
        """
        Get all bookings scheduled to check in today.
        Returns list of dictionaries with booking and guest info.
        """
        try:
            with get_db_session() as session:
                today = date.today()
                tomorrow = today + timedelta(days=1)
                
                bookings = session.query(Booking).filter(
                    Booking.check_in_date >= today,
                    Booking.check_in_date < tomorrow,
                    Booking.booking_status == 'confirmed'
                ).all()
                
                arrivals = []
                for booking in bookings:
                    user = session.query(User).filter_by(user_id=booking.user_id).first()
                    room = session.query(Room).filter_by(room_id=booking.room_id).first()
                    
                    arrivals.append({
                        'booking_id': booking.booking_id,
                        'booking_reference': booking.booking_reference,
                        'guest_name': f"{user.first_name} {user.last_name}" if user else 'N/A',
                        'guest_email': user.email if user else 'N/A',
                        'guest_phone': user.phone_number if user else 'N/A',
                        'room_number': room.room_number if room else 'N/A',
                        'room_type': room.room_type if room else 'N/A',
                        'num_guests': booking.num_guests,
                        'check_in_date': booking.check_in_date,
                        'check_out_date': booking.check_out_date,
                        'actual_check_in': booking.actual_check_in,
                        'checked_in': booking.actual_check_in is not None,
                        'id_verified': booking.id_verified,
                        'special_requests': booking.special_requests
                    })
                
                return arrivals
        except Exception as e:
            print(f"Error getting arrivals: {e}")
            return []
    
    @staticmethod
    def get_todays_departures():
        """
        Get all bookings scheduled to check out today.
        Returns list of dictionaries with booking and guest info.
        """
        try:
            with get_db_session() as session:
                today = date.today()
                tomorrow = today + timedelta(days=1)
                
                bookings = session.query(Booking).filter(
                    Booking.check_out_date >= today,
                    Booking.check_out_date < tomorrow,
                    Booking.booking_status == 'confirmed',
                    Booking.actual_check_in.isnot(None)  # Only checked-in guests
                ).all()
                
                departures = []
                for booking in bookings:
                    user = session.query(User).filter_by(user_id=booking.user_id).first()
                    room = session.query(Room).filter_by(room_id=booking.room_id).first()
                    
                    departures.append({
                        'booking_id': booking.booking_id,
                        'booking_reference': booking.booking_reference,
                        'guest_name': f"{user.first_name} {user.last_name}" if user else 'N/A',
                        'guest_email': user.email if user else 'N/A',
                        'room_number': room.room_number if room else 'N/A',
                        'room_type': room.room_type if room else 'N/A',
                        'check_in_date': booking.check_in_date,
                        'check_out_date': booking.check_out_date,
                        'actual_check_in': booking.actual_check_in,
                        'actual_check_out': booking.actual_check_out,
                        'checked_out': booking.actual_check_out is not None
                    })
                
                return departures
        except Exception as e:
            print(f"Error getting departures: {e}")
            return []
    
    @staticmethod
    def get_current_occupancy():
        """
        Get all currently occupied rooms (checked in but not checked out).
        """
        try:
            with get_db_session() as session:
                bookings = session.query(Booking).filter(
                    Booking.booking_status == 'confirmed',
                    Booking.actual_check_in.isnot(None),
                    Booking.actual_check_out.is_(None)
                ).all()
                
                occupied = []
                for booking in bookings:
                    user = session.query(User).filter_by(user_id=booking.user_id).first()
                    room = session.query(Room).filter_by(room_id=booking.room_id).first()
                    
                    occupied.append({
                        'booking_id': booking.booking_id,
                        'booking_reference': booking.booking_reference,
                        'guest_name': f"{user.first_name} {user.last_name}" if user else 'N/A',
                        'room_number': room.room_number if room else 'N/A',
                        'room_type': room.room_type if room else 'N/A',
                        'check_in_date': booking.check_in_date,
                        'check_out_date': booking.check_out_date,
                        'actual_check_in': booking.actual_check_in,
                        'num_guests': booking.num_guests
                    })
                
                return occupied
        except Exception as e:
            print(f"Error getting occupancy: {e}")
            return []
    
    @staticmethod
    def check_in_guest(booking_id, admin_id=None):
        """
        Check in a guest.
        Updates booking with actual check-in time and changes room status.
        
        Args:
            booking_id: ID of booking to check in
            admin_id: ID of admin performing check-in
        
        Returns:
            (success: bool, message: str)
        """
        try:
            with get_db_session() as session:
                booking = session.query(Booking).filter_by(booking_id=booking_id).first()
                
                if not booking:
                    return False, "Booking not found"
                
                if booking.booking_status != 'confirmed':
                    return False, f"Cannot check in: booking status is {booking.booking_status}"
                
                if booking.actual_check_in:
                    return False, "Guest already checked in"
                
                # Check if ID is verified
                if not booking.id_verified:
                    return False, "ID verification required before check-in"
                
                # Update booking
                booking.actual_check_in = datetime.now()
                booking.checked_in_by = admin_id
                
                # Update room status to occupied
                room = session.query(Room).filter_by(room_id=booking.room_id).first()
                if room:
                    room.status = 'occupied'
                
                session.commit()
                
                return True, f"Guest checked in successfully at {booking.actual_check_in.strftime('%H:%M')}"
        
        except Exception as e:
            return False, f"Check-in failed: {str(e)}"
    
    @staticmethod
    def check_out_guest(booking_id, admin_id=None):
        """
        Check out a guest.
        Updates booking with actual check-out time and changes room status.
        
        Args:
            booking_id: ID of booking to check out
            admin_id: ID of admin performing check-out
        
        Returns:
            (success: bool, message: str)
        """
        try:
            with get_db_session() as session:
                booking = session.query(Booking).filter_by(booking_id=booking_id).first()
                
                if not booking:
                    return False, "Booking not found"
                
                if not booking.actual_check_in:
                    return False, "Guest was never checked in"
                
                if booking.actual_check_out:
                    return False, "Guest already checked out"
                
                # Update booking
                booking.actual_check_out = datetime.now()
                booking.checked_out_by = admin_id
                booking.booking_status = 'completed'
                
                # Update room status to cleaning (will be set to available by housekeeping)
                room = session.query(Room).filter_by(room_id=booking.room_id).first()
                if room:
                    room.status = 'cleaning'
                
                session.commit()
                
                return True, f"Guest checked out successfully at {booking.actual_check_out.strftime('%H:%M')}"
        
        except Exception as e:
            return False, f"Check-out failed: {str(e)}"
    
    @staticmethod
    def search_booking(search_term):
        """
        Search for bookings by reference, guest name, email, or room number.
        """
        try:
            with get_db_session() as session:
                # Get all confirmed bookings
                bookings = session.query(Booking).filter(
                    Booking.booking_status == 'confirmed'
                ).all()
                
                results = []
                search_lower = search_term.lower().strip()
                
                for booking in bookings:
                    user = session.query(User).filter_by(user_id=booking.user_id).first()
                    room = session.query(Room).filter_by(room_id=booking.room_id).first()
                    
                    # Check if search term matches any field
                    matches = False
                    
                    # Check booking reference
                    if search_lower in booking.booking_reference.lower():
                        matches = True
                    
                    # Check guest name and email
                    if user:
                        if (search_lower in user.first_name.lower() or 
                            search_lower in user.last_name.lower() or
                            search_lower in user.email.lower()):
                            matches = True
                    
                    # Check room number
                    if room and search_lower in room.room_number.lower():
                        matches = True
                    
                    # If matches, add to results
                    if matches:
                        results.append({
                            'booking_id': booking.booking_id,
                            'booking_reference': booking.booking_reference,
                            'guest_name': f"{user.first_name} {user.last_name}" if user else 'N/A',
                            'guest_email': user.email if user else 'N/A',
                            'room_number': room.room_number if room else 'N/A',
                            'room_type': room.room_type if room else 'N/A',
                            'check_in_date': booking.check_in_date,
                            'check_out_date': booking.check_out_date,
                            'booking_status': booking.booking_status,
                            'actual_check_in': booking.actual_check_in,
                            'actual_check_out': booking.actual_check_out,
                            'id_verified': booking.id_verified
                        })
                
                return results
                
        except Exception as e:
            print(f"Search error: {e}")
            return []

