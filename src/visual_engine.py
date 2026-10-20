import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from src.config import VIDEO_WIDTH, VIDEO_HEIGHT

# Dynamic color themes for visual variety (Anti-repetition)
COLOR_THEMES = [
    {
        "name": "CYBER_CYAN",
        "bg_top": (8, 12, 24),
        "bg_bot": (18, 30, 56),
        "card_fill": (14, 22, 42),
        "card_outline": (0, 240, 255),
        "accent": (0, 240, 255),
        "badge_hook": (255, 30, 86)
    },
    {
        "name": "NEON_PURPLE",
        "bg_top": (14, 8, 26),
        "bg_bot": (36, 16, 62),
        "card_fill": (24, 14, 42),
        "card_outline": (195, 75, 255),
        "accent": (215, 115, 255),
        "badge_hook": (255, 45, 130)
    },
    {
        "name": "MATRIX_EMERALD",
        "bg_top": (6, 18, 14),
        "bg_bot": (12, 40, 30),
        "card_fill": (14, 32, 24),
        "card_outline": (0, 235, 140),
        "accent": (0, 255, 175),
        "badge_hook": (255, 60, 60)
    },
    {
        "name": "SUNSET_GOLD",
        "bg_top": (18, 12, 8),
        "bg_bot": (46, 26, 16),
        "card_fill": (32, 20, 14),
        "card_outline": (255, 175, 35),
        "accent": (255, 210, 50),
        "badge_hook": (255, 40, 85)
    }
]

def get_font(size: int, bold: bool = False):
    """Load system font across Windows and Linux (GitHub Actions) with fallback"""
    font_candidates = [
        # Windows
        "arialbd.ttf" if bold else "arial.ttf",
        "segoeuib.ttf" if bold else "segoeui.ttf",
        # Linux (Ubuntu GitHub Actions)
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans.ttf",
        # Generic
        "DejaVuSans.ttf"
    ]
    for candidate in font_candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except Exception:
            continue
    try:
        return ImageFont.load_default()
    except Exception:
        return None

def create_gradient_background(width: int, height: int, top_color=(10, 14, 26), bottom_color=(22, 30, 54)):
    """Draw a smooth vertical cyber-dark gradient"""
    base = Image.new('RGB', (width, height), top_color)
    top_r, top_g, top_b = top_color
    bot_r, bot_g, bot_b = bottom_color
    
    draw = ImageDraw.Draw(base)
    for y in range(height):
        ratio = y / float(height)
        r = int(top_r + (bot_r - top_r) * ratio)
        g = int(top_g + (bot_g - top_g) * ratio)
        b = int(top_b + (bot_b - top_b) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return base

def draw_rounded_card(draw: ImageDraw.Draw, xy, fill=(18, 24, 42), outline=(0, 240, 255), radius=28, border_width=4):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=border_width)

def draw_pill_badge(draw: ImageDraw.Draw, xy, text: str, font, fill=(255, 45, 85), text_color=(255, 255, 255)):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=fill)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = x0 + ((x1 - x0) - tw) / 2
    ty = y0 + ((y1 - y0) - th) / 2 - 2
    draw.text((tx, ty), text, fill=text_color, font=font)

def wrap_text(text: str, font, max_width: int, draw: ImageDraw.Draw):
    words = text.split()
    lines = []
    current_line = []
    for w in words:
        test_line = " ".join(current_line + [w])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if (bbox[2] - bbox[0]) <= max_width:
            current_line.append(w)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [w]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def generate_scene_images(content: dict, temp_dir: Path) -> list[Path]:
    temp_dir.mkdir(parents=True, exist_ok=True)
    images = []
    
    # Pick a random dynamic color theme for this run
    theme = random.choice(COLOR_THEMES)
    print(f"🎨 Visual Theme Applied: {theme['name']}")
    
    font_badge = get_font(34, bold=True)
    font_title_large = get_font(72, bold=True)
    font_heading = get_font(56, bold=True)
    font_body = get_font(42, bold=False)
    font_body_bold = get_font(44, bold=True)
    
    tool_name = content.get("tool_name", "AI Tool").upper()
    category = content.get("category", "AI SOFTWARE").upper()
    rating = content.get("rating", "9.8/10")
    tagline = content.get("tagline", "Next-Gen AI Platform")
    features = content.get("features", ["Feature 1", "Feature 2", "Feature 3"])
    
    # -------------------------------------------------------------
    # SCENE 1: HOOK (Attention Grabber)
    # -------------------------------------------------------------
    img1 = create_gradient_background(VIDEO_WIDTH, VIDEO_HEIGHT, theme["bg_top"], theme["bg_bot"])
    draw1 = ImageDraw.Draw(img1)
    
    draw_pill_badge(draw1, (240, 260, 840, 340), "[ SECRET AI HACK ]", font_badge, fill=theme["badge_hook"])
    draw_rounded_card(draw1, (80, 420, 1000, 1100), fill=theme["card_fill"], outline=theme["accent"], radius=35, border_width=5)
    
    hook_lines = wrap_text(content.get("hook", "Stop wasting your time doing things manually!"), font_heading, 800, draw1)
    y_text = 490
    for line in hook_lines:
        bbox = draw1.textbbox((0, 0), line, font=font_heading)
        lw = bbox[2] - bbox[0]
        draw1.text(((VIDEO_WIDTH - lw) / 2, y_text), line, fill=(255, 255, 255), font=font_heading)
        y_text += 75
        
    draw_pill_badge(draw1, (290, 940, 790, 1030), "DON'T MISS THIS >>", font_badge, fill=(255, 184, 0), text_color=(0, 0, 0))
    
    path1 = temp_dir / "scene_01_hook.png"
    img1.save(path1)
    images.append(path1)
    
    # -------------------------------------------------------------
    # SCENE 2: TOOL REVEAL
    # -------------------------------------------------------------
    img2 = create_gradient_background(VIDEO_WIDTH, VIDEO_HEIGHT, theme["bg_top"], theme["bg_bot"])
    draw2 = ImageDraw.Draw(img2)
    
    draw_pill_badge(draw2, (260, 260, 820, 340), f"[ {category} ]", font_badge, fill=theme["accent"], text_color=(0, 0, 0))
    draw_rounded_card(draw2, (80, 400, 1000, 1120), fill=theme["card_fill"], outline=theme["card_outline"], radius=35, border_width=5)
    
    rating_text = f"OVERALL RATING: {rating}"
    bbox_r = draw2.textbbox((0, 0), rating_text, font=font_body_bold)
    draw2.text(((VIDEO_WIDTH - (bbox_r[2] - bbox_r[0])) / 2, 460), rating_text, fill=(255, 215, 0), font=font_body_bold)
    
    bbox_t = draw2.textbbox((0, 0), tool_name, font=font_title_large)
    draw2.text(((VIDEO_WIDTH - (bbox_t[2] - bbox_t[0])) / 2, 570), tool_name, fill=theme["accent"], font=font_title_large)
    
    tag_lines = wrap_text(tagline, font_heading, 800, draw2)
    y_tag = 720
    for line in tag_lines:
        bbox_l = draw2.textbbox((0, 0), line, font=font_heading)
        draw2.text(((VIDEO_WIDTH - (bbox_l[2] - bbox_l[0])) / 2, y_tag), line, fill=(240, 240, 240), font=font_heading)
        y_tag += 70
        
    draw_pill_badge(draw2, (300, 960, 780, 1050), "100% FREE TO START", font_badge, fill=(0, 230, 118), text_color=(0, 0, 0))
    
    path2 = temp_dir / "scene_02_tool.png"
    img2.save(path2)
    images.append(path2)
    
    # -------------------------------------------------------------
    # SCENE 3: 3 KILLER FEATURES
    # -------------------------------------------------------------
    img3 = create_gradient_background(VIDEO_WIDTH, VIDEO_HEIGHT, theme["bg_top"], theme["bg_bot"])
    draw3 = ImageDraw.Draw(img3)
    
    draw_pill_badge(draw3, (280, 220, 800, 300), "WHY IT'S A GAME-CHANGER", font_badge, fill=theme["accent"], text_color=(0, 0, 0))
    
    y_feat = 370
    card_colors = [
        (theme["card_fill"], theme["card_outline"]),
        (theme["card_fill"], (255, 200, 0)),
        (theme["card_fill"], (0, 230, 118))
    ]
    badge_prefixes = ["01", "02", "03"]
    
    for i, feat in enumerate(features[:3]):
        fill_c, out_c = card_colors[i % len(card_colors)]
        draw_rounded_card(draw3, (80, y_feat, 1000, y_feat + 230), fill=fill_c, outline=out_c, radius=28, border_width=4)
        
        draw_pill_badge(draw3, (120, y_feat + 30, 240, y_feat + 90), badge_prefixes[i], font_body_bold, fill=out_c, text_color=(0, 0, 0))
        
        flines = wrap_text(feat, font_body_bold, 780, draw3)
        fy = y_feat + 105
        for fline in flines[:2]:
            draw3.text((120, fy), fline, fill=(255, 255, 255), font=font_body_bold)
            fy += 55
            
        y_feat += 270
        
    path3 = temp_dir / "scene_03_features.png"
    img3.save(path3)
    images.append(path3)
    
    # -------------------------------------------------------------
    # SCENE 4: CTA (Link In Bio)
    # -------------------------------------------------------------
    img4 = create_gradient_background(VIDEO_WIDTH, VIDEO_HEIGHT, theme["bg_top"], theme["bg_bot"])
    draw4 = ImageDraw.Draw(img4)
    
    draw_pill_badge(draw4, (260, 320, 820, 400), "WANT TO TRY THIS?", font_badge, fill=(255, 184, 0), text_color=(0, 0, 0))
    
    draw_rounded_card(draw4, (80, 470, 1000, 1180), fill=theme["card_fill"], outline=theme["accent"], radius=40, border_width=6)
    
    bbox_cta1 = draw4.textbbox((0, 0), ">> LINK IN BIO <<", font_title_large)
    draw4.text(((VIDEO_WIDTH - (bbox_cta1[2] - bbox_cta1[0])) / 2, 570), ">> LINK IN BIO <<", fill=theme["accent"], font=font_title_large)
    
    cta_sub = "Click the link in our profile to test this AI completely free!"
    clines = wrap_text(cta_sub, font_heading, 800, draw4)
    cy = 730
    for line in clines:
        bbox_c = draw4.textbbox((0, 0), line, font=font_heading)
        draw4.text(((VIDEO_WIDTH - (bbox_c[2] - bbox_c[0])) / 2, cy), line, fill=(240, 240, 240), font=font_heading)
        cy += 70
        
    draw_pill_badge(draw4, (200, 990, 880, 1080), "FOLLOW FOR DAILY AI HACKS", font_badge, fill=(255, 30, 86), text_color=(255, 255, 255))
    
    path4 = temp_dir / "scene_04_cta.png"
    img4.save(path4)
    images.append(path4)
    
    return images
