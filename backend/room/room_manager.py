"""
Room CRUD operations.
Manages room inventory and details.
"""

from database.db_manager import get_db_session, DatabaseManager
from database.models import Room
from sqlalchemy.orm import Session


class RoomManager:
    """Manages room operations."""
    
    @staticmethod
    def create_room(room_number, room_type, capacity, base_price, description, amenities, floor_number, view_type, status='available'):
        """Create new room."""
        try:
            with get_db_session() as session:
                existing = session.query(Room).filter_by(room_number=room_number).first()
                if existing:
                    return False, "Room number already exists"
                
                new_room = Room(
                    room_number=room_number,
                    room_type=room_type,
                    capacity=capacity,
                    base_price_per_night=base_price,
                    description=description,
                    amenities=amenities,
                    floor_number=floor_number,
                    view_type=view_type,
                    status=status,
                    images=[]
                )
                
                session.add(new_room)
                session.commit()
                
                return True, "Room created successfully"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def update_room(room_id, **kwargs):
        """Update room details."""
        try:
            with get_db_session() as session:
                room = session.query(Room).filter_by(room_id=room_id).first()
                if not room:
                    return False, "Room not found"
                
                for key, value in kwargs.items():
                    if hasattr(room, key):
                        setattr(room, key, value)
                
                session.commit()
                return True, "Room updated successfully"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def delete_room(room_id):
        """Delete room."""
        try:
            with get_db_session() as session:
                room = session.query(Room).filter_by(room_id=room_id).first()
                if not room:
                    return False, "Room not found"
                
                session.delete(room)
                session.commit()
                return True, "Room deleted successfully"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_room(room_id):
        """Get room by ID - returns fresh object from new session."""
        try:
            with get_db_session() as session:
                room = session.query(Room).filter_by(room_id=room_id).first()
                if room:
                    # ✅ FIX: Access all attributes within session to load them
                    _ = room.room_id
                    _ = room.room_number
                    _ = room.room_type
                    _ = room.capacity
                    _ = room.base_price_per_night
                    _ = room.description
                    _ = room.amenities
                    _ = room.floor_number
                    _ = room.view_type
                    _ = room.status
                    _ = room.images
                return room
        except Exception as e:
            print(f"Error getting room: {e}")
            return None
    
    @staticmethod
    def get_all_rooms(room_type=None, status=None):
        """Get all rooms with optional filters."""
        try:
            with get_db_session() as session:
                query = session.query(Room)
                
                if room_type:
                    query = query.filter_by(room_type=room_type)
                if status:
                    query = query.filter_by(status=status)
                
                rooms = query.all()
                
                # ✅ FIX: Force load all attributes
                result = []
                for room in rooms:
                    _ = room.room_id
                    _ = room.room_number
                    _ = room.room_type
                    _ = room.capacity
                    _ = room.base_price_per_night
                    result.append(room)
                
                return result
        except Exception as e:
            print(f"Error getting rooms: {e}")
            return []
