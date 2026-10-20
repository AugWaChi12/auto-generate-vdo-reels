import sys
import json
import os
import requests
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, AFFILIATE_BIO_URL, ROOT_DIR

TOKEN_FILE = ROOT_DIR / "token.json"

def get_youtube_service():
    """Build and return an authorized YouTube service instance"""
    token_data = None
    
    # 1. Check environment variable (for GitHub Actions)
    yt_env = os.getenv("YOUTUBE_TOKEN_JSON", "")
    if yt_env:
        try:
            token_data = json.loads(yt_env)
        except Exception:
            token_data = None
            
    # 2. Check local file
    if not token_data and TOKEN_FILE.exists():
        try:
            with open(TOKEN_FILE, "r", encoding="utf-8") as f:
                token_data = json.load(f)
        except Exception:
            token_data = None
            
    if not token_data:
        return None
        
    scopes = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.readonly"]
    creds = Credentials.from_authorized_user_info(token_data, scopes=scopes)
    
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            # Save refreshed token if local file exists
            if TOKEN_FILE.exists():
                token_data["token"] = creds.token
                with open(TOKEN_FILE, "w", encoding="utf-8") as f:
                    json.dump(token_data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to refresh YouTube token: {e}")
            return None
            
    return build("youtube", "v3", credentials=creds, cache_discovery=False)

def upload_to_youtube(video_path: Path, metadata: dict) -> str:
    """Upload video to YouTube Shorts"""
    youtube = get_youtube_service()
    if not youtube:
        print("ℹ️ YouTube service not authenticated. Skipping auto-upload.")
        return ""
        
    title = metadata.get("title", "AI Tool Review")
    if "#shorts" not in title.lower():
        title = f"{title} #shorts"
        
    body = {
        "snippet": {
            "title": title[:100],
            "description": metadata.get("description", ""),
            "tags": metadata.get("tags", ["shorts", "aitools", "tech"]),
            "categoryId": "28"  # Science & Technology
        },
        "status": {
            "privacyStatus": os.getenv("YOUTUBE_PRIVACY", "public"),
            "selfDeclaredMadeForKids": False
        }
    }
    
    media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True)
    
    print(f"🚀 Uploading video to YouTube Shorts: {title}...")
    try:
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"   Upload progress: {int(status.progress() * 100)}%")
                
        video_id = response.get("id")
        short_url = f"https://youtube.com/shorts/{video_id}"
        print(f"🎉 YouTube Shorts Published Successfully!")
        print(f"👉 Watch here: {short_url}")
        return short_url
    except Exception as e:
        print(f"⚠️ YouTube upload error: {e}")
        return ""

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

👉 Follow @nextgen_ai_hacks for daily secret AI tools that feel illegal to know!

{hashtags}
#aitools #artificialintelligence #productivity #futuretech #trending #shorts
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
        
    return metadata

def send_telegram_alert(metadata: dict, video_path: Path, yt_url: str = ""):
    """Optional Telegram alert when video is rendered"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
        
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendVideo"
    caption = f"🎬 *New Short Published!*\n\n*Title:* {metadata['title']}\n*Tool:* {metadata['tool_name']}\n*YouTube:* {yt_url}\n*Bio:* {metadata['affiliate_link']}"
    
    try:
        with open(video_path, "rb") as video_file:
            payload = {
                "chat_id": TELEGRAM_CHAT_ID,
                "caption": caption,
                "parse_mode": "Markdown"
            }
            files = {"video": video_file}
            requests.post(url, data=payload, files=files, timeout=60)
    except Exception as e:
        print(f"⚠️ Telegram alert error: {e}")

def publish_video(content: dict, video_path: Path):
    metadata = format_video_metadata(content, video_path)
    
    # 1. Upload to YouTube Shorts
    yt_url = upload_to_youtube(video_path, metadata)
    if yt_url:
        metadata["youtube_url"] = yt_url
        with open(video_path.with_suffix(".json"), "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
            
    # 2. Upload to Facebook Reels
    fb_token = os.getenv("FB_PAGE_ACCESS_TOKEN", "")
    fb_page_id = os.getenv("FB_PAGE_ID", "1294260180447455")
    if fb_token:
        try:
            from src.facebook_uploader import upload_facebook_reel
            fb_desc = f"{metadata.get('title', '')}\n\n{metadata.get('description', '')}"
            fb_video_id = upload_facebook_reel(str(video_path), fb_desc, page_id=fb_page_id, access_token=fb_token)
            if fb_video_id:
                metadata["fb_video_id"] = fb_video_id
                with open(video_path.with_suffix(".json"), "w", encoding="utf-8") as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Facebook Reels upload error: {e}")
            
    send_telegram_alert(metadata, video_path, yt_url)
    return metadata
