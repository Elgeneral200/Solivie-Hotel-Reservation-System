"""
Advanced room filtering system
"""
from database.db_manager import get_db_session
from database.models import Room, Booking
from datetime import datetime


class AdvancedFilter:
    """Handle advanced room filtering"""
    
    @staticmethod
    def filter_rooms(
        check_in=None,
        check_out=None,
        min_price=None,
        max_price=None,
        room_types=None,
        amenities=None,
        floor_numbers=None,
        view_types=None,
        min_capacity=1,
        sort_by='price_low'
    ):
        """
        Advanced room filtering with multiple criteria.
        
        Returns list of rooms matching all filters.
        """
        try:
            with get_db_session() as session:
                # Base query - available rooms
                query = session.query(Room).filter(Room.status == 'available')
                
                # Price filters - FIXED: use base_price_per_night
                if min_price is not None:
                    query = query.filter(Room.base_price_per_night >= min_price)
                if max_price is not None:
                    query = query.filter(Room.base_price_per_night <= max_price)
                
                # Room type filter
                if room_types and len(room_types) > 0:
                    query = query.filter(Room.room_type.in_(room_types))
                
                # View type filter
                if view_types and len(view_types) > 0:
                    query = query.filter(Room.view_type.in_(view_types))
                
                # Floor filter
                if floor_numbers and len(floor_numbers) > 0:
                    query = query.filter(Room.floor_number.in_(floor_numbers))
                
                # Capacity filter
                if min_capacity:
                    query = query.filter(Room.capacity >= min_capacity)
                
                rooms = query.all()
                
                # Convert to dict
                results = []
                for room in rooms:
                    # Check availability for dates if provided
                    if check_in and check_out:
                        # Check for conflicts
                        conflicts = session.query(Booking).filter(
                            Booking.room_id == room.room_id,
                            Booking.booking_status.in_(['confirmed', 'pending']),
                            Booking.check_out_date > check_in,
                            Booking.check_in_date < check_out
                        ).count()
                        
                        if conflicts > 0:
                            continue  # Skip unavailable rooms
                    
                    # Amenity filtering (JSON column - no need for json.loads)
                    if amenities and len(amenities) > 0:
                        room_amenities = room.amenities if room.amenities else []
                        # Check if room has ALL selected amenities
                        if not all(amenity in room_amenities for amenity in amenities):
                            continue
                    
                    # FIXED: use base_price_per_night
                    results.append({
                        'room_id': room.room_id,
                        'room_number': room.room_number,
                        'room_type': room.room_type,
                        'base_price': room.base_price_per_night,
                        'capacity': room.capacity,
                        'floor_number': room.floor_number,
                        'view_type': room.view_type,
                        'description': room.description,
                        'amenities': room.amenities if room.amenities else [],
                        'status': room.status
                    })
                
                # Sort results
                if sort_by == 'price_low':
                    results.sort(key=lambda x: x['base_price'])
                elif sort_by == 'price_high':
                    results.sort(key=lambda x: x['base_price'], reverse=True)
                elif sort_by == 'capacity':
                    results.sort(key=lambda x: x['capacity'], reverse=True)
                elif sort_by == 'room_number':
                    results.sort(key=lambda x: x['room_number'])
                
                return results
                
        except Exception as e:
            print(f"Filter error: {e}")
            return []
    
    @staticmethod
    def get_filter_options():
        """Get all available filter options from database"""
        try:
            with get_db_session() as session:
                rooms = session.query(Room).all()
                
                room_types = list(set([r.room_type for r in rooms]))
                view_types = list(set([r.view_type for r in rooms if r.view_type]))
                floors = sorted(list(set([r.floor_number for r in rooms if r.floor_number])))
                
                # Get price range - FIXED: use base_price_per_night
                prices = [r.base_price_per_night for r in rooms]
                min_price = min(prices) if prices else 0
                max_price = max(prices) if prices else 1000
                
                # Get all amenities (JSON column - direct access)
                all_amenities = set()
                for room in rooms:
                    if room.amenities:
                        all_amenities.update(room.amenities)
                
                return {
                    'room_types': room_types,
                    'view_types': view_types,
                    'floors': floors,
                    'min_price': min_price,
                    'max_price': max_price,
                    'amenities': sorted(list(all_amenities))
                }
        except Exception as e:
            print(f"Error getting filter options: {e}")
            return {}
