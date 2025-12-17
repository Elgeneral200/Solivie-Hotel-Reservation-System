"""
Shopping cart manager for multiple room bookings
"""
from datetime import datetime


class CartManager:
    """Manage shopping cart for multiple room bookings"""
    
    @staticmethod
    def init_cart(session_state):
        """Initialize cart in session state"""
        if 'cart' not in session_state:
            session_state.cart = []
        if 'cart_check_in' not in session_state:
            session_state.cart_check_in = None
        if 'cart_check_out' not in session_state:
            session_state.cart_check_out = None
        if 'cart_guests' not in session_state:
            session_state.cart_guests = {}
    
    @staticmethod
    def add_to_cart(session_state, room_data, check_in, check_out, num_guests, total_price, nights):
        """
        Add a room to cart.
        
        Args:
            session_state: Streamlit session state
            room_data: Dict with room information
            check_in: Check-in datetime
            check_out: Check-out datetime
            num_guests: Number of guests for this room
            total_price: Total price for this room
            nights: Number of nights
        
        Returns:
            (success: bool, message: str)
        """
        CartManager.init_cart(session_state)
        
        # Set dates if first item
        if len(session_state.cart) == 0:
            session_state.cart_check_in = check_in
            session_state.cart_check_out = check_out
        else:
            # Verify same dates
            if (session_state.cart_check_in != check_in or 
                session_state.cart_check_out != check_out):
                return False, "All rooms must have the same check-in and check-out dates"
        
        # Check if room already in cart
        for item in session_state.cart:
            if item['room_id'] == room_data['room_id']:
                return False, f"Room {room_data['room_number']} is already in your cart"
        
        # Add to cart
        cart_item = {
            'room_id': room_data['room_id'],
            'room_number': room_data['room_number'],
            'room_type': room_data['room_type'],
            'num_guests': num_guests,
            'base_price': room_data['base_price'],
            'total_price': total_price,
            'nights': nights,
            'description': room_data.get('description', ''),
            'capacity': room_data.get('capacity', 2)
        }
        
        session_state.cart.append(cart_item)
        session_state.cart_guests[room_data['room_id']] = num_guests
        
        return True, f"Room {room_data['room_number']} added to cart!"
    
    @staticmethod
    def remove_from_cart(session_state, room_id):
        """Remove a room from cart"""
        CartManager.init_cart(session_state)
        
        session_state.cart = [item for item in session_state.cart if item['room_id'] != room_id]
        
        if room_id in session_state.cart_guests:
            del session_state.cart_guests[room_id]
        
        # Clear dates if cart is empty
        if len(session_state.cart) == 0:
            session_state.cart_check_in = None
            session_state.cart_check_out = None
            session_state.cart_guests = {}
        
        return True, "Room removed from cart"
    
    @staticmethod
    def clear_cart(session_state):
        """Clear entire cart"""
        session_state.cart = []
        session_state.cart_check_in = None
        session_state.cart_check_out = None
        session_state.cart_guests = {}
        return True, "Cart cleared"
    
    @staticmethod
    def get_cart_total(session_state):
        """Calculate total price for all rooms in cart"""
        CartManager.init_cart(session_state)
        
        total = sum(item['total_price'] for item in session_state.cart)
        return total
    
    @staticmethod
    def get_cart_count(session_state):
        """Get number of rooms in cart"""
        CartManager.init_cart(session_state)
        return len(session_state.cart)
    
    @staticmethod
    def get_total_guests(session_state):
        """Get total number of guests across all rooms"""
        CartManager.init_cart(session_state)
        return sum(item['num_guests'] for item in session_state.cart)
