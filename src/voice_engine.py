import asyncio
import edge_tts
from pathlib import Path
from src.config import VOICE_NAME, VOICE_RATE, VOICE_PITCH

def format_ass_time(seconds: float) -> str:
    """Convert seconds to ASS subtitle timestamp format: H:MM:SS.cs"""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    if cs >= 100:
        cs = 99
    return f"{hrs}:{mins:02d}:{secs:02d}.{cs:02d}"

def split_sentence_into_chunks(text: str, start_time: float, duration: float, max_words: int = 5):
    """Split a sentence into smaller punchy chunks for mobile TikTok/Shorts viewing"""
    words = text.strip().split()
    if not words:
        return []
    
    if len(words) <= max_words:
        return [(start_time, start_time + duration, text.strip().upper())]
    
    chunks = []
    chunk_words = []
    for w in words:
        chunk_words.append(w)
        if len(chunk_words) >= max_words:
            chunks.append(" ".join(chunk_words).upper())
            chunk_words = []
    if chunk_words:
        chunks.append(" ".join(chunk_words).upper())
        
    chunk_duration = duration / len(chunks)
    result = []
    for i, c in enumerate(chunks):
        c_start = start_time + (i * chunk_duration)
        c_end = c_start + chunk_duration
        result.append((c_start, c_end, c))
    return result

async def generate_voice_and_subtitles(text: str, audio_path: Path, ass_path: Path, voice: str = VOICE_NAME):
    communicate = edge_tts.Communicate(text, voice=voice, rate=VOICE_RATE, pitch=VOICE_PITCH)
    
    audio_path = Path(audio_path)
    ass_path = Path(ass_path)
    
    sentence_events = []
    
    with open(audio_path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "SentenceBoundary":
                offset_sec = chunk["offset"] / 10_000_000.0
                duration_sec = chunk["duration"] / 10_000_000.0
                sentence_events.append({
                    "start": offset_sec,
                    "duration": duration_sec,
                    "text": chunk.get("text", "")
                })
                
    # Build ASS content
    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,60,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,5,2,2,40,40,320,1
Style: Accent,Arial,64,&H0000E5FF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,5,3,2,40,40,320,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    dialogues = []
    for ev in sentence_events:
        chunks = split_sentence_into_chunks(ev["text"], ev["start"], ev["duration"], max_words=5)
        for i, (c_start, c_end, c_text) in enumerate(chunks):
            # Highlight important trigger words or alternate styles
            style = "Accent" if i % 2 == 1 else "Default"
            start_str = format_ass_time(c_start)
            end_str = format_ass_time(c_end)
            dialogues.append(f"Dialogue: 0,{start_str},{end_str},{style},,0,0,0,,{c_text}")
            
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_header + "\n".join(dialogues) + "\n")
        
    print(f"🎙️ Audio generated: {audio_path} ({len(sentence_events)} sentences)")
    print(f"📝 Subtitles created: {ass_path} ({len(dialogues)} cues)")

def synthesize_voice(text: str, audio_path: Path, ass_path: Path, voice: str = VOICE_NAME):
    asyncio.run(generate_voice_and_subtitles(text, audio_path, ass_path, voice))
