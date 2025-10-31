"""
Room inventory tracking.
Manages room status and availability.
"""

from database.db_manager import get_db_session
from database.models import Room


class InventoryManager:
    """Manages room inventory."""
    
    @staticmethod
    def update_room_status(room_id, new_status):
        """Update room status (available, occupied, maintenance, cleaning)."""
        try:
            with get_db_session() as session:
                room = session.query(Room).filter_by(room_id=room_id).first()
                if not room:
                    return False, "Room not found"
                
                room.status = new_status
                session.commit()
                return True, f"Room status updated to {new_status}"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_inventory_summary():
        """Get summary of room inventory by status."""
        try:
            with get_db_session() as session:
                rooms = session.query(Room).all()
                
                summary = {
                    'total': len(rooms),
                    'available': sum(1 for r in rooms if r.status == 'available'),
                    'occupied': sum(1 for r in rooms if r.status == 'occupied'),
                    'maintenance': sum(1 for r in rooms if r.status == 'maintenance'),
                    'cleaning': sum(1 for r in rooms if r.status == 'cleaning')
                }
                
                return summary
        except:
            return {}
    
    @staticmethod
    def get_rooms_by_floor(floor_number):
        """Get all rooms on specific floor."""
        try:
            with get_db_session() as session:
                return session.query(Room).filter_by(floor_number=floor_number).all()
        except:
            return []
