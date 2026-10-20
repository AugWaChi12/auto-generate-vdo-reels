import sys
import time
import shutil
from pathlib import Path
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
from src.config import OUTPUT_DIR
from src.gemini_brain import generate_short_content
from src.voice_engine import synthesize_voice
from src.visual_engine import generate_scene_images
from src.video_stitcher import stitch_video
from src.uploader import publish_video

def run_pipeline(tool_hint: str = None) -> Path:
    start_time = time.time()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_id = f"short_{timestamp}"
    
    work_dir = OUTPUT_DIR / run_id
    work_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n🚀 ===================================================")
    print(f"🎬 Starting Auto Shorts Pipeline: {run_id}")
    print(f"===================================================\n")
    
    # 1. Brain & Script
    print("🧠 Step 1: Generating viral script and hooks...")
    content = generate_short_content(tool_hint)
    print(f"📌 Tool Selected: {content.get('tool_name')}")
    print(f"📝 Title: {content.get('title')}")
    
    # 2. Voice & Subtitles
    print("\n🗣️ Step 2: Synthesizing voiceover & word-timed subtitles...")
    audio_path = work_dir / "voice.mp3"
    ass_path = work_dir / "subtitles.ass"
    synthesize_voice(content["voice_script"], audio_path, ass_path)
    
    # 3. Visuals & Graphics
    print("\n🎨 Step 3: Rendering dynamic 1080x1920 scene cards...")
    scene_images = generate_scene_images(content, work_dir)
    
    # 4. Video Assembly
    print("\n🎞️ Step 4: Stitching audio, visuals, BGM & animated subtitles...")
    final_video = OUTPUT_DIR / f"{run_id}.mp4"
    stitch_video(scene_images, audio_path, ass_path, final_video)
    
    # 5. Metadata & Publishing
    print("\n📦 Step 5: Generating metadata and publishing alerts...")
    publish_video(content, final_video)
    
    elapsed = time.time() - start_time
    print(f"\n🎉 ===================================================")
    print(f"✅ Pipeline Completed in {elapsed:.2f} seconds!")
    print(f"📹 Final Output Video: {final_video}")
    print(f"===================================================\n")
    
    return final_video

if __name__ == "__main__":
    run_pipeline()
