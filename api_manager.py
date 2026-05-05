"""
API Manager - Einfache Verwaltung aller APIs
Nutze einfach: from api_manager import APIManager
"""

import os
from config import OPENAI_API_KEY, ELEVENLAB_API_KEY, STABILITY_API_KEY
from dotenv import load_dotenv

load_dotenv()

class APIManager:
    """Zentrale API-Verwaltung"""
    
    @staticmethod
    def status():
        """Zeige API-Status"""
        print("\n🔧 API Manager Status:")
        print("=" * 50)
        print(f"✅ OpenAI: {OPENAI_API_KEY[:10]}..." if OPENAI_API_KEY else "❌ OpenAI: Nicht konfiguriert")
        print(f"✅ ElevenLabs: {ELEVENLAB_API_KEY[:10]}..." if ELEVENLAB_API_KEY else "❌ ElevenLabs: Nicht konfiguriert")
        print(f"✅ StabilityAI: {STABILITY_API_KEY[:10]}..." if STABILITY_API_KEY else "❌ StabilityAI: Nicht konfiguriert")
        print("=" * 50 + "\n")
    
    @staticmethod
    def generate_text(prompt, api="openai"):
        """
        Text generieren mit OpenAI
        
        Args:
            prompt: Text-Eingabe
            api: Welche API nutzen (default: openai)
        
        Returns:
            Generierter Text
        """
        if not OPENAI_API_KEY:
            return "❌ OpenAI API Key fehlt! Füge ihn in .env ein"
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ Fehler: {str(e)}"
    
    @staticmethod
    def generate_voice(text, output_file="output.mp3", api="elevenlab"):
        """
        Stimme generieren mit ElevenLabs
        
        Args:
            text: Text zum Vorlesen
            output_file: Ausgabedatei
            api: Welche API nutzen (default: elevenlab)
        
        Returns:
            Status-Nachricht
        """
        if not ELEVENLAB_API_KEY:
            return "❌ ElevenLabs API Key fehlt! Füge ihn in .env ein"
        
        try:
            import requests
            from config import ELEVENLAB_VOICE_ID
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLAB_VOICE_ID}"
            headers = {"xi-api-key": ELEVENLAB_API_KEY}
            data = {"text": text, "model_id": "eleven_monolingual_v1"}
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                with open(output_file, "wb") as f:
                    f.write(response.content)
                return f"✅ Audiodatei erstellt: {output_file}"
            else:
                return f"❌ Fehler: {response.status_code}"
        except Exception as e:
            return f"❌ Fehler: {str(e)}"
    
    @staticmethod
    def generate_image(prompt, output_file="image.png", api="stability"):
        """
        Bild generieren mit Stability AI
        
        Args:
            prompt: Bild-Beschreibung
            output_file: Ausgabedatei
            api: Welche API nutzen (default: stability)
        
        Returns:
            Status-Nachricht
        """
        if not STABILITY_API_KEY:
            return "❌ StabilityAI API Key fehlt! Füge ihn in .env ein"
        
        try:
            import requests
            
            url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"
            headers = {
                "Authorization": f"Bearer {STABILITY_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "text_prompts": [{"text": prompt}],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 20
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                image_data = response.json()
                with open(output_file, "wb") as f:
                    f.write(response.content)
                return f"✅ Bild erstellt: {output_file}"
            else:
                return f"❌ Fehler: {response.status_code}"
        except Exception as e:
            return f"❌ Fehler: {str(e)}"

# Beispiel-Nutzung
if __name__ == "__main__":
    APIManager.status()
    
    # Text generieren
    # text = APIManager.generate_text("Schreibe einen kurzen Song")
    # print(text)
    
    # Sprache generieren
    # APIManager.generate_voice(text, "song.mp3")
    
    # Bild generieren
    # APIManager.generate_image("Ein schönes Sonnenuntergang", "sunset.png")
