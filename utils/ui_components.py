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
        """Dark luxury theme with synchronized animations + JavaScript button fix"""
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
        
        /* ===== BUTTONS - GOLD GRADIENT ===== */
        .stButton > button,
        div[data-testid="stButton"] > button,
        button {
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            letter-spacing: 0.5px !important;
            transition: all 0.4s ease !important;
            border: none !important;
            text-transform: uppercase !important;
            font-size: 0.9rem !important;
        }
        
        .stButton > button[kind="primary"],
        div[data-testid="stButton"] > button[kind="primary"],
        button[kind="primary"],
        button[type="submit"],
        .stForm button,
        .stDownloadButton > button {
            background: linear-gradient(135deg, #C4935B 0%, #B8875A 100%) !important;
            color: #1A1F1E !important;
            box-shadow: 0 4px 15px rgba(196, 147, 91, 0.3) !important;
        }
        
        .stButton > button[kind="primary"]:hover,
        div[data-testid="stButton"] > button[kind="primary"]:hover,
        button[kind="primary"]:hover,
        button[type="submit"]:hover,
        .stForm button:hover,
        .stDownloadButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 25px rgba(196, 147, 91, 0.5) !important;
            background: linear-gradient(135deg, #D4A76A 0%, #C4935B 100%) !important;
        }
        
        .stButton > button[kind="secondary"],
        div[data-testid="stButton"] > button[kind="secondary"],
        button[kind="secondary"] {
            background: transparent !important;
            color: #C4935B !important;
            border: 2px solid #C4935B !important;
        }
        
        .stButton > button[kind="secondary"]:hover,
        div[data-testid="stButton"] > button[kind="secondary"]:hover,
        button[kind="secondary"]:hover {
            background: rgba(196, 147, 91, 0.1) !important;
            border-color: #D4A76A !important;
            color: #D4A76A !important;
            transform: translateY(-2px) !important;
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
        
        /* ===== INPUTS - DARK THEME ===== */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input,
        .stDateInput > div > div > input,
        input, textarea {
            border-radius: 10px !important;
            border: 2px solid #3D4A47 !important;
            background-color: #2A3533 !important;
            color: #F5F5F0 !important;
            padding: 0.75rem !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stDateInput > div > div > input:focus,
        input:focus, textarea:focus {
            border-color: #C4935B !important;
            box-shadow: 0 0 0 3px rgba(196, 147, 91, 0.2) !important;
            background-color: #2C3E3A !important;
        }
        
        /* Disabled inputs */
        input:disabled, textarea:disabled, select:disabled {
            background-color: #1F2524 !important;
            color: #9BA8A5 !important;
            opacity: 0.7 !important;
            cursor: not-allowed !important;
        }
        
        /* Labels */
        label {
            color: #C4935B !important;
            font-weight: 600 !important;
        }
        
        /* ===== SELECTBOX STYLING - DARK LUXURY ===== */
        /* Main selectbox container */
        .stSelectbox > div > div {
            background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%) !important;
            border: 2px solid #3D4A47 !important;
            border-radius: 10px !important;
            transition: all 0.3s ease !important;
        }
        
        .stSelectbox > div > div:hover {
            border-color: #C4935B !important;
            box-shadow: 0 0 0 3px rgba(196, 147, 91, 0.2) !important;
        }
        
        /* Selected value text */
        .stSelectbox [data-baseweb="select"] > div {
            background-color: transparent !important;
            color: #F5F5F0 !important;
            font-weight: 600 !important;
            padding: 0.75rem !important;
        }
        
        /* Dropdown arrow - position at the end */
        .stSelectbox [data-baseweb="select"] svg {
            fill: #C4935B !important;
            width: 20px !important;
            height: 20px !important;
        }
        
        /* Fix arrow container positioning */
        .stSelectbox [data-baseweb="select"] > div:last-child {
            display: flex !important;
            align-items: center !important;
            padding-right: 12px !important;
        }
        
        /* Dropdown menu background */
        .stSelectbox [data-baseweb="popover"] {
            background: linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%) !important;
            border: 2px solid #C4935B !important;
            border-radius: 10px !important;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5) !important;
            margin-top: 4px !important;
        }
        
        /* Dropdown list container */
        .stSelectbox [role="listbox"] {
            background: transparent !important;
            padding: 0.5rem !important;
        }
        
        /* Dropdown options */
        .stSelectbox [role="option"] {
            background: transparent !important;
            color: #F5F5F0 !important;
            padding: 0.75rem 1rem !important;
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
            margin-bottom: 0.25rem !important;
        }
        
        .stSelectbox [role="option"]:hover {
            background: rgba(196, 147, 91, 0.2) !important;
            color: #C4935B !important;
        }
        
        /* Selected option in dropdown */
        .stSelectbox [aria-selected="true"] {
            background: linear-gradient(135deg, #C4935B 0%, #B8875A 100%) !important;
            color: #1A1F1E !important;
            font-weight: 700 !important;
        }
        
        /* Focus state */
        .stSelectbox [data-baseweb="select"]:focus-within {
            border-color: #C4935B !important;
            box-shadow: 0 0 0 3px rgba(196, 147, 91, 0.3) !important;
        }
        
        /* Remove default Streamlit selectbox styles */
        .stSelectbox > div > div > div {
            background-color: transparent !important;
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
        
        <script>
        // ============================================================================
        // SOLIVIE HOTEL - FORCE GOLD BUTTON STYLING (JAVASCRIPT OVERRIDE)
        // This ensures buttons remain gold even when Streamlit applies inline styles
        // ============================================================================
        
        (function() {
            'use strict';
            
            console.log('🎨 Solivie Hotel - Initializing gold button styling...');
            
            function applyGoldStyling() {
                // ===== TARGET ALL BUTTONS =====
                const allButtons = document.querySelectorAll('button');
                let primaryCount = 0;
                let secondaryCount = 0;
                
                allButtons.forEach(button => {
                    const text = (button.innerText || button.textContent || '').trim().toUpperCase();
                    const kind = button.getAttribute('kind');
                    const type = button.getAttribute('type');
                    
                    // Identify primary buttons
                    const isPrimary = 
                        kind === 'primary' ||
                        type === 'submit' ||
                        text.includes('SAVE') ||
                        text.includes('SUBMIT') ||
                        text.includes('LOGIN') ||
                        text.includes('REGISTER') ||
                        text.includes('BOOK') ||
                        text.includes('PAY') ||
                        text.includes('CONFIRM') ||
                        text.includes('DOWNLOAD') ||
                        text.includes('SEARCH') ||
                        text.includes('GENERATE') ||
                        text.includes('ADD') ||
                        text.includes('UPDATE') ||
                        text.includes('CREATE') ||
                        text.includes('CHECK');
                    
                    // Identify secondary buttons
                    const isSecondary = 
                        kind === 'secondary' ||
                        text.includes('CANCEL') ||
                        text.includes('BACK') ||
                        text.includes('VIEW') ||
                        text.includes('INVOICE') ||
                        text.includes('CALENDAR') ||
                        text.includes('CART') ||
                        text.includes('HOME') ||
                        text.includes('LOGOUT') ||
                        text.includes('REFRESH') ||
                        text.includes('DELETE');
                    
                    if (isPrimary) {
                        // Apply gold gradient
                        button.style.setProperty('background', 'linear-gradient(135deg, #C4935B 0%, #B8875A 100%)', 'important');
                        button.style.setProperty('background-color', '#C4935B', 'important');
                        button.style.setProperty('color', '#1A1F1E', 'important');
                        button.style.setProperty('border', 'none', 'important');
                        button.style.setProperty('border-radius', '10px', 'important');
                        button.style.setProperty('font-weight', '700', 'important');
                        button.style.setProperty('text-transform', 'uppercase', 'important');
                        button.style.setProperty('box-shadow', '0 4px 15px rgba(196, 147, 91, 0.3)', 'important');
                        primaryCount++;
                        
                    } else if (isSecondary) {
                        // Apply transparent with gold border
                        button.style.setProperty('background', 'transparent', 'important');
                        button.style.setProperty('color', '#C4935B', 'important');
                        button.style.setProperty('border', '2px solid #C4935B', 'important');
                        button.style.setProperty('border-radius', '10px', 'important');
                        button.style.setProperty('font-weight', '600', 'important');
                        button.style.setProperty('text-transform', 'uppercase', 'important');
                        secondaryCount++;
                    }
                });
                
                if (primaryCount > 0 || secondaryCount > 0) {
                    console.log(`✅ Styled ${primaryCount} primary and ${secondaryCount} secondary buttons`);
                }
                
                // ===== STYLE INPUT FIELDS =====
                const inputs = document.querySelectorAll('input, textarea');
                inputs.forEach(input => {
                    if (input.disabled) {
                        input.style.setProperty('background-color', '#1F2524', 'important');
                        input.style.setProperty('color', '#9BA8A5', 'important');
                    } else {
                        input.style.setProperty('background-color', '#2A3533', 'important');
                        input.style.setProperty('color', '#F5F5F0', 'important');
                        input.style.setProperty('border', '2px solid #3D4A47', 'important');
                        input.style.setProperty('border-radius', '10px', 'important');
                    }
                });
                
                // ===== STYLE SELECTBOXES =====
                const selectBoxes = document.querySelectorAll('[data-baseweb="select"]');
                selectBoxes.forEach(select => {
                    const container = select.closest('.stSelectbox > div > div');
                    if (container) {
                        container.style.setProperty('background', 'linear-gradient(145deg, #2A3533 0%, #2C3E3A 100%)', 'important');
                        container.style.setProperty('border', '2px solid #3D4A47', 'important');
                        container.style.setProperty('border-radius', '10px', 'important');
                    }
                });
            }
            
            // Run immediately
            applyGoldStyling();
            
            // Run after delays to catch dynamic content
            setTimeout(applyGoldStyling, 300);
            setTimeout(applyGoldStyling, 800);
            setTimeout(applyGoldStyling, 1500);
            setTimeout(applyGoldStyling, 3000);
            
            // Watch for DOM changes
            const observer = new MutationObserver(function(mutations) {
                let hasNewElements = false;
                mutations.forEach(mutation => {
                    mutation.addedNodes.forEach(node => {
                        if (node.nodeType === 1) {
                            if (node.tagName === 'BUTTON' || node.querySelector('button') || 
                                node.querySelector('[data-baseweb="select"]')) {
                                hasNewElements = true;
                            }
                        }
                    });
                });
                if (hasNewElements) {
                    setTimeout(applyGoldStyling, 100);
                }
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
            
            // Re-apply on tab clicks and interactions
            document.addEventListener('click', function(e) {
                if (e.target.closest('[role="tab"]') || e.target.closest('.stSelectbox')) {
                    setTimeout(applyGoldStyling, 200);
                    setTimeout(applyGoldStyling, 600);
                }
            });
            
            console.log('✅ Solivie gold styling system active!');
        })();
        </script>
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
