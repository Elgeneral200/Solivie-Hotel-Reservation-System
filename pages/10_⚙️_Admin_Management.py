"""
Admin Management - Room & User Management
Merged: Manage Rooms + Manage Users functionality
Enhanced with Dark Luxury Theme
"""
import streamlit as st
from backend.room.room_manager import RoomManager
from database.db_manager import get_db_session
from database.models import Room, User, Booking
from utils.ui_components import SolivieUI
from utils.helpers import format_currency
from utils.constants import RoomStatus
from datetime import date
import config


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Admin Management - Solivie Hotel",
    page_icon="⚙️",
    layout="wide"
)

# Apply dark luxury CSS
SolivieUI.inject_custom_css()

# Additional management-specific styling
st.markdown("""
<style>
/* ===== ROOM CARDS ===== */
.room-card {
    background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
    padding: 1.5rem;
    border-radius: 15px;
    border: 2px solid #3D4A47;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.room-card:hover {
    border-color: #C4935B;
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(196, 147, 91, 0.3);
}

/* ===== USER CARDS ===== */
.user-card {
    background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
    padding: 1.5rem;
    border-radius: 15px;
    border: 2px solid #3D4A47;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.user-card:hover {
    border-color: #7B9CA8;
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(123, 156, 168, 0.3);
}

/* ===== INFO SECTIONS ===== */
.info-section {
    background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
    padding: 1.25rem;
    border-radius: 12px;
    border: 2px solid #3D4A47;
    margin-bottom: 1rem;
}

.section-title {
    color: #C4935B;
    font-size: 1.1rem;
    font-weight: 700;
    margin: 0 0 1rem 0;
}

/* ===== STATUS BADGES ===== */
.status-available {
    background: rgba(107, 142, 126, 0.2);
    color: #6B8E7E;
    border: 2px solid #6B8E7E;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-weight: 700;
    display: inline-block;
}

.status-occupied {
    background: rgba(169, 95, 95, 0.2);
    color: #D4A76A;
    border: 2px solid #A95F5F;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-weight: 700;
    display: inline-block;
}

.status-maintenance {
    background: rgba(196, 147, 91, 0.2);
    color: #C4935B;
    border: 2px solid #C4935B;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-weight: 700;
    display: inline-block;
}

/* ===== ID EXPIRY WARNING ===== */
.id-expired {
    background: rgba(169, 95, 95, 0.3);
    border: 2px solid #A95F5F;
    padding: 1rem;
    border-radius: 10px;
    color: #D4A76A;
    font-weight: 700;
    text-align: center;
}

.id-expiring-soon {
    background: rgba(196, 147, 91, 0.3);
    border: 2px solid #C4935B;
    padding: 1rem;
    border-radius: 10px;
    color: #C4935B;
    font-weight: 700;
    text-align: center;
}

.id-valid {
    background: rgba(107, 142, 126, 0.2);
    border: 2px solid #6B8E7E;
    padding: 1rem;
    border-radius: 10px;
    color: #6B8E7E;
    font-weight: 700;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# ============================================================================
# ADMIN ACCESS CHECK
# ============================================================================

if not st.session_state.get('is_admin', False):
    st.markdown("""
    <div style='background: linear-gradient(145deg, #3D2A2A 0%, #2C2020 100%);
                padding: 3rem 2rem;
                border-radius: 15px;
                text-align: center;
                border: 2px solid #A95F5F;
                margin: 2rem 0;'>
        <h1 style='color: #D4A76A; margin: 0 0 1rem 0; font-size: 3rem;'>🔒</h1>
        <h2 style='color: #D4A76A; margin: 0 0 1rem 0;'>Admin Access Required</h2>
        <p style='color: #F5F5F0; font-size: 1.1rem; margin: 0;'>
            You need administrator privileges to access management tools
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 LOGIN AS ADMIN", use_container_width=True, type="primary", key="mgmt_login"):
            st.switch_page("pages/2_🔐_Login.py")
    with col2:
        if st.button("🏠 HOME", use_container_width=True, type="secondary", key="mgmt_home"):
            st.switch_page("app.py")
    st.stop()


# ============================================================================
# PAGE HEADER
# ============================================================================

SolivieUI.page_header(
    "Admin Management Center",
    "Comprehensive room management & user administration",
    "⚙️"
)


# ============================================================================
# MAIN TABS
# ============================================================================

tab1, tab2 = st.tabs(["🛏️ Manage Rooms", "👥 Manage Users"])


# ============================================================================
# TAB 1: MANAGE ROOMS
# ============================================================================

with tab1:
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 2rem;'>
        <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
            🛏️ Room Management System
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Sub-tabs
    room_tab1, room_tab2, room_tab3 = st.tabs(["📋 View Rooms", "➕ Add Room", "✏️ Edit Room"])
    
    # ===== SUB-TAB 1: VIEW ROOMS =====
    with room_tab1:
        st.markdown("""
        <div class='solivie-card' style='margin-bottom: 1.5rem;'>
            <h4 style='color: #C4935B; margin: 0;'>📋 All Rooms Overview</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_type = st.selectbox(
                "🏨 Filter by Type",
                ["All"] + list(config.ROOM_TYPES.keys()),
                key="view_type_filter"
            )
        
        with col2:
            filter_status = st.selectbox(
                "🎯 Filter by Status",
                ["All"] + RoomStatus.get_all(),
                key="view_status_filter"
            )
        
        with col3:
            st.markdown("<div style='height: 1.75rem;'></div>", unsafe_allow_html=True)
            if st.button("🔄 REFRESH", use_container_width=True, type="secondary", key="refresh_rooms"):
                st.rerun()
        
        # Get rooms
        with st.spinner("🛏️ Loading rooms..."):
            with get_db_session() as session:
                query = session.query(Room)
                
                if filter_type != "All":
                    query = query.filter_by(room_type=filter_type)
                if filter_status != "All":
                    query = query.filter_by(status=filter_status)
                
                rooms = query.all()
                
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
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        # Display results
        if not rooms_data:
            st.markdown("""
            <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                        padding: 3rem 2rem;
                        border-radius: 15px;
                        text-align: center;
                        border: 2px solid #3D4A47;'>
                <h3 style='color: #C4935B; margin: 0 0 1rem 0;'>🛏️ No Rooms Found</h3>
                <p style='color: #9BA8A5; margin: 0;'>No rooms match your selected filters</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Summary metrics
            available_count = len([r for r in rooms_data if r['status'] == 'available'])
            occupied_count = len([r for r in rooms_data if r['status'] == 'occupied'])
            maintenance_count = len([r for r in rooms_data if r['status'] == 'maintenance'])
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                            padding: 1.5rem;
                            border-radius: 12px;
                            text-align: center;
                            border: 2px solid #C4935B;'>
                    <p style='color: #9BA8A5; margin: 0;'>📊 Total</p>
                    <p style='color: #C4935B; margin: 0.5rem 0 0 0; font-size: 2.5rem; font-weight: 700;'>{len(rooms_data)}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                            padding: 1.5rem;
                            border-radius: 12px;
                            text-align: center;
                            border: 2px solid #6B8E7E;'>
                    <p style='color: #9BA8A5; margin: 0;'>✅ Available</p>
                    <p style='color: #6B8E7E; margin: 0.5rem 0 0 0; font-size: 2.5rem; font-weight: 700;'>{available_count}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                            padding: 1.5rem;
                            border-radius: 12px;
                            text-align: center;
                            border: 2px solid #A95F5F;'>
                    <p style='color: #9BA8A5; margin: 0;'>🔴 Occupied</p>
                    <p style='color: #D4A76A; margin: 0.5rem 0 0 0; font-size: 2.5rem; font-weight: 700;'>{occupied_count}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                            padding: 1.5rem;
                            border-radius: 12px;
                            text-align: center;
                            border: 2px solid #C4935B;'>
                    <p style='color: #9BA8A5; margin: 0;'>🔧 Maintenance</p>
                    <p style='color: #C4935B; margin: 0.5rem 0 0 0; font-size: 2.5rem; font-weight: 700;'>{maintenance_count}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
            
            # Display each room
            for room in rooms_data:
                # Status styling
                if room['status'] == 'available':
                    status_class = 'status-available'
                    status_emoji = '✅'
                elif room['status'] == 'occupied':
                    status_class = 'status-occupied'
                    status_emoji = '🔴'
                elif room['status'] == 'maintenance':
                    status_class = 'status-maintenance'
                    status_emoji = '🔧'
                else:
                    status_class = 'status-maintenance'
                    status_emoji = '🟡'
                
                with st.expander(
                    f"{status_emoji} Room {room['room_number']} - {room['room_type']} • {room['status'].upper()}",
                    expanded=False
                ):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("""
                        <div class='info-section'>
                            <p class='section-title'>🏨 Room Details</p>
                        """, unsafe_allow_html=True)
                        st.write(f"**Room Number:** {room['room_number']}")
                        st.write(f"**Type:** {room['room_type']}")
                        st.write(f"**Capacity:** {room['capacity']} guests")
                        st.write(f"**Floor:** {room['floor_number']}")
                        st.write(f"**View:** {room['view_type']}")
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("""
                        <div class='info-section'>
                            <p class='section-title'>💰 Pricing & Status</p>
                        """, unsafe_allow_html=True)
                        st.write(f"**Price per Night:** {format_currency(room['base_price_per_night'])}")
                        st.markdown(f"<span class='{status_class}'>{status_emoji} {room['status'].upper()}</span>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    if room['description']:
                        st.markdown(f"""
                        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                                    padding: 1.25rem;
                                    border-radius: 10px;
                                    border: 2px solid #7B9CA8;
                                    margin-top: 1rem;'>
                            <p style='color: #7B9CA8; margin: 0 0 0.5rem 0; font-weight: 600;'>📝 Description:</p>
                            <p style='color: #F5F5F0; margin: 0;'>{room['description']}</p>
                        </div>
                        """, unsafe_allow_html=True)
    
    # ===== SUB-TAB 2: ADD ROOM =====
    with room_tab2:
        st.markdown("""
        <div class='solivie-card' style='margin-bottom: 1.5rem;'>
            <h4 style='color: #C4935B; margin: 0;'>➕ Add New Room to Inventory</h4>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("add_room_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                room_number = st.text_input(
                    "🔢 Room Number *",
                    key="add_room_number",
                    placeholder="101"
                )
                
                room_type = st.selectbox(
                    "🏨 Room Type *",
                    list(config.ROOM_TYPES.keys()),
                    key="add_room_type"
                )
                
                capacity = st.number_input(
                    "👥 Guest Capacity *",
                    min_value=1,
                    max_value=10,
                    value=2,
                    key="add_capacity"
                )
                
                price = st.number_input(
                    "💰 Price per Night ($) *",
                    min_value=0.0,
                    value=100.0,
                    step=10.0,
                    key="add_price"
                )
            
            with col2:
                floor = st.number_input(
                    "🏢 Floor Number *",
                    min_value=1,
                    max_value=20,
                    value=1,
                    key="add_floor"
                )
                
                view = st.selectbox(
                    "🌅 View Type",
                    ["City", "Garden", "Sea", "Mountain"],
                    key="add_view"
                )
                
                status = st.selectbox(
                    "🎯 Room Status",
                    RoomStatus.get_all(),
                    key="add_status"
                )
            
            description = st.text_area(
                "📝 Room Description",
                key="add_description",
                placeholder="Describe the room features and amenities...",
                height=100
            )
            
            amenities = st.multiselect(
                "✨ Room Amenities",
                [
                    "WiFi", "TV", "AC", "Mini Fridge", "Coffee Maker",
                    "Balcony", "Bathtub", "Room Service", "Safe", "Desk",
                    "Hair Dryer", "Iron", "Microwave", "Ocean View"
                ],
                key="add_amenities"
            )
            
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            
            submitted = st.form_submit_button(
                "✅ ADD ROOM",
                use_container_width=True,
                type="primary"
            )
            
            if submitted:
                if not room_number:
                    st.error("❌ Room number is required")
                else:
                    success, message = RoomManager.create_room(
                        room_number,
                        room_type,
                        capacity,
                        price,
                        description,
                        amenities,
                        floor,
                        view,
                        status
                    )
                    
                    if success:
                        st.success(f"✅ {message}")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
    
    # ===== SUB-TAB 3: EDIT ROOM =====
    with room_tab3:
        st.markdown("""
        <div class='solivie-card' style='margin-bottom: 1.5rem;'>
            <h4 style='color: #C4935B; margin: 0;'>✏️ Edit Existing Room</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Get all rooms for selection
        with get_db_session() as session:
            all_rooms = session.query(Room).order_by(Room.room_number).all()
            
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
            st.markdown("""
            <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                        padding: 2rem;
                        border-radius: 12px;
                        text-align: center;
                        border: 2px solid #3D4A47;'>
                <p style='color: #9BA8A5; margin: 0; font-size: 1.1rem;'>
                    📭 No rooms available to edit
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            selected = st.selectbox(
                "🏨 Select Room to Edit",
                list(rooms_dict.keys()),
                key="edit_room_select"
            )
            
            room_data = rooms_dict[selected]
            
            with st.form("edit_room_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_number = st.text_input(
                        "🔢 Room Number *",
                        value=room_data['room_number'],
                        key="edit_number"
                    )
                    
                    new_type = st.selectbox(
                        "🏨 Room Type *",
                        list(config.ROOM_TYPES.keys()),
                        index=list(config.ROOM_TYPES.keys()).index(room_data['room_type']),
                        key="edit_type"
                    )
                    
                    new_capacity = st.number_input(
                        "👥 Guest Capacity *",
                        min_value=1,
                        max_value=10,
                        value=room_data['capacity'],
                        key="edit_capacity"
                    )
                    
                    new_price = st.number_input(
                        "💰 Price per Night ($) *",
                        min_value=0.0,
                        value=float(room_data['base_price_per_night']),
                        step=10.0,
                        key="edit_price"
                    )
                
                with col2:
                    new_floor = st.number_input(
                        "🏢 Floor Number *",
                        min_value=1,
                        max_value=20,
                        value=room_data['floor_number'],
                        key="edit_floor"
                    )
                    
                    view_list = ["City", "Garden", "Sea", "Mountain"]
                    view_index = view_list.index(room_data['view_type']) if room_data['view_type'] in view_list else 0
                    new_view = st.selectbox(
                        "🌅 View Type",
                        view_list,
                        index=view_index,
                        key="edit_view"
                    )
                    
                    status_list = RoomStatus.get_all()
                    status_index = status_list.index(room_data['status']) if room_data['status'] in status_list else 0
                    new_status = st.selectbox(
                        "🎯 Room Status",
                        status_list,
                        index=status_index,
                        key="edit_status"
                    )
                
                new_desc = st.text_area(
                    "📝 Room Description",
                    value=room_data['description'] or "",
                    key="edit_description",
                    height=100
                )
                
                st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    update_btn = st.form_submit_button(
                        "💾 UPDATE ROOM",
                        use_container_width=True,
                        type="primary"
                    )
                
                with col_b:
                    delete_btn = st.form_submit_button(
                        "🗑️ DELETE ROOM",
                        use_container_width=True,
                        type="secondary"
                    )
                
                if update_btn:
                    if not new_number:
                        st.error("❌ Room number is required")
                    else:
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
                
                if delete_btn:
                    st.warning("⚠️ Delete functionality requires confirmation. Contact developer for safe deletion implementation.")


# ============================================================================
# TAB 2: MANAGE USERS
# ============================================================================

with tab2:
    st.markdown("""
    <div class='solivie-card' style='margin-bottom: 2rem;'>
        <h3 style='color: #C4935B; margin: 0; font-size: 1.5rem;'>
            👥 User Management & ID Verification
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Search bar
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search = st.text_input(
            "🔍 Search by name or email",
            key="user_search",
            placeholder="Enter name or email..."
        )
    
    with col2:
        st.markdown("<div style='height: 1.75rem;'></div>", unsafe_allow_html=True)
        if st.button("🔄 REFRESH", use_container_width=True, type="secondary", key="refresh_users"):
            st.rerun()
    
    # Get users
    with st.spinner("👥 Loading users..."):
        with get_db_session() as session:
            query = session.query(User)
            
            if search:
                query = query.filter(
                    (User.first_name.contains(search)) |
                    (User.last_name.contains(search)) |
                    (User.email.contains(search))
                )
            
            users = query.order_by(User.created_at.desc()).all()
            
            users_data = []
            for user in users:
                booking_count = session.query(Booking).filter_by(user_id=user.user_id).count()
                
                users_data.append({
                    'user_id': user.user_id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'phone_number': user.phone_number or 'N/A',
                    'address': user.address or 'N/A',
                    'city': user.city or 'N/A',
                    'country': user.country or 'N/A',
                    'national_id': user.national_id,
                    'passport_number': user.passport_number,
                    'nationality': user.nationality,
                    'date_of_birth': user.date_of_birth,
                    'id_expiry_date': user.id_expiry_date,
                    'loyalty_points': user.loyalty_points,
                    'account_status': user.account_status,
                    'created_at': user.created_at,
                    'booking_count': booking_count
                })
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Display results
    if not users_data:
        st.markdown("""
        <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                    padding: 3rem 2rem;
                    border-radius: 15px;
                    text-align: center;
                    border: 2px solid #3D4A47;'>
            <h3 style='color: #C4935B; margin: 0 0 1rem 0;'>👥 No Users Found</h3>
            <p style='color: #9BA8A5; margin: 0;'>No users match your search criteria</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Summary metrics
        active_users = len([u for u in users_data if u['account_status'] == 'active'])
        total_bookings = sum(u['booking_count'] for u in users_data)
        users_with_id = len([u for u in users_data if u['national_id'] or u['passport_number']])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                        padding: 1.5rem;
                        border-radius: 12px;
                        text-align: center;
                        border: 2px solid #7B9CA8;'>
                <p style='color: #9BA8A5; margin: 0;'>👥 Total Users</p>
                <p style='color: #7B9CA8; margin: 0.5rem 0 0 0; font-size: 2.5rem; font-weight: 700;'>{len(users_data)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                        padding: 1.5rem;
                        border-radius: 12px;
                        text-align: center;
                        border: 2px solid #6B8E7E;'>
                <p style='color: #9BA8A5; margin: 0;'>✅ Active</p>
                <p style='color: #6B8E7E; margin: 0.5rem 0 0 0; font-size: 2.5rem; font-weight: 700;'>{active_users}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                        padding: 1.5rem;
                        border-radius: 12px;
                        text-align: center;
                        border: 2px solid #C4935B;'>
                <p style='color: #9BA8A5; margin: 0;'>📋 Bookings</p>
                <p style='color: #C4935B; margin: 0.5rem 0 0 0; font-size: 2.5rem; font-weight: 700;'>{total_bookings}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style='background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
                        padding: 1.5rem;
                        border-radius: 12px;
                        text-align: center;
                        border: 2px solid #6B8E7E;'>
                <p style='color: #9BA8A5; margin: 0;'>🆔 With ID</p>
                <p style='color: #6B8E7E; margin: 0.5rem 0 0 0; font-size: 2.5rem; font-weight: 700;'>{users_with_id}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        
        # Display each user
        for data in users_data:
            # Calculate ID expiry warning
            id_warning = ""
            id_warning_emoji = ""
            if data['id_expiry_date']:
                days_until_expiry = (data['id_expiry_date'] - date.today()).days
                if days_until_expiry < 0:
                    id_warning = f" ⚠️ ID EXPIRED"
                    id_warning_emoji = "🔴"
                elif days_until_expiry < 30:
                    id_warning = f" ⚠️ Expires in {days_until_expiry} days"
                    id_warning_emoji = "🟡"
            
            # Account status emoji
            status_emoji = "✅" if data['account_status'] == 'active' else "🔴"
            
            with st.expander(
                f"{status_emoji} {data['first_name']} {data['last_name']} • {data['email']}{id_warning}",
                expanded=False
            ):
                # Row 1: Account & Location & Activity
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("""
                    <div class='info-section'>
                        <p class='section-title'>📧 Account Information</p>
                    """, unsafe_allow_html=True)
                    st.write(f"**Email:** {data['email']}")
                    st.write(f"**Phone:** {data['phone_number']}")
                    st.write(f"**Status:** {data['account_status'].upper()}")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div class='info-section'>
                        <p class='section-title'>📍 Location Details</p>
                    """, unsafe_allow_html=True)
                    st.write(f"**Address:** {data['address']}")
                    st.write(f"**City:** {data['city']}")
                    st.write(f"**Country:** {data['country']}")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col3:
                    st.markdown("""
                    <div class='info-section'>
                        <p class='section-title'>📊 Activity Statistics</p>
                    """, unsafe_allow_html=True)
                    st.write(f"**Loyalty Points:** {data['loyalty_points']}")
                    st.write(f"**Member Since:** {data['created_at'].strftime('%Y-%m-%d')}")
                    st.write(f"**Total Bookings:** {data['booking_count']}")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                
                # Row 2: ID Information
                st.markdown("""
                <div style='background: linear-gradient(145deg, #3D3528 0%, #2C2820 100%);
                            padding: 1.5rem;
                            border-radius: 15px;
                            border: 2px solid #C4935B;'>
                    <h4 style='color: #C4935B; margin: 0 0 1.5rem 0;'>🆔 Identification Information</h4>
                """, unsafe_allow_html=True)
                
                has_id = data['national_id'] or data['passport_number']
                
                if has_id:
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.write("**ID Document:**")
                        if data['national_id']:
                            st.write(f"🆔 National ID")
                            st.write(f"`{data['national_id']}`")
                        elif data['passport_number']:
                            st.write(f"🛂 Passport")
                            st.write(f"`{data['passport_number']}`")
                    
                    with col2:
                        st.write("**Nationality:**")
                        st.write(f"{data['nationality'] or 'N/A'}")
                    
                    with col3:
                        st.write("**Date of Birth:**")
                        if data['date_of_birth']:
                            st.write(f"{data['date_of_birth'].strftime('%Y-%m-%d')}")
                            age = (date.today() - data['date_of_birth']).days // 365
                            st.caption(f"Age: {age} years")
                        else:
                            st.write("N/A")
                    
                    with col4:
                        st.write("**ID Expiry Date:**")
                        if data['id_expiry_date']:
                            expiry_str = data['id_expiry_date'].strftime('%Y-%m-%d')
                            days_left = (data['id_expiry_date'] - date.today()).days
                            
                            if days_left < 0:
                                st.markdown(f"""
                                <div class='id-expired'>
                                    🔴 EXPIRED<br>{expiry_str}
                                </div>
                                """, unsafe_allow_html=True)
                            elif days_left < 30:
                                st.markdown(f"""
                                <div class='id-expiring-soon'>
                                    ⚠️ EXPIRES SOON<br>{expiry_str}<br>({days_left} days)
                                </div>
                                """, unsafe_allow_html=True)
                            elif days_left < 90:
                                st.markdown(f"""
                                <div class='id-valid'>
                                    ✅ VALID<br>{expiry_str}<br>({days_left} days left)
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.write(f"{expiry_str}")
                                st.caption(f"✅ Valid ({days_left} days left)")
                        else:
                            st.write("N/A")
                else:
                    st.markdown("""
                    <div style='background: rgba(169, 95, 95, 0.2);
                                border: 2px solid #A95F5F;
                                padding: 1.5rem;
                                border-radius: 10px;
                                text-align: center;'>
                        <p style='color: #D4A76A; margin: 0; font-weight: 700; font-size: 1.1rem;'>
                            ⚠️ No Identification Information on File
                        </p>
                        <p style='color: #9BA8A5; margin: 0.5rem 0 0 0; font-size: 0.9rem;'>
                            User may be required to provide ID documents at check-in
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)


# ============================================================================
# FOOTER NAVIGATION
# ============================================================================

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏠 HOME", use_container_width=True, type="secondary", key="footer_home"):
        st.switch_page("app.py")

with col2:
    if st.button("📊 DASHBOARD", use_container_width=True, type="secondary", key="footer_dashboard"):
        st.switch_page("pages/8_📊_Dashboard.py")

with col3:
    if st.button("🏨 OPERATIONS", use_container_width=True, type="secondary", key="footer_ops"):
        st.switch_page("pages/9_🏨_Admin_Operations.py")

with col4:
    if st.button("🚪 LOGOUT", use_container_width=True, type="secondary", key="footer_logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ============================================================================
# FOOTER
# ============================================================================

SolivieUI.footer()
