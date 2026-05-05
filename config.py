"""
Zentrale Konfiguration für alle APIs
Einfach hier die API-Keys eintragen!
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# YOUTUBE API
# ============================================
YOUTUBE_CLIENT_SECRET = "client_secrets.json"
YOUTUBE_TOKEN_FILE = "token.pickle"

# ============================================
# OPENAI API (für Video-Generierung/Text)
# ============================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4"  # oder "gpt-3.5-turbo"

# ============================================
# ELEVENLAB API (für Audio/Stimmen)
# ============================================
ELEVENLAB_API_KEY = os.getenv("ELEVENLAB_API_KEY", "")
ELEVENLAB_VOICE_ID = os.getenv("ELEVENLAB_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")

# ============================================
# STABILITYAI API (für Bilder)
# ============================================
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY", "")

# ============================================
# VIDEO EINSTELLUNGEN
# ============================================
VIDEO_SETTINGS = {
    "title": os.getenv("VIDEO_TITLE", "Mein Video"),
    "description": os.getenv("VIDEO_DESCRIPTION", ""),
    "tags": ["ai", "automation"],
    "category_id": "22",  # People & Blogs
    "privacy": "public"  # public, unlisted, private
}

# ============================================
# VERFÜGBARE DIENSTE PRÜFEN
# ============================================
def check_apis():
    """Zeigt welche APIs konfiguriert sind"""
    print("\n📊 API Status:")
    print("=" * 40)
    print(f"✅ YouTube: Konfiguriert" if os.path.exists(YOUTUBE_CLIENT_SECRET) else "❌ YouTube: Fehlt client_secrets.json")
    print(f"✅ OpenAI: {OPENAI_API_KEY[:10]}..." if OPENAI_API_KEY else "❌ OpenAI: Fehlt API Key")
    print(f"✅ ElevenLabs: {ELEVENLAB_API_KEY[:10]}..." if ELEVENLAB_API_KEY else "❌ ElevenLabs: Fehlt API Key")
    print(f"✅ StabilityAI: {STABILITY_API_KEY[:10]}..." if STABILITY_API_KEY else "❌ StabilityAI: Fehlt API Key")
    print("=" * 40 + "\n")

if __name__ == "__main__":
    check_apis()
