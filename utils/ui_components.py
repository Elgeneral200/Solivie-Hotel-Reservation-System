"""
Solivie Hotel - Dark Luxury UI Components
Premium dark theme with synchronized animations
"""
import streamlit as st


class SolivieUI:
    """Dark luxury UI components for Solivie Hotel"""
    
    # ===== DARK LUXURY COLOR PALETTE =====
    PRIMARY_DARK = "#2C3E3A"  # Deep forest green
    SECONDARY_DARK = "#5A726F"  # Sage green (from logo)
    ACCENT_GOLD = "#C4935B"  # Bronze/gold (from logo)
    RICH_GOLD = "#B8875A"  # Warm gold
    
    # Dark backgrounds
    BG_DARK = "#1A1F1E"  # Almost black with green tint
    BG_CARD = "#2A3533"  # Dark card background
    BG_HOVER = "#3D4A47"  # Hover state
    
    # Text colors
    TEXT_LIGHT = "#F5F5F0"  # Cream (from logo)
    TEXT_GOLD = "#C4935B"  # Gold text
    TEXT_MUTED = "#9BA8A5"  # Muted light
    
    # Borders
    BORDER_DARK = "#3D4A47"
    BORDER_GOLD = "#C4935B"
    
    @staticmethod
    def inject_custom_css():
        """Dark luxury theme with synchronized animations"""
        st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;600;700&display=swap');
        
        /* Global Dark Theme */
        .stApp {
            background: linear-gradient(180deg, #1A1F1E 0%, #2C3E3A 100%);
            font-family: 'Inter', sans-serif;
        }
        
        /* Headers */
        h1, h2, h3 {
            font-family: 'Playfair Display', serif;
            color: #F5F5F0 !important;
        }
        
        h1 {
            font-weight: 700;
            letter-spacing: 1px;
        }
        
        /* Main content background */
        .main .block-container {
            background: transparent;
        }
        
        /* Buttons - Gold Gradient */
        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
            letter-spacing: 0.5px;
            transition: all 0.4s ease;
            border: none;
            text-transform: uppercase;
            font-size: 0.9rem;
        }
        
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #C4935B 0%, #B8875A 100%);
            color: #1A1F1E;
            box-shadow: 0 4px 15px rgba(196, 147, 91, 0.3);
        }
        
        .stButton > button[kind="primary"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(196, 147, 91, 0.5);
            background: linear-gradient(135deg, #D4A76A 0%, #C4935B 100%);
        }
        
        .stButton > button[kind="secondary"] {
            background: transparent;
            color: #C4935B;
            border: 2px solid #C4935B;
        }
        
        .stButton > button[kind="secondary"]:hover {
            background: rgba(196, 147, 91, 0.1);
            border-color: #D4A76A;
            color: #D4A76A;
            transform: translateY(-2px);
        }
        
        /* Cards - Dark with glow */
        .solivie-card {
            background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
            margin-bottom: 1.5rem;
            transition: all 0.4s ease;
            border: 1px solid #3D4A47;
        }
        
        .solivie-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(196, 147, 91, 0.2);
            border-color: #C4935B;
        }
        
        /* ===== SYNCHRONIZED ANIMATED STATS ===== */
        .stats-container {
            animation: fadeInUp 0.8s ease-out;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .stat-card {
            background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
            text-align: center;
            border: 2px solid #3D4A47;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(196, 147, 91, 0.1), transparent);
            transition: left 0.5s;
        }
        
        /* Synchronized hover - all scale together */
        .stats-container:hover .stat-card {
            transform: translateY(-10px) scale(1.05);
            box-shadow: 0 15px 50px rgba(196, 147, 91, 0.3);
            border-color: #C4935B;
        }
        
        .stat-card:hover::before {
            left: 100%;
        }
        
        .stat-number {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, #C4935B 0%, #D4A76A 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: numberPulse 2s ease-in-out infinite;
        }
        
        @keyframes numberPulse {
            0%, 100% { 
                transform: scale(1);
                filter: brightness(1);
            }
            50% { 
                transform: scale(1.1);
                filter: brightness(1.2);
            }
        }
        
        .stat-label {
            color: #9BA8A5;
            font-size: 1.1rem;
            font-weight: 600;
            margin-top: 0.5rem;
        }
        
        .stat-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            animation: iconFloat 3s ease-in-out infinite;
        }
        
        @keyframes iconFloat {
            0%, 100% { 
                transform: translateY(0px) rotate(0deg); 
            }
            50% { 
                transform: translateY(-10px) rotate(5deg); 
            }
        }
        
        /* ===== ANIMATED ROOM CARDS ===== */
        .room-card {
            background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.4);
            text-align: center;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            border: 2px solid #3D4A47;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .room-card::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, #C4935B, #D4A76A);
            transform: scaleX(0);
            transition: transform 0.4s ease;
        }
        
        .room-card:hover {
            transform: translateY(-15px) scale(1.05);
            box-shadow: 0 20px 50px rgba(196, 147, 91, 0.4);
            border-color: #C4935B;
        }
        
        .room-card:hover::after {
            transform: scaleX(1);
        }
        
        .room-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
            filter: drop-shadow(0 4px 8px rgba(196, 147, 91, 0.3));
            transition: all 0.4s ease;
        }
        
        .room-card:hover .room-icon {
            transform: scale(1.2) rotate(5deg);
        }
        
        .room-price {
            color: #C4935B;
            font-size: 2rem;
            font-weight: 700;
            margin: 1rem 0;
            transition: all 0.3s ease;
        }
        
        .room-card:hover .room-price {
            color: #D4A76A;
            transform: scale(1.1);
        }
        
        /* Feature Cards */
        .feature-card {
            background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            border: 2px solid #3D4A47;
            transition: all 0.4s ease;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        
        .feature-card:hover {
            transform: translateY(-8px);
            border-color: #C4935B;
            box-shadow: 0 12px 35px rgba(196, 147, 91, 0.25);
        }
        
        .feature-icon {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            filter: drop-shadow(0 4px 8px rgba(196, 147, 91, 0.3));
        }
        
        /* Inputs - Dark theme */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        .stNumberInput > div > div > input,
        .stDateInput > div > div > input {
            border-radius: 10px;
            border: 2px solid #3D4A47;
            background-color: #2A3533;
            color: #F5F5F0;
            padding: 0.75rem;
        }
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus,
        .stDateInput > div > div > input:focus {
            border-color: #C4935B;
            box-shadow: 0 0 0 3px rgba(196, 147, 91, 0.2);
        }
        
        /* Sidebar - Luxury dark */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #2C3E3A 0%, #1A1F1E 100%);
            border-right: 1px solid #C4935B;
        }
        
        [data-testid="stSidebar"] * {
            color: #F5F5F0 !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: #2A3533;
            padding: 0.75rem;
            border-radius: 12px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            color: #9BA8A5;
            background: transparent;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #C4935B 0%, #B8875A 100%);
            color: #1A1F1E !important;
        }
        
        /* Expanders */
        .streamlit-expanderHeader {
            background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
            border-radius: 10px;
            font-weight: 600;
            color: #F5F5F0;
            border: 2px solid #3D4A47;
        }
        
        .streamlit-expanderHeader:hover {
            border-color: #C4935B;
        }
        
        /* Messages */
        .stSuccess {
            background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
            border-left: 4px solid #6B8E7E;
            color: #F5F5F0;
            border-radius: 10px;
        }
        
        .stError {
            background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
            border-left: 4px solid #A95F5F;
            color: #F5F5F0;
            border-radius: 10px;
        }
        
        .stWarning {
            background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
            border-left: 4px solid #D4A76A;
            color: #F5F5F0;
            border-radius: 10px;
        }
        
        .stInfo {
            background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
            border-left: 4px solid #7B9CA8;
            color: #F5F5F0;
            border-radius: 10px;
        }
        
        /* Metrics */
        .stMetric {
            background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 2px solid #3D4A47;
        }
        
        .stMetric label {
            color: #9BA8A5 !important;
        }
        
        .stMetric [data-testid="stMetricValue"] {
            color: #C4935B !important;
        }
        
        /* Divider */
        hr {
            border-color: #3D4A47;
            margin: 2rem 0;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #2A3533;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #C4935B;
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #D4A76A;
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def page_header(title, subtitle="", icon="🏨"):
        """Dark luxury header with glow animation"""
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #2C3E3A 0%, #5A726F 50%, #2C3E3A 100%);
                    padding: 3rem 2rem; 
                    border-radius: 20px; 
                    margin-bottom: 2rem;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.5);
                    border: 2px solid #C4935B;
                    position: relative;
                    overflow: hidden;'>
            <div style='position: absolute; top: -50%; right: -10%; width: 40%; height: 200%;
                        background: radial-gradient(circle, rgba(196,147,91,0.1) 0%, transparent 70%);
                        animation: glow 3s ease-in-out infinite;'></div>
            <h1 style='color: #F5F5F0; margin: 0; font-size: 3rem; position: relative; z-index: 1;'>
                {icon} {title}
            </h1>
            {f"<p style='color: #C4935B; margin: 1rem 0 0 0; font-size: 1.3rem; font-weight: 500; position: relative; z-index: 1;'>{subtitle}</p>" if subtitle else ""}
        </div>
        <style>
        @keyframes glow {{
            0%, 100% {{ opacity: 0.5; }}
            50% {{ opacity: 1; }}
        }}
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def hero_section(title, description):
        """Dark luxury hero with pattern background"""
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #1A1F1E 0%, #2C3E3A 50%, #5A726F 100%);
                    padding: 5rem 2rem; 
                    border-radius: 25px; 
                    margin-bottom: 3rem;
                    text-align: center;
                    box-shadow: 0 15px 60px rgba(0,0,0,0.6);
                    border: 3px solid #C4935B;
                    position: relative;
                    overflow: hidden;'>
            <div style='position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                        background: url("data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cpath d=\'M0 0h60v60H0z\' fill=\'none\'/%3E%3Cpath d=\'M30 0l30 30-30 30L0 30z\' fill=\'%23C4935B\' fill-opacity=\'0.03\'/%3E%3C/svg%3E");
                        opacity: 0.5;'></div>
            <h1 style='color: #F5F5F0; font-size: 4rem; margin: 0 0 1.5rem 0; font-weight: 700;
                       text-shadow: 0 4px 20px rgba(0,0,0,0.5); position: relative; z-index: 1;
                       font-family: "Playfair Display", serif;'>
                {title}
            </h1>
            <p style='color: #C4935B; font-size: 1.5rem; margin: 0; font-weight: 600;
                      text-shadow: 0 2px 10px rgba(0,0,0,0.5); position: relative; z-index: 1;'>
                {description}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def feature_card(icon, title, description):
        """Dark feature card"""
        st.markdown(f"""
        <div class='feature-card'>
            <div class='feature-icon'>{icon}</div>
            <h3 style='color: #C4935B; margin: 1rem 0 0.5rem 0; font-size: 1.3rem;'>{title}</h3>
            <p style='color: #9BA8A5; margin: 0; line-height: 1.6;'>{description}</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def stat_card(number, label, icon="📊"):
        """Animated stat card with pulsing number"""
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-icon'>{icon}</div>
            <div class='stat-number'>{number}</div>
            <div class='stat-label'>{label}</div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def footer():
        """Dark luxury footer"""
        st.markdown("---")
        st.markdown("""
        <div style='background: linear-gradient(135deg, #1A1F1E 0%, #2C3E3A 100%); 
                    color: #F5F5F0; 
                    padding: 3rem 2rem; 
                    border-radius: 15px; 
                    margin-top: 3rem;
                    border: 2px solid #C4935B;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.5);'>
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2.5rem;'>
                <div>
                    <h3 style='color: #C4935B; margin-top: 0; font-size: 1.5rem; font-family: "Playfair Display", serif;'>
                        🏨 Solivie Hotel
                    </h3>
                    <p style='margin: 0.5rem 0; color: #9BA8A5; line-height: 1.6;'>
                        Experience luxury and comfort in every stay
                    </p>
                </div>
                <div>
                    <h4 style='color: #C4935B; font-size: 1.2rem;'>Contact</h4>
                    <p style='margin: 0.5rem 0; color: #F5F5F0;'>📧 info@solivie.com</p>
                    <p style='margin: 0.5rem 0; color: #F5F5F0;'>📞 +1 (555) 123-4567</p>
                    <p style='margin: 0.5rem 0; color: #F5F5F0;'>📍 123 Luxury Ave, City</p>
                </div>
                <div>
                    <h4 style='color: #C4935B; font-size: 1.2rem;'>Quick Links</h4>
                    <p style='margin: 0.5rem 0; color: #F5F5F0;'>• About Us</p>
                    <p style='margin: 0.5rem 0; color: #F5F5F0;'>• Privacy Policy</p>
                    <p style='margin: 0.5rem 0; color: #F5F5F0;'>• Terms & Conditions</p>
                </div>
            </div>
            <hr style='border-color: #3D4A47; margin: 2rem 0;'>
            <p style='text-align: center; margin: 0; color: #9BA8A5;'>
                © 2025 Solivie Hotel. All rights reserved. | Crafted with excellence
            </p>
        </div>
        """, unsafe_allow_html=True)
