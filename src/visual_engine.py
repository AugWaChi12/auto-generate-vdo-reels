from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from src.config import VIDEO_WIDTH, VIDEO_HEIGHT

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
    
    # Simple line-by-line interpolation
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
    
    # Fonts
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
    img1 = create_gradient_background(VIDEO_WIDTH, VIDEO_HEIGHT, (8, 10, 20), (25, 15, 35))
    draw1 = ImageDraw.Draw(img1)
    
    # Top Warning Badge
    draw_pill_badge(draw1, (240, 260, 840, 340), "⚠️ SECRET AI HACK ⚠️", font_badge, fill=(255, 30, 86))
    
    # Hook Card
    draw_rounded_card(draw1, (80, 420, 1000, 1100), fill=(16, 20, 36), outline=(255, 75, 110), radius=35, border_width=5)
    
    hook_lines = wrap_text(content.get("hook", "Stop wasting your time doing things manually!"), font_heading, 800, draw1)
    y_text = 490
    for line in hook_lines:
        bbox = draw1.textbbox((0, 0), line, font=font_heading)
        lw = bbox[2] - bbox[0]
        draw1.text(((VIDEO_WIDTH - lw) / 2, y_text), line, fill=(255, 255, 255), font=font_heading)
        y_text += 75
        
    # Bottom tease inside card
    draw_pill_badge(draw1, (290, 940, 790, 1030), "DON'T MISS THIS ➔", font_badge, fill=(255, 184, 0), text_color=(0, 0, 0))
    
    path1 = temp_dir / "scene_01_hook.png"
    img1.save(path1)
    images.append(path1)
    
    # -------------------------------------------------------------
    # SCENE 2: TOOL REVEAL
    # -------------------------------------------------------------
    img2 = create_gradient_background(VIDEO_WIDTH, VIDEO_HEIGHT, (6, 15, 30), (14, 28, 55))
    draw2 = ImageDraw.Draw(img2)
    
    draw_pill_badge(draw2, (260, 260, 820, 340), f"⚡ {category} ⚡", font_badge, fill=(0, 190, 255))
    
    draw_rounded_card(draw2, (80, 400, 1000, 1120), fill=(14, 22, 42), outline=(0, 240, 255), radius=35, border_width=5)
    
    # Rating
    rating_text = f"⭐⭐⭐⭐⭐  {rating}"
    bbox_r = draw2.textbbox((0, 0), rating_text, font=font_body_bold)
    draw2.text(((VIDEO_WIDTH - (bbox_r[2] - bbox_r[0])) / 2, 460), rating_text, fill=(255, 215, 0), font=font_body_bold)
    
    # Giant Tool Name
    bbox_t = draw2.textbbox((0, 0), tool_name, font=font_title_large)
    draw2.text(((VIDEO_WIDTH - (bbox_t[2] - bbox_t[0])) / 2, 570), tool_name, fill=(0, 240, 255), font=font_title_large)
    
    # Tagline
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
    # SCENE 3: THE 3 FEATURES
    # -------------------------------------------------------------
    img3 = create_gradient_background(VIDEO_WIDTH, VIDEO_HEIGHT, (8, 12, 28), (20, 24, 48))
    draw3 = ImageDraw.Draw(img3)
    
    draw_pill_badge(draw3, (280, 240, 800, 320), "🔥 WHY IT'S INSANE 🔥", font_badge, fill=(138, 43, 226))
    
    # Render 3 Feature Cards
    y_cards = [380, 620, 860]
    for i, (f_text, y_pos) in enumerate(zip(features[:3], y_cards)):
        draw_rounded_card(draw3, (90, y_pos, 990, y_pos + 200), fill=(16, 22, 40), outline=(0, 230, 118), radius=25, border_width=3)
        draw_pill_badge(draw3, (120, y_pos + 30, 240, y_pos + 90), f"#{i+1}", font_badge, fill=(0, 230, 118), text_color=(0, 0, 0))
        
        f_lines = wrap_text(f_text, font_body_bold, 680, draw3)
        y_fl = y_pos + 35
        for fl in f_lines:
            draw3.text((270, y_fl), fl, fill=(255, 255, 255), font=font_body_bold)
            y_fl += 55
            
    path3 = temp_dir / "scene_03_features.png"
    img3.save(path3)
    images.append(path3)
    
    # -------------------------------------------------------------
    # SCENE 4: CALL TO ACTION (CTA)
    # -------------------------------------------------------------
    img4 = create_gradient_background(VIDEO_WIDTH, VIDEO_HEIGHT, (10, 8, 26), (32, 16, 52))
    draw4 = ImageDraw.Draw(img4)
    
    draw_pill_badge(draw4, (260, 260, 820, 340), "✨ GET FREE ACCESS ✨", font_badge, fill=(0, 240, 255), text_color=(0, 0, 0))
    
    draw_rounded_card(draw4, (80, 420, 1000, 1100), fill=(20, 16, 42), outline=(255, 215, 0), radius=35, border_width=5)
    
    cta_header = f"TRY {tool_name} NOW"
    bbox_ch = draw4.textbbox((0, 0), cta_header, font=font_title_large)
    draw4.text(((VIDEO_WIDTH - (bbox_ch[2] - bbox_ch[0])) / 2, 500), cta_header, fill=(255, 215, 0), font=font_title_large)
    
    cta_lines = wrap_text("Click the link in bio to try this tool free and save this video for later!", font_heading, 800, draw4)
    y_cta = 660
    for line in cta_lines:
        bbox_l = draw4.textbbox((0, 0), line, font=font_heading)
        draw4.text(((VIDEO_WIDTH - (bbox_l[2] - bbox_l[0])) / 2, y_cta), line, fill=(240, 240, 240), font=font_heading)
        y_cta += 75
        
    draw_pill_badge(draw4, (180, 940, 900, 1040), "🔗 LINK IN BIO ➔", font_heading, fill=(0, 240, 255), text_color=(0, 0, 0))
    
    path4 = temp_dir / "scene_04_cta.png"
    img4.save(path4)
    images.append(path4)
    
    print(f"🎨 4 Scene Images rendered successfully in: {temp_dir}")
    return images
