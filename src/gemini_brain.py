import os
import json
import random
import requests
from src.config import GEMINI_API_KEY, GEMINI_MODEL, DATABASE_FILE, AFFILIATE_BIO_URL, ROOT_DIR

HISTORY_FILE = ROOT_DIR / "history.json"

PRIMARY_MONETIZATION_TOOLS = [
    {
        "name": "ElevenLabs",
        "category": "VOICE & AUDIO AI",
        "rating": "9.9/10",
        "tagline": "The Most Realistic Voice AI on Earth"
    },
    {
        "name": "Gamma App",
        "category": "PRESENTATION & DOC AI",
        "rating": "9.8/10",
        "tagline": "Build Beautiful Decks in 30s"
    },
    {
        "name": "Descript",
        "category": "VIDEO & AUDIO EDITOR",
        "rating": "9.8/10",
        "tagline": "Edit Video Just Like a Text Doc"
    }
]

VIRAL_TRENDING_TOOLS = [
    {"name": "Perplexity AI", "category": "AI SEARCH ENGINE", "rating": "9.9/10", "tagline": "The AI Search That Beats Google"},
    {"name": "Notion AI", "category": "PRODUCTIVITY WORKSPACE", "rating": "9.8/10", "tagline": "Your Second Brain On Autopilot"},
    {"name": "Runway Gen-2", "category": "AI VIDEO GENERATOR", "rating": "9.9/10", "tagline": "Text To Cinematic Video In Seconds"},
    {"name": "Cursor AI", "category": "AI CODING ASSISTANT", "rating": "9.9/10", "tagline": "The Future of Coding is Here"},
    {"name": "Midjourney", "category": "HYPER-REALISTIC IMAGES", "rating": "9.9/10", "tagline": "Photorealistic AI Art in Seconds"},
    {"name": "Suno AI", "category": "FULL SONG GENERATOR", "rating": "9.8/10", "tagline": "Create Full Radio Hit Songs Instantly"},
    {"name": "Leonardo AI", "category": "STUDIO ASSET GENERATOR", "rating": "9.8/10", "tagline": "Game & Studio Assets in 1-Click"},
    {"name": "HeyGen", "category": "AI AVATAR VIDEO", "rating": "9.8/10", "tagline": "Create Studio Avatars Without Cameras"}
]

ANGLES = [
    {
        "name": "TIME-CRUNCH / LAZY PRODUCTIVITY",
        "hook_guide": "Focus on saving 5-10 hours of exhausting manual work. Example: 'Stop wasting 5 hours doing X manually... This secret AI does it in 30 seconds.'"
    },
    {
        "name": "SECRET CREATOR / HOLLYWOOD PRODUCTION HACK",
        "hook_guide": "Focus on how top YouTubers and studios get million-dollar quality on a zero budget. Example: 'How creators are secretly producing Hollywood-level content without spending a dime.'"
    },
    {
        "name": "THE ILLEGAL CHEAT CODE / UNFAIR ADVANTAGE",
        "hook_guide": "Frame the tool as an unfair secret weapon that 99% of people have no idea exists. Example: 'This free AI tool feels completely illegal to know, but nobody is talking about it.'"
    },
    {
        "name": "FUTURE SHOCK / TRADITIONAL SOFTWARE IS DEAD",
        "hook_guide": "Declare traditional manual software obsolete. Example: 'Doing X the old way is officially dead. This free AI tool replaced my entire workflow in 1 click.'"
    }
]

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
    history.append(tool_name)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def select_candidate_tool(tool_hint: str = None) -> tuple[dict, bool]:
    """
    70/30 Strategy:
    - 70% chance: Select from Primary Monetization Tools (ElevenLabs, Gamma, Descript)
    - 30% chance: Select from Viral Trending Tools (Perplexity, Runway, etc.)
    """
    if tool_hint:
        for t in PRIMARY_MONETIZATION_TOOLS + VIRAL_TRENDING_TOOLS:
            if t["name"].lower() == tool_hint.lower():
                return t, True
        return {"name": tool_hint, "category": "AI SOFTWARE", "rating": "9.8/10", "tagline": "Next-Gen AI Tool"}, False

    history = load_history()
    recent_tools = history[-4:] if history else []

    # 70% Primary Monetization, 30% Viral
    is_primary = random.random() < 0.70

    if is_primary:
        # Pick a monetization tool that wasn't the immediate last one
        candidates = [t for t in PRIMARY_MONETIZATION_TOOLS if t["name"] not in recent_tools[:1]]
        if not candidates:
            candidates = PRIMARY_MONETIZATION_TOOLS
        selected = random.choice(candidates)
        return selected, True
    else:
        candidates = [t for t in VIRAL_TRENDING_TOOLS if t["name"] not in recent_tools]
        if not candidates:
            candidates = VIRAL_TRENDING_TOOLS
        selected = random.choice(candidates)
        return selected, False

def generate_short_content(tool_hint: str = None) -> dict:
    """
    Generate viral Short script via Gemini API using the 70/30 Angle Rotation Strategy.
    Guarantees dynamic, non-repetitive scripts that comply with YouTube & Meta spam policies.
    """
    candidate, is_monetization = select_candidate_tool(tool_hint)
    angle = random.choice(ANGLES)

    tool_name = candidate["name"]
    category = candidate.get("category", "AI SOFTWARE")
    rating = candidate.get("rating", "9.8/10")
    tagline = candidate.get("tagline", "Next-Gen AI Tool")

    print(f"🎯 Target Tool: {tool_name} ({'Primary Monetization' if is_monetization else 'Viral Traffic Booster'})")
    print(f"📐 Selected Angle: {angle['name']}")

    if not GEMINI_API_KEY:
        print("ℹ️ GEMINI_API_KEY not detected. Using structured fallback.")
        content = {
            "title": f"This AI Tool Feels Totally Illegal To Know... 🤯 ({tool_name})",
            "tool_name": tool_name,
            "category": category,
            "rating": rating,
            "tagline": tagline,
            "hook": f"Stop wasting hours on manual work! This free AI tool called {tool_name} will 10x your speed.",
            "features": [
                f"100% automated {category.lower()} in seconds",
                "Built for creators, students & professionals",
                "Completely free to test out today"
            ],
            "cta": "Link to try this free is in our bio! Follow @nextgen_ai_hacks for daily secret tech.",
            "voice_script": f"Stop wasting hours on manual work! This free AI tool called {tool_name} will ten x your speed. First, it automates your workflow in seconds. Second, it is built specifically for creators and professionals. And third, you can try it completely free today. Grab the free link in our bio, and follow NextGen AI Hacks for daily secret tech!",
            "hashtags": ["#shorts", "#aitools", "#techhacks", "#productivity"]
        }
        save_to_history(tool_name)
        return content

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

    prompt = f"""
    You are an elite YouTube Shorts & Facebook Reels creator for tech brand 'NextGen AI Hacks'.
    Create a high-retention 35-42 second video script in English reviewing: '{tool_name}'.

    CATEGORY: {category}
    CURRENT EPISODE ANGLE: {angle['name']}
    HOOK GUIDELINE: {angle['hook_guide']}

    STRICT VIRAL FORMULA:
    1. 0-3s HOOK: High-energy, curiosity-driven opening sentence following the specified angle.
    2. 3-25s BODY: 3 mind-blowing, specific practical use-cases / features explained in conversational English. Avoid technical jargon.
    3. 25-35s CTA: Direct the viewer to the link in bio to try it free and follow for daily secret AI hacks.

    RULES:
    - Never sound generic. Talk about real-world scenarios (saving time, making money, creating better content).
    - Total voiceover script MUST be between 70 and 85 words so spoken length is exactly 30-38 seconds.

    OUTPUT REQUIREMENT:
    Return ONLY a valid JSON object (no markdown, no quotes around output) with these exact keys:
    {{
        "title": "Clickbait yet accurate Shorts title with 1 emoji",
        "tool_name": "{tool_name}",
        "category": "{category}",
        "rating": "{rating}",
        "tagline": "{tagline}",
        "hook": "Opening 1-2 sentences hook",
        "features": [
            "Feature 1 (max 8 words)",
            "Feature 2 (max 8 words)",
            "Feature 3 (max 8 words)"
        ],
        "cta": "Closing call to action directing to link in bio",
        "voice_script": "Full continuous spoken script under 85 words.",
        "hashtags": ["#shorts", "#aitools", "#techhacks", "#productivity"]
    }}
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.8,
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
            save_to_history(tool_name)
            print(f"✨ Gemini successfully crafted unique script for: {tool_name} [{angle['name']}]")
            return result
        else:
            print(f"⚠️ Gemini API error {resp.status_code}: {resp.text[:120]}")
    except Exception as e:
        print(f"⚠️ Gemini request exception: {e}")

    # Fallback
    save_to_history(tool_name)
    return {
        "title": f"Secret AI Hack: {tool_name} 🤯",
        "tool_name": tool_name,
        "category": category,
        "rating": rating,
        "tagline": tagline,
        "hook": f"Stop wasting hours on manual tasks. This secret AI tool called {tool_name} changes everything.",
        "features": [
            f"Automates {category.lower()} in seconds",
            "Saves 5+ hours of tedious work",
            "100% free to test right now"
        ],
        "cta": "Check the link in bio to try it free! Follow @nextgen_ai_hacks for more.",
        "voice_script": f"Stop wasting hours on manual tasks. This secret AI tool called {tool_name} changes everything. First, it automates your workflow in seconds. Second, it saves you over five hours of tedious work every single week. And third, it is completely free to start. Grab the link in our bio right now, and follow NextGen AI Hacks for daily secret tech!",
        "hashtags": ["#shorts", "#aitools", "#techhacks", "#productivity"]
    }
