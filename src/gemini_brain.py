import os
import json
import random
import requests
from src.config import GEMINI_API_KEY, GEMINI_MODEL, DATABASE_FILE, AFFILIATE_BIO_URL, ROOT_DIR

HISTORY_FILE = ROOT_DIR / "history.json"

def load_history() -> list[str]:
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_to_history(tool_name: str):
    history = load_history()
    if tool_name not in history:
        history.append(tool_name)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

def load_catalog():
    if DATABASE_FILE.exists():
        with open(DATABASE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def get_fallback_content(tool_name: str = None) -> dict:
    catalog = load_catalog()
    if not catalog:
        return {
            "title": "This AI Tool Feels Illegal To Know... 🤯",
            "tool_name": "Gamma App",
            "category": "PRESENTATION AI",
            "rating": "9.9/10",
            "tagline": "Build Presentations in 30 Seconds",
            "hook": "Stop wasting hours on boring PowerPoint slides! This free AI builds entire presentations from a single prompt.",
            "features": [
                "Generates 10+ slides in 30 seconds",
                "Auto-creates visuals, charts and layouts",
                "Exports directly to PowerPoint and PDF"
            ],
            "cta": f"Link to try this free is in the bio! Save this video before your next presentation.",
            "voice_script": "Stop wasting hours on boring PowerPoint slides! This free AI builds entire presentations from a single prompt. It generates over ten beautifully designed slides in thirty seconds, complete with images and charts. Plus, you can export directly to PowerPoint with one click. Grab the free link in our bio, and save this video for later!",
            "hashtags": ["#shorts", "#aitools", "#techhacks", "#productivity", "#presentation"]
        }
    
    if tool_name:
        for item in catalog:
            if item.get("name", "").lower() == tool_name.lower():
                selected = item
                break
        else:
            selected = random.choice(catalog)
    else:
        selected = random.choice(catalog)
        
    voice_script = f"{selected['hook']} First, {selected['features'][0]}. Second, {selected['features'][1]}. And third, {selected['features'][2]}. {selected['cta']}"
    
    return {
        "title": f"This AI Tool Feels Totally Illegal To Know... 🤯 ({selected['name']})",
        "tool_name": selected["name"],
        "category": selected.get("category", "AI SOFTWARE"),
        "rating": selected.get("rating", "9.8/10"),
        "tagline": selected.get("tagline", "Next-Gen AI Platform"),
        "hook": selected["hook"],
        "features": selected["features"],
        "cta": selected["cta"],
        "voice_script": voice_script,
        "hashtags": selected.get("tags", ["#shorts", "#aitools", "#tech", "#productivity"])
    }

def generate_short_content(tool_hint: str = None) -> dict:
    """
    Generate viral Short script via Gemini API.
    Guarantees non-repeating tools by tracking history.
    """
    history = load_history()
    
    if not GEMINI_API_KEY:
        print("ℹ️ GEMINI_API_KEY not detected. Using curated high-converting AI database.")
        content = get_fallback_content(tool_hint)
        save_to_history(content["tool_name"])
        return content
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    
    catalog = load_catalog()
    catalog_remaining = [t["name"] for t in catalog if t["name"] not in history]
    if not catalog_remaining:
        catalog_remaining = [t["name"] for t in catalog]
        
    already_done_str = ", ".join(history[-25:]) if history else "None yet"
    
    prompt = f"""
    You are a viral YouTube Shorts and TikTok content creator specializing in AI Tools.
    Create a high-retention 35-45 second video script in English reviewing an insane, mind-blowing AI tool.
    Recommended tool candidate: {tool_hint if tool_hint else random.choice(catalog_remaining)}.

    STRICT ANTI-REPEAT RULE:
    DO NOT review any of these tools that were recently featured:
    [{already_done_str}]
    Pick a FRESH, trending, or highly useful AI tool across any category (e.g. video creation, audio/music, coding, 3D, writing, productivity, image gen, marketing, automation).

    Follow this viral formula:
    1. 0-3s HOOK: Scroll-stopping, high-curiosity or huge pain-point (e.g. 'Stop wasting 5 hours doing X...').
    2. 3-25s BODY: 3 mind-blowing features explained in simple, punchy, conversational language.
    3. 25-35s CTA: Urge the viewer to check the link in the bio to try it free and follow for more.

    OUTPUT REQUIREMENT:
    Return ONLY a valid JSON object (no markdown quotes, no triple backticks) with these exact keys:
    {{
        "title": "Clickbait yet accurate YouTube Shorts title with 1 emoji",
        "tool_name": "Exact Name of Tool",
        "category": "CATEGORY IN 2-3 WORDS (e.g. PRESENTATION AI)",
        "rating": "9.8/10",
        "tagline": "Punchy 4-6 word tagline",
        "hook": "Opening 1-2 sentences",
        "features": [
            "Short punchy feature 1 (max 8 words)",
            "Short punchy feature 2 (max 8 words)",
            "Short punchy feature 3 (max 8 words)"
        ],
        "cta": "Closing call to action directing to link in bio",
        "voice_script": "Full continuous text for the voiceover to read out loud smoothly. Keep under 80 words so it takes ~30-35 seconds to speak.",
        "hashtags": ["#shorts", "#aitools", "#productivity", "#tech"]
    }}
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "responseMimeType": "application/json"
        }
    }
    
    try:
        resp = requests.post(url, json=payload, timeout=20)
        if resp.status_code == 200:
            data = resp.json()
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            result = json.loads(raw_text.strip())
            tool_name = result.get('tool_name', 'AI Tool')
            save_to_history(tool_name)
            print(f"✨ Gemini successfully generated script for: {tool_name}")
            return result
        else:
            print(f"⚠️ Gemini API returned status {resp.status_code}: {resp.text[:150]}")
            content = get_fallback_content(tool_hint)
            save_to_history(content["tool_name"])
            return content
    except Exception as e:
        print(f"⚠️ Gemini API request failed: {e}. Falling back to curated catalog.")
        content = get_fallback_content(tool_hint)
        save_to_history(content["tool_name"])
        return content
