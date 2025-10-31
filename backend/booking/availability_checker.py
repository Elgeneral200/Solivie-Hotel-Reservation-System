"""
Room availability checking logic.
Checks if rooms are available for given date ranges.
"""

from datetime import datetime, timedelta
from database.db_manager import get_db_session
from database.models import Room, Booking
from sqlalchemy import and_, or_


class AvailabilityChecker:
    """Checks room availability."""
    
    @staticmethod
    def is_room_available(room_id, check_in, check_out):
        """Check if specific room is available."""
        try:
            with get_db_session() as session:
                room = session.query(Room).filter_by(room_id=room_id).first()
                if not room or room.status != 'available':
                    return False
                
                conflicts = session.query(Booking).filter(
                    and_(
                        Booking.room_id == room_id,
                        Booking.booking_status.in_(['confirmed', 'pending']),
                        or_(
                            and_(Booking.check_in_date <= check_in, Booking.check_out_date > check_in),
                            and_(Booking.check_in_date < check_out, Booking.check_out_date >= check_out),
                            and_(Booking.check_in_date >= check_in, Booking.check_out_date <= check_out)
                        )
                    )
                ).first()
                
                return conflicts is None
        except:
            return False
    
    @staticmethod
    def get_available_rooms(check_in, check_out, room_type=None, capacity=None):
        """
        Get all available room IDs for date range.
        Returns list of dictionaries with room data (not objects).
        """
        try:
            with get_db_session() as session:
                query = session.query(Room).filter(Room.status == 'available')
                
                if room_type:
                    query = query.filter_by(room_type=room_type)
                if capacity:
                    query = query.filter(Room.capacity >= capacity)
                
                all_rooms = query.all()
                
                # ✅ FIX: Extract data and check availability WITHIN session
                available = []
                for room in all_rooms:
                    # Check conflicts
                    conflicts = session.query(Booking).filter(
                        and_(
                            Booking.room_id == room.room_id,
                            Booking.booking_status.in_(['confirmed', 'pending']),
                            or_(
                                and_(Booking.check_in_date <= check_in, Booking.check_out_date > check_in),
                                and_(Booking.check_in_date < check_out, Booking.check_out_date >= check_out),
                                and_(Booking.check_in_date >= check_in, Booking.check_out_date <= check_out)
                            )
                        )
                    ).first()
                    
                    if not conflicts:
                        # ✅ FIX: Return dictionary with room data, not object
                        available.append({
                            'room_id': room.room_id,
                            'room_number': room.room_number,
                            'room_type': room.room_type,
                            'capacity': room.capacity,
                            'floor_number': room.floor_number,
                            'view_type': room.view_type,
                            'description': room.description,
                            'base_price': room.base_price_per_night,
                            'status': room.status
                        })
                
                return available
                
        except Exception as e:
            print(f"Error in get_available_rooms: {e}")
            return []
    
    @staticmethod
    def get_occupancy_rate(start_date, end_date):
        """Calculate occupancy rate percentage."""
        try:
            with get_db_session() as session:
                total_rooms = session.query(Room).filter_by(status='available').count()
                if total_rooms == 0:
                    return 0.0
                
                num_days = (end_date - start_date).days
                if num_days == 0:
                    num_days = 1
                total_room_nights = total_rooms * num_days
                
                bookings = session.query(Booking).filter(
                    and_(
                        Booking.booking_status.in_(['confirmed', 'checked_in']),
                        Booking.check_in_date < end_date,
                        Booking.check_out_date > start_date
                    )
                ).all()
                
                booked_nights = 0
                for booking in bookings:
                    overlap_start = max(booking.check_in_date, start_date)
                    overlap_end = min(booking.check_out_date, end_date)
                    nights = (overlap_end - overlap_start).days
                    if nights > 0:
                        booked_nights += nights
                
                occupancy = (booked_nights / total_room_nights) * 100 if total_room_nights > 0 else 0
                return round(occupancy, 2)
        except Exception as e:
            print(f"Error calculating occupancy: {e}")
            return 0.0
