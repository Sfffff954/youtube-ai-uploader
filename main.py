"""
main.py - Full workflow: generate script → voice → thumbnail → upload
Usage: python main.py
"""

import os
import sys
from api_manager import APIManager
from uploader import upload_video

# ─── CONFIG ───────────────────────────────────────────
TOPIC        = "The Future of Artificial Intelligence"
VIDEO_FILE   = "video.mp4"        # must exist before running
AUDIO_FILE   = "audio.mp3"
THUMBNAIL    = "thumbnail.png"
CATEGORY_ID  = "27"               # Education
# ──────────────────────────────────────────────────────


def main():
    print("\n🚀 YouTube AI Uploader - Full Workflow")
    print("=" * 50)

    # 1. Check API status
    APIManager.status()

    # 2. Generate script
    print(f"📝 Generating script for: {TOPIC}")
    script = APIManager.generate_text(
        f"Write a short 1-minute YouTube video script about: {TOPIC}. "
        f"Keep it engaging and educational."
    )
    if script.startswith("❌"):
        print(f"Script generation failed: {script}")
        sys.exit(1)
    print(f"✅ Script generated ({len(script)} chars)\n")

    # 3. Generate voiceover
    print("🎙️ Generating voiceover...")
    voice_result = APIManager.generate_voice(script, AUDIO_FILE)
    print(voice_result)

    # 4. Generate thumbnail
    print("\n🖼️ Generating thumbnail...")
    img_result = APIManager.generate_image(
        f"Professional YouTube thumbnail for: {TOPIC}, vibrant colors, bold text style",
        THUMBNAIL
    )
    print(img_result)

    # 5. Check video file
    if not os.path.exists(VIDEO_FILE):
        print(f"\n⚠️  '{VIDEO_FILE}' not found — skipping upload.")
        print("   Place your video file as 'video.mp4' and re-run to upload.")
        print("\n📋 Generated content:")
        print(f"   Script: saved to memory (print below)")
        print(f"   Audio:  {AUDIO_FILE}")
        print(f"   Image:  {THUMBNAIL}")
        print(f"\n--- SCRIPT ---\n{script}\n")
        return

    # 6. Upload to YouTube
    print("\n📤 Uploading to YouTube...")
    tags = [word.lower() for word in TOPIC.split() if len(word) > 3]
    tags += ["ai", "automation"]

    result = upload_video(
        file_path=VIDEO_FILE,
        title=TOPIC,
        description=script,
        tags=tags,
        category_id=CATEGORY_ID
    )

    if result:
        video_id = result.get("id", "unknown")
        print(f"\n✅ Done! https://youtu.be/{video_id}")
    else:
        print("\n❌ Upload failed.")


if __name__ == "__main__":
    main()
