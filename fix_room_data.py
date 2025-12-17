"""
Fix existing room data - update view types and ensure amenities
"""
from database.db_manager import get_db_session
from database.models import Room
import config


def fix_rooms():
    """Update existing rooms with correct data"""
    
    # Map old view types to new ones
    view_map = {
        'City': 'City View',
        'Garden': 'Garden View',
        'Sea': 'Sea View'
    }
    
    try:
        with get_db_session() as session:
            rooms = session.query(Room).all()
            
            print(f"🔧 Fixing {len(rooms)} rooms...\n")
            
            for room in rooms:
                # Fix view type
                if room.view_type in view_map:
                    old_view = room.view_type
                    room.view_type = view_map[old_view]
                    print(f"✅ Room {room.room_number}: {old_view} → {room.view_type}")
                
                # Ensure amenities exist (from config)
                if room.room_type in config.ROOM_TYPES:
                    room_config = config.ROOM_TYPES[room.room_type]
                    
                    # If amenities is empty or None, add from config
                    if not room.amenities or len(room.amenities) == 0:
                        room.amenities = room_config.get('amenities', [])
                        print(f"   Added {len(room.amenities)} amenities")
                
                # Verify floor_number exists
                if not room.floor_number:
                    # Extract from room number (101 = floor 1)
                    try:
                        floor = int(room.room_number[0])
                        room.floor_number = floor if floor > 0 else 1
                        print(f"   Set floor to {room.floor_number}")
                    except:
                        room.floor_number = 1
            
            session.commit()
            print(f"\n🎉 Successfully fixed {len(rooms)} rooms!")
            
            # Show summary
            print("\n📊 SUMMARY:")
            views = {}
            for room in rooms:
                views[room.view_type] = views.get(room.view_type, 0) + 1
            
            for view, count in views.items():
                print(f"  {view}: {count} rooms")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("🔧 FIXING ROOM DATA")
    print("=" * 60 + "\n")
    fix_rooms()
    print("\n" + "=" * 60)
    print("✅ DONE! Refresh your search page now!")
    print("=" * 60)
