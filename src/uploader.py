import json
import os
import requests
from pathlib import Path
from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, AFFILIATE_BIO_URL

def format_video_metadata(content: dict, video_path: Path) -> dict:
    tool_name = content.get("tool_name", "AI Tool")
    title = content.get("title", f"Insane AI Tool You Need To Try ({tool_name})")
    hashtags = " ".join(content.get("hashtags", ["#shorts", "#aitools", "#tech", "#productivity"]))
    
    description = f"""🔥 Featured Tool: {tool_name}
🚀 Try it free here: {AFFILIATE_BIO_URL}

{content.get('hook', '')}

Key Features:
- {content.get('features', [''])[0]}
- {content.get('features', ['', ''])[1]}
- {content.get('features', ['', '', ''])[2]}

👉 Follow for daily secret AI tools that feel illegal to know!

{hashtags}
#aitools #artificialintelligence #productivity #futuretech #trending
"""
    metadata = {
        "title": title,
        "description": description,
        "tags": content.get("hashtags", ["shorts", "aitools", "tech", "productivity"]),
        "tool_name": tool_name,
        "video_path": str(video_path),
        "affiliate_link": AFFILIATE_BIO_URL
    }
    
    meta_path = video_path.with_suffix(".json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
        
    print(f"📋 Metadata generated: {meta_path}")
    return metadata

def send_telegram_alert(metadata: dict, video_path: Path):
    """Optional Telegram alert when video is rendered"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
        
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
    caption = f"🎬 *New AI Short Generated!*\n\n*Title:* {metadata['title']}\n*Tool:* {metadata['tool_name']}\n*Link:* {metadata['affiliate_link']}"
    
    try:
        with open(video_path, "rb") as video_file:
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "caption": caption,
                "parse_mode": "Markdown"
            }
            files = {"video": video_file}
            resp = requests.post(url, data=payload, files=files, timeout=60)
            if resp.status_code == 200:
                print("📲 Telegram notification sent successfully!")
            else:
                print(f"⚠️ Telegram API response: {resp.status_code}")
    except Exception as e:
        print(f"⚠️ Failed to send Telegram alert: {e}")

def publish_video(content: dict, video_path: Path):
    metadata = format_video_metadata(content, video_path)
    send_telegram_alert(metadata, video_path)
    return metadata
