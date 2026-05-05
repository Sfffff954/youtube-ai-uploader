"""
API Manager - Multi-AI with automatic fallback
Usage: from api_manager import APIManager
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# --- Keys ---
OPENAI_API_KEY       = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY    = os.getenv("ANTHROPIC_API_KEY", "")
GROQ_API_KEY         = os.getenv("GROQ_API_KEY", "")
GEMINI_API_KEY       = os.getenv("GEMINI_API_KEY", "")

ELEVENLAB_API_KEY    = os.getenv("ELEVENLAB_API_KEY", "")
ELEVENLAB_VOICE_ID   = os.getenv("ELEVENLAB_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
OPENAI_TTS_KEY       = os.getenv("OPENAI_API_KEY", "")  # reuse
PYTTSX3_AVAILABLE    = False  # offline fallback

STABILITY_API_KEY    = os.getenv("STABILITY_API_KEY", "")
OPENAI_IMAGE_KEY     = os.getenv("OPENAI_API_KEY", "")
REPLICATE_API_KEY    = os.getenv("REPLICATE_API_KEY", "")

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    pass


class APIManager:

    # ─────────────────────────────────────────────
    # STATUS
    # ─────────────────────────────────────────────

    @staticmethod
    def status():
        keys = {
            "OpenAI":      OPENAI_API_KEY,
            "Anthropic":   ANTHROPIC_API_KEY,
            "Groq":        GROQ_API_KEY,
            "Gemini":      GEMINI_API_KEY,
            "ElevenLabs":  ELEVENLAB_API_KEY,
            "StabilityAI": STABILITY_API_KEY,
            "Replicate":   REPLICATE_API_KEY,
        }
        print("\n🔧 API Manager Status:")
        print("=" * 50)
        for name, key in keys.items():
            if key:
                print(f"✅ {name}: {key[:10]}...")
            else:
                print(f"❌ {name}: not configured")
        print(f"{'✅' if PYTTSX3_AVAILABLE else '❌'} pyttsx3 (offline TTS): {'available' if PYTTSX3_AVAILABLE else 'not installed'}")
        print("=" * 50 + "\n")

    # ─────────────────────────────────────────────
    # TEXT GENERATION
    # ─────────────────────────────────────────────

    @staticmethod
    def generate_text(prompt, prefer=None):
        """
        Generate text with automatic fallback.
        prefer: 'openai' | 'anthropic' | 'groq' | 'gemini'
        """
        providers = ["openai", "anthropic", "groq", "gemini"]
        if prefer and prefer in providers:
            providers = [prefer] + [p for p in providers if p != prefer]

        for provider in providers:
            result = APIManager._text(prompt, provider)
            if not result.startswith("❌"):
                return result
            print(f"[fallback] {provider} failed, trying next...")
        return "❌ All text APIs failed."

    @staticmethod
    def _text(prompt, provider):
        try:
            if provider == "openai":
                if not OPENAI_API_KEY:
                    return "❌ no key"
                from openai import OpenAI
                client = OpenAI(api_key=OPENAI_API_KEY)
                r = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )
                return r.choices[0].message.content

            elif provider == "anthropic":
                if not ANTHROPIC_API_KEY:
                    return "❌ no key"
                import anthropic
                client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
                msg = client.messages.create(
                    model="claude-haiku-4-5",
                    max_tokens=500,
                    messages=[{"role": "user", "content": prompt}]
                )
                return msg.content[0].text

            elif provider == "groq":
                if not GROQ_API_KEY:
                    return "❌ no key"
                from groq import Groq
                client = Groq(api_key=GROQ_API_KEY)
                r = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )
                return r.choices[0].message.content

            elif provider == "gemini":
                if not GEMINI_API_KEY:
                    return "❌ no key"
                import google.generativeai as genai
                genai.configure(api_key=GEMINI_API_KEY)
                model = genai.GenerativeModel("gemini-pro")
                r = model.generate_content(prompt)
                return r.text

        except Exception as e:
            return f"❌ {provider}: {e}"
        return "❌ unknown provider"

    # ─────────────────────────────────────────────
    # VOICE GENERATION
    # ─────────────────────────────────────────────

    @staticmethod
    def generate_voice(text, output_file="output.mp3", prefer=None):
        """
        Generate voice with automatic fallback.
        prefer: 'elevenlab' | 'openai' | 'pyttsx3'
        """
        providers = ["elevenlab", "openai", "pyttsx3"]
        if prefer and prefer in providers:
            providers = [prefer] + [p for p in providers if p != prefer]

        for provider in providers:
            result = APIManager._voice(text, output_file, provider)
            if not result.startswith("❌"):
                return result
            print(f"[fallback] {provider} failed, trying next...")
        return "❌ All voice APIs failed."

    @staticmethod
    def _voice(text, output_file, provider):
        try:
            if provider == "elevenlab":
                if not ELEVENLAB_API_KEY:
                    return "❌ no key"
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLAB_VOICE_ID}"
                r = requests.post(url,
                    headers={"xi-api-key": ELEVENLAB_API_KEY},
                    json={"text": text, "model_id": "eleven_monolingual_v1"})
                if r.status_code == 200:
                    with open(output_file, "wb") as f:
                        f.write(r.content)
                    return f"✅ Voice created: {output_file}"
                return f"❌ elevenlab: {r.status_code}"

            elif provider == "openai":
                if not OPENAI_TTS_KEY:
                    return "❌ no key"
                from openai import OpenAI
                client = OpenAI(api_key=OPENAI_TTS_KEY)
                response = client.audio.speech.create(
                    model="tts-1", voice="alloy", input=text)
                response.stream_to_file(output_file)
                return f"✅ Voice created: {output_file}"

            elif provider == "pyttsx3":
                if not PYTTSX3_AVAILABLE:
                    return "❌ pyttsx3 not installed"
                import pyttsx3
                engine = pyttsx3.init()
                engine.save_to_file(text, output_file)
                engine.runAndWait()
                return f"✅ Voice created (offline): {output_file}"

        except Exception as e:
            return f"❌ {provider}: {e}"
        return "❌ unknown provider"

    # ─────────────────────────────────────────────
    # IMAGE GENERATION
    # ─────────────────────────────────────────────

    @staticmethod
    def generate_image(prompt, output_file="image.png", prefer=None):
        """
        Generate image with automatic fallback.
        prefer: 'stability' | 'openai' | 'replicate'
        """
        providers = ["stability", "openai", "replicate"]
        if prefer and prefer in providers:
            providers = [prefer] + [p for p in providers if p != prefer]

        for provider in providers:
            result = APIManager._image(prompt, output_file, provider)
            if not result.startswith("❌"):
                return result
            print(f"[fallback] {provider} failed, trying next...")
        return "❌ All image APIs failed."

    @staticmethod
    def _image(prompt, output_file, provider):
        try:
            if provider == "stability":
                if not STABILITY_API_KEY:
                    return "❌ no key"
                url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"
                r = requests.post(url,
                    headers={"Authorization": f"Bearer {STABILITY_API_KEY}", "Content-Type": "application/json"},
                    json={"text_prompts": [{"text": prompt}], "cfg_scale": 7,
                          "height": 1024, "width": 1024, "samples": 1, "steps": 20})
                if r.status_code == 200:
                    import base64, json
                    data = r.json()
                    img_b64 = data["artifacts"][0]["base64"]
                    with open(output_file, "wb") as f:
                        f.write(base64.b64decode(img_b64))
                    return f"✅ Image created: {output_file}"
                return f"❌ stability: {r.status_code}"

            elif provider == "openai":
                if not OPENAI_IMAGE_KEY:
                    return "❌ no key"
                from openai import OpenAI
                client = OpenAI(api_key=OPENAI_IMAGE_KEY)
                r = client.images.generate(model="dall-e-3", prompt=prompt, n=1, size="1024x1024")
                img_url = r.data[0].url
                img_data = requests.get(img_url).content
                with open(output_file, "wb") as f:
                    f.write(img_data)
                return f"✅ Image created: {output_file}"

            elif provider == "replicate":
                if not REPLICATE_API_KEY:
                    return "❌ no key"
                import replicate
                output = replicate.run(
                    "stability-ai/sdxl:39ed52f2319f9b6a5d45b6b98caebbaa3a6c3e8b6d5e4d4e5d04d6b0f2c1a3e1",
                    input={"prompt": prompt}
                )
                img_url = output[0]
                img_data = requests.get(img_url).content
                with open(output_file, "wb") as f:
                    f.write(img_data)
                return f"✅ Image created: {output_file}"

        except Exception as e:
            return f"❌ {provider}: {e}"
        return "❌ unknown provider"


if __name__ == "__main__":
    APIManager.status()
