import os
import sys
import time
import argparse
import requests
from pathlib import Path
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

PAGE_ID = os.environ.get("FB_PAGE_ID", "1294260180447455")
PAGE_ACCESS_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN")

GRAPH_API_VERSION = "v20.0"

def upload_facebook_reel(video_path: str, description: str, page_id: str = None, access_token: str = None):
    pid = page_id or PAGE_ID
    token = access_token or PAGE_ACCESS_TOKEN
    
    if not token:
        raise ValueError("FB_PAGE_ACCESS_TOKEN is required to upload to Facebook Reels.")
    
    video_file = Path(video_path)
    if not video_file.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    file_size = video_file.stat().st_size
    print(f"[Facebook Reels] Starting upload for: {video_file.name} ({file_size / (1024*1024):.2f} MB)")
    print(f"[Facebook Reels] Target Page ID: {pid}")

    # Step 1: Initialize Reel upload
    start_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{pid}/video_reels"
    init_res = requests.post(start_url, data={
        "upload_phase": "start",
        "access_token": token
    })
    
    if init_res.status_code != 200:
        print(f"[Facebook Reels] ERROR initializing upload: {init_res.text}")
        init_res.raise_for_status()
        
    init_data = init_res.json()
    video_id = init_data["video_id"]
    upload_url = init_data["upload_url"]
    print(f"[Facebook Reels] Initialized! Video ID: {video_id}")

    # Step 2: Binary chunk upload
    print("[Facebook Reels] Uploading binary video data...")
    with open(video_file, "rb") as f:
        headers = {
            "Authorization": f"OAuth {token}",
            "offset": "0",
            "file_size": str(file_size),
            "Content-Type": "application/octet-stream"
        }
        upload_res = requests.post(upload_url, headers=headers, data=f)
        
    if upload_res.status_code not in (200, 201):
        print(f"[Facebook Reels] ERROR binary upload: {upload_res.text}")
        upload_res.raise_for_status()
        
    print("[Facebook Reels] Binary upload complete!")

    # Step 3: Finish and Publish
    print("[Facebook Reels] Publishing Reel to Facebook Page...")
    finish_res = requests.post(start_url, data={
        "upload_phase": "finish",
        "access_token": token,
        "video_id": video_id,
        "video_state": "PUBLISHED",
        "description": description
    })
    
    if finish_res.status_code != 200:
        print(f"[Facebook Reels] ERROR publishing reel: {finish_res.text}")
        finish_res.raise_for_status()
        
    finish_data = finish_res.json()
    print(f"[Facebook Reels] SUCCESS! Published successfully: {finish_data}")
    return video_id

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload Facebook Reel")
    parser.add_argument("--video", required=True, help="Path to mp4 video")
    parser.add_argument("--description", default="", help="Caption for reel")
    parser.add_argument("--page_id", default=None, help="Facebook Page ID")
    parser.add_argument("--token", default=None, help="Page Access Token")
    
    args = parser.parse_args()
    upload_facebook_reel(args.video, args.description, args.page_id, args.token)
