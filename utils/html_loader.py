# utils/html_loader.py
"""
HTML/CSS loader utilities for modular component rendering
"""

import os
import base64


def get_base64_image(image_path):
    """Convert image to base64 string for embedding in HTML."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        print(f"⚠️ Error encoding image: {e}")
        return None


def render_hero_card(logo_path=None):
    """
    Render the hero card with inline CSS and HTML.
    
    Args:
        logo_path: Path to logo image file
        
    Returns:
        Complete HTML/CSS string ready for st.markdown()
    """
    
    # Prepare logo content
    if logo_path and os.path.exists(logo_path):
        logo_base64 = get_base64_image(logo_path)
        if logo_base64:
            # Determine image type
            ext = os.path.splitext(logo_path)[1].lower()
            mime_type = "image/jpeg" if ext in ['.jpg', '.jpeg'] else "image/png"
            logo_html = f'<img src="data:{mime_type};base64,{logo_base64}" class="hero-logo" alt="Solivie Hotel Logo">'
        else:
            logo_html = '<div class="hero-logo-placeholder">🏨</div>'
    else:
        logo_html = '<div class="hero-logo-placeholder">🏨</div>'
    
    # Complete HTML with inline CSS
    html_content = f"""
    <style>
        .hero-container {{
            margin: 1.5rem 0 3rem 0;
        }}

        .hero-card {{
            background: linear-gradient(135deg, #1A1F1E 0%, #2C3E3A 50%, #5A726F 100%);
            padding: 3rem;
            border-radius: 25px;
            box-shadow: 0 15px 60px rgba(0, 0, 0, 0.6);
            border: 3px solid #C4935B;
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            gap: 3rem;
            min-height: 200px;
        }}

        .hero-background-pattern {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 0h60v60H0z' fill='none'/%3E%3Cpath d='M30 0l30 30-30 30L0 30z' fill='%23C4935B' fill-opacity='0.03'/%3E%3C/svg%3E");
            opacity: 0.5;
            pointer-events: none;
        }}

        .hero-logo-section {{
            position: relative;
            z-index: 1;
            flex-shrink: 0;
        }}

        .hero-logo {{
            width: 180px;
            height: auto;
            border-radius: 15px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
            display: block;
        }}

        .hero-logo-placeholder {{
            width: 180px;
            height: 180px;
            background: #2C3E3A;
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid #C4935B;
            font-size: 3rem;
        }}

        .hero-text-section {{
            position: relative;
            z-index: 1;
            flex-grow: 1;
        }}

        .hero-title {{
            color: #F5F5F0;
            font-size: 2.8rem;
            margin: 0 0 1rem 0;
            font-weight: 700;
            font-family: "Playfair Display", serif;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
            line-height: 1.2;
        }}

        .hero-subtitle {{
            color: #C4935B;
            font-size: 1.15rem;
            margin: 0;
            font-weight: 600;
            font-style: italic;
            letter-spacing: 2px;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
        }}

        @media (max-width: 768px) {{
            .hero-card {{
                flex-direction: column;
                gap: 2rem;
                padding: 2rem;
                text-align: center;
            }}
            
            .hero-title {{
                font-size: 2rem;
            }}
            
            .hero-subtitle {{
                font-size: 1rem;
                letter-spacing: 1px;
            }}
            
            .hero-logo {{
                width: 150px;
            }}
            
            .hero-logo-placeholder {{
                width: 150px;
                height: 150px;
                font-size: 2.5rem;
            }}
        }}
    </style>
    
    <div class="hero-container">
        <div class="hero-card">
            <div class="hero-background-pattern"></div>
            
            <div class="hero-logo-section">
                {logo_html}
            </div>
            
            <div class="hero-text-section">
                <h1 class="hero-title">Welcome to Solivie Hotel</h1>
                <p class="hero-subtitle">✨ WHERE LUXURY MEETS COMFORT ✨</p>
            </div>
        </div>
    </div>
    """
    
    return html_content
