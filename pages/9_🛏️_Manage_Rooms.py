"""
Room management page - COMPLETE FIXED VERSION
Add, edit, and delete rooms.
"""
import streamlit as st
from backend.room.room_manager import RoomManager
from database.db_manager import get_db_session
from database.models import Room
from utils.helpers import format_currency
from utils.constants import RoomStatus
import config

st.set_page_config(page_title="Manage Rooms", page_icon="🛏️", layout="wide")

if not st.session_state.get('is_admin', False):
    st.error("❌ Admin access required")
    st.stop()

st.title("🛏️ Room Management")

tab1, tab2, tab3 = st.tabs(["📋 View Rooms", "➕ Add Room", "✏️ Edit Room"])

# ===== TAB 1: VIEW ROOMS =====
with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_type = st.selectbox("Type", ["All"] + list(config.ROOM_TYPES.keys()), key="view_type")
    with col2:
        filter_status = st.selectbox("Status", ["All"] + RoomStatus.get_all(), key="view_status")
    with col3:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    # ✅ FIX 1: Extract all data within session before accessing
    with get_db_session() as session:
        query = session.query(Room)
        if filter_type != "All":
            query = query.filter_by(room_type=filter_type)
        if filter_status != "All":
            query = query.filter_by(status=filter_status)
        rooms = query.all()
        
        # ✅ CRITICAL: Extract to dictionaries WITHIN session
        rooms_data = []
        for room in rooms:
            rooms_data.append({
                'room_id': room.room_id,
                'room_number': room.room_number,
                'room_type': room.room_type,
                'capacity': room.capacity,
                'floor_number': room.floor_number,
                'view_type': room.view_type,
                'description': room.description,
                'base_price_per_night': room.base_price_per_night,
                'status': room.status
            })
    
    # ✅ Now use dictionaries OUTSIDE session
    if not rooms_data:
        st.info("No rooms found")
    else:
        st.success(f"Found {len(rooms_data)} room(s)")
        st.markdown("---")
        
        for room in rooms_data:
            with st.expander(f"🏨 Room {room['room_number']} - {room['room_type']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Type:** {room['room_type']}")
                    st.write(f"**Capacity:** {room['capacity']} guests")
                    st.write(f"**Floor:** {room['floor_number']}")
                    st.write(f"**View:** {room['view_type']}")
                with col2:
                    st.write(f"**Price:** {format_currency(room['base_price_per_night'])}/night")
                    st.write(f"**Status:** {room['status']}")
                    st.write(f"**Description:** {room['description']}")

# ===== TAB 2: ADD ROOM =====
with tab2:
    with st.form("add_room"):
        col1, col2 = st.columns(2)
        with col1:
            room_number = st.text_input("Room Number *", key="add_room_number")
            room_type = st.selectbox("Type *", list(config.ROOM_TYPES.keys()), key="add_type")
            capacity = st.number_input("Capacity *", min_value=1, value=2, key="add_capacity")
            price = st.number_input("Price/Night *", min_value=0.0, value=50.0, step=10.0, key="add_price")
        with col2:
            floor = st.number_input("Floor *", min_value=1, value=1, key="add_floor")
            view = st.selectbox("View", ["City", "Garden", "Sea", "Mountain"], key="add_view")
            status = st.selectbox("Status", RoomStatus.get_all(), key="add_status")
        
        description = st.text_area("Description", key="add_description")
        amenities = st.multiselect("Amenities", [
            "WiFi", "TV", "AC", "Mini Fridge", "Coffee Maker", 
            "Balcony", "Bathtub", "Room Service", "Safe"
        ], key="add_amenities")
        
        if st.form_submit_button("✅ Add Room", use_container_width=True, type="primary"):
            if not room_number:
                st.error("❌ Room number required")
            else:
                success, message = RoomManager.create_room(
                    room_number, room_type, capacity, price, 
                    description, amenities, floor, view, status
                )
                if success:
                    st.success(f"✅ {message}")
                    st.balloons()
                else:
                    st.error(f"❌ {message}")

# ===== TAB 3: EDIT ROOM =====
with tab3:
    # ✅ FIX 2: Extract room data within session
    with get_db_session() as session:
        all_rooms = session.query(Room).all()
        
        # ✅ Extract to dictionaries within session
        rooms_dict = {}
        for r in all_rooms:
            rooms_dict[f"Room {r.room_number} - {r.room_type}"] = {
                'room_id': r.room_id,
                'room_number': r.room_number,
                'room_type': r.room_type,
                'capacity': r.capacity,
                'floor_number': r.floor_number,
                'view_type': r.view_type,
                'description': r.description,
                'base_price_per_night': r.base_price_per_night,
                'status': r.status
            }
    
    if not rooms_dict:
        st.info("No rooms to edit")
    else:
        selected = st.selectbox("Select Room", list(rooms_dict.keys()), key="edit_room_select")
        room_data = rooms_dict[selected]  # ✅ Use dictionary
        
        with st.form("edit_room"):
            col1, col2 = st.columns(2)
            with col1:
                new_number = st.text_input("Room Number", value=room_data['room_number'], key="edit_number")
                new_type = st.selectbox(
                    "Type", 
                    list(config.ROOM_TYPES.keys()), 
                    index=list(config.ROOM_TYPES.keys()).index(room_data['room_type']),
                    key="edit_type"
                )
                new_capacity = st.number_input("Capacity", min_value=1, value=room_data['capacity'], key="edit_capacity")
                new_price = st.number_input(
                    "Price/Night", 
                    min_value=0.0, 
                    value=float(room_data['base_price_per_night']),
                    key="edit_price"
                )
            with col2:
                new_floor = st.number_input("Floor", min_value=1, value=room_data['floor_number'], key="edit_floor")
                
                # ✅ Safe view index selection
                view_list = ["City", "Garden", "Sea", "Mountain"]
                view_index = view_list.index(room_data['view_type']) if room_data['view_type'] in view_list else 0
                new_view = st.selectbox(
                    "View", 
                    view_list,
                    index=view_index,
                    key="edit_view"
                )
                
                # ✅ Safe status index selection
                status_list = RoomStatus.get_all()
                status_index = status_list.index(room_data['status']) if room_data['status'] in status_list else 0
                new_status = st.selectbox(
                    "Status", 
                    status_list,
                    index=status_index,
                    key="edit_status"
                )
            
            new_desc = st.text_area("Description", value=room_data['description'] or "", key="edit_description")
            
            if st.form_submit_button("💾 Update Room", use_container_width=True, type="primary"):
                success, message = RoomManager.update_room(
                    room_data['room_id'],
                    room_number=new_number,
                    room_type=new_type,
                    capacity=new_capacity,
                    base_price_per_night=new_price,
                    floor_number=new_floor,
                    view_type=new_view,
                    status=new_status,
                    description=new_desc
                )
                if success:
                    st.success(f"✅ {message}")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")

# ===== LOGOUT BUTTON =====
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 1])
with col3:
    if st.button("🚪 Logout", use_container_width=True, type="secondary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
