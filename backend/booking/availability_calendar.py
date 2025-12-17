"""
Room Availability Calendar Manager
Provides calendar-based availability data
"""
from database.db_manager import get_db_session
from database.models import Room, Booking
from datetime import datetime, timedelta
from collections import defaultdict


class AvailabilityCalendar:
    """Manage calendar-based room availability"""
    
    @staticmethod
    def get_month_availability(year, month, room_type=None):
        """
        Get availability for all rooms for a specific month.
        
        Returns dict with:
        - dates: list of all dates in month
        - rooms: list of rooms with daily availability
        """
        try:
            from calendar import monthrange
            
            # Get number of days in month
            _, num_days = monthrange(year, month)
            
            # Generate all dates in month
            dates = []
            for day in range(1, num_days + 1):
                dates.append(datetime(year, month, day))
            
            with get_db_session() as session:
                # Get rooms
                query = session.query(Room)
                if room_type:
                    query = query.filter(Room.room_type == room_type)
                
                rooms = query.all()
                
                # Get all bookings for this month
                start_date = datetime(year, month, 1)
                if month == 12:
                    end_date = datetime(year + 1, 1, 1)
                else:
                    end_date = datetime(year, month + 1, 1)
                
                bookings = session.query(Booking).filter(
                    Booking.booking_status.in_(['confirmed', 'pending']),
                    Booking.check_out_date > start_date,
                    Booking.check_in_date < end_date
                ).all()
                
                # Build availability map
                room_availability = []
                
                for room in rooms:
                    # Get bookings for this room
                    room_bookings = [b for b in bookings if b.room_id == room.room_id]
                    
                    # Check each date
                    daily_status = {}
                    for date in dates:
                        # Check if booked on this date
                        is_booked = False
                        booking_status = None
                        
                        for booking in room_bookings:
                            if booking.check_in_date.date() <= date.date() < booking.check_out_date.date():
                                is_booked = True
                                booking_status = booking.booking_status
                                break
                        
                        if is_booked:
                            daily_status[date.strftime('%Y-%m-%d')] = {
                                'status': 'booked' if booking_status == 'confirmed' else 'pending',
                                'available': False
                            }
                        else:
                            daily_status[date.strftime('%Y-%m-%d')] = {
                                'status': 'available',
                                'available': True
                            }
                    
                    room_availability.append({
                        'room_id': room.room_id,
                        'room_number': room.room_number,
                        'room_type': room.room_type,
                        'daily_status': daily_status
                    })
                
                return {
                    'year': year,
                    'month': month,
                    'dates': [d.strftime('%Y-%m-%d') for d in dates],
                    'rooms': room_availability
                }
                
        except Exception as e:
            print(f"Error getting month availability: {e}")
            return None
    
    @staticmethod
    def get_room_availability_range(room_id, start_date, end_date):
        """
        Check if a specific room is available for a date range.
        Returns (available: bool, conflicting_bookings: list)
        """
        try:
            with get_db_session() as session:
                conflicts = session.query(Booking).filter(
                    Booking.room_id == room_id,
                    Booking.booking_status.in_(['confirmed', 'pending']),
                    Booking.check_out_date > start_date,
                    Booking.check_in_date < end_date
                ).all()
                
                if conflicts:
                    conflict_list = [{
                        'booking_reference': b.booking_reference,
                        'check_in': b.check_in_date,
                        'check_out': b.check_out_date,
                        'status': b.booking_status
                    } for b in conflicts]
                    return False, conflict_list
                
                return True, []
                
        except Exception as e:
            print(f"Error checking availability: {e}")
            return False, []
    
    @staticmethod
    def get_available_dates_for_room(room_id, start_date, num_days=30):
        """
        Get list of available dates for a room starting from start_date.
        Useful for suggesting alternative dates.
        """
        try:
            available_dates = []
            
            with get_db_session() as session:
                for i in range(num_days):
                    check_date = start_date + timedelta(days=i)
                    next_date = check_date + timedelta(days=1)
                    
                    # Check if available on this date
                    conflicts = session.query(Booking).filter(
                        Booking.room_id == room_id,
                        Booking.booking_status.in_(['confirmed', 'pending']),
                        Booking.check_out_date > check_date,
                        Booking.check_in_date < next_date
                    ).count()
                    
                    if conflicts == 0:
                        available_dates.append(check_date.strftime('%Y-%m-%d'))
                
                return available_dates
                
        except Exception as e:
            print(f"Error getting available dates: {e}")
            return []
