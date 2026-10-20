import subprocess
import shutil
from pathlib import Path
from src.config import VIDEO_WIDTH, VIDEO_HEIGHT, FPS, BGM_DIR, BGM_VOLUME

def get_audio_duration(audio_path: Path) -> float:
    """Get precise duration of audio in seconds via ffprobe"""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(audio_path)
    ]
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode("utf-8").strip()
        return float(output)
    except Exception as e:
        print(f"⚠️ Failed to get audio duration with ffprobe: {e}. Fallback to 30.0s")
        return 30.0

def stitch_video(scene_images: list[Path], audio_path: Path, ass_path: Path, output_mp4: Path) -> Path:
    """
    Assemble scene cards, voiceover audio, BGM and ASS subtitles into final 1080x1920 MP4
    """
    temp_dir = scene_images[0].parent
    total_duration = get_audio_duration(audio_path)
    print(f"⏱️ Total voiceover duration: {total_duration:.2f} seconds")
    
    # Calculate scene timings
    # 4 scenes: Hook (18%), Tool (32%), Features (32%), CTA (18%)
    d1 = max(3.0, total_duration * 0.18)
    d2 = max(5.0, total_duration * 0.32)
    d3 = max(5.0, total_duration * 0.32)
    d4 = max(3.0, total_duration - (d1 + d2 + d3))
    
    durations = [d1, d2, d3, d4]
    
    # Build concat file (using local filenames relative to temp_dir)
    concat_file = temp_dir / "concat.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for img, dur in zip(scene_images, durations):
            f.write(f"file '{img.name}'\n")
            f.write(f"duration {dur:.3f}\n")
        # FFmpeg concat demuxer quirk: repeat last image without duration
        f.write(f"file '{scene_images[-1].name}'\n")
        
    # Check for BGM track
    bgm_candidates = list(BGM_DIR.glob("*.mp3")) + list(BGM_DIR.glob("*.wav"))
    bgm_path = bgm_candidates[0] if bgm_candidates else None
    
    # Copy subtitle to temp_dir if not already there
    local_sub_name = "subtitles.ass"
    dest_ass = temp_dir / local_sub_name
    if ass_path.resolve() != dest_ass.resolve():
        shutil.copy2(ass_path, dest_ass)
        
    dest_voice = temp_dir / "voice.mp3"
    if audio_path.resolve() != dest_voice.resolve():
        shutil.copy2(audio_path, dest_voice)
    
    # Prepare FFmpeg command
    # Run FFmpeg from temp_dir to guarantee no path-escaping / colon bugs on Windows
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "concat.txt",
        "-i", "voice.mp3"
    ]
    
    if bgm_path and bgm_path.exists():
        shutil.copy2(bgm_path, temp_dir / "bgm.wav")
        ffmpeg_cmd.extend(["-stream_loop", "-1", "-i", "bgm.wav"])
        filter_complex = (
            f"[0:v]scale={VIDEO_WIDTH}:{VIDEO_HEIGHT},format=yuv420p,ass={local_sub_name}[v];"
            f"[1:a]volume=1.0[voice];"
            f"[2:a]volume={BGM_VOLUME}[bgm];"
            f"[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[a]"
        )
        ffmpeg_cmd.extend([
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-map", "[a]"
        ])
    else:
        filter_complex = f"[0:v]scale={VIDEO_WIDTH}:{VIDEO_HEIGHT},format=yuv420p,ass={local_sub_name}[v]"
        ffmpeg_cmd.extend([
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-map", "1:a"
        ])
        
    ffmpeg_cmd.extend([
        "-c:v", "libx264",
        "-preset", "faster",
        "-crf", "22",
        "-r", str(FPS),
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(output_mp4.resolve())
    ])
    
    print(f"🎬 Rendering final video with FFmpeg...")
    result = subprocess.run(ffmpeg_cmd, cwd=str(temp_dir), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        err_msg = result.stderr.decode('utf-8', errors='ignore')
        print(f"❌ FFmpeg error: {err_msg[-400:]}")
        raise RuntimeError(f"FFmpeg failed: {err_msg[-200:]}")
        
    print(f"✅ Video rendered successfully: {output_mp4} ({output_mp4.stat().st_size / (1024*1024):.2f} MB)")
    return output_mp4
