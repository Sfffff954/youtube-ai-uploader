# YouTube AI Uploader

Automated video uploader for YouTube with simple AI API integration.

## Features

- ✅ YouTube API Integration
- ✅ Video Upload with Authentication
- ✅ Title, Description and Tags
- ✅ Automatic Token Management
- ✅ OpenAI Text Generation
- ✅ ElevenLabs Voice Generation
- ✅ Stability AI Image Generation

## Installation

### 1. YouTube API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the **YouTube Data API v3**
4. Create OAuth 2.0 Credentials (Desktop Application)
5. Download the JSON file and save it as `client_secrets.json`

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
OPENAI_API_KEY=sk-...your-key-here...
ELEVENLAB_API_KEY=...your-key-here...
STABILITY_API_KEY=...your-key-here...
```

## Quick Start

### Check API Status
```python
from api_manager import APIManager

APIManager.status()
```

### Generate Text with OpenAI
```python
from api_manager import APIManager

text = APIManager.generate_text("Write a song about artificial intelligence")
print(text)
```

### Generate Voice with ElevenLabs
```python
from api_manager import APIManager

APIManager.generate_voice("Hello, this is AI speaking", "output.mp3")
```

### Generate Image with Stability AI
```python
from api_manager import APIManager

APIManager.generate_image("A beautiful sunset with AI", "sunset.png")
```

### Upload Video to YouTube
```python
from uploader import upload_video

upload_video(
    file_path="video.mp4",
    title="My AI Video",
    description="Created with AI automation",
    tags=["ai", "automation", "youtube"],
    category_id="22"
)
```

## Complete Workflow Example

```python
from api_manager import APIManager
from uploader import upload_video
import os

# 1. Generate text
topic = "The Future of AI"
script = APIManager.generate_text(f"Write a 1-minute video script about: {topic}")
print("Generated Script:", script)

# 2. Generate voice
APIManager.generate_voice(script, "video_audio.mp3")

# 3. Generate thumbnail
APIManager.generate_image(f"Professional thumbnail for {topic}", "thumbnail.png")

# 4. Upload to YouTube
video_id = upload_video(
    file_path="my_video.mp4",
    title=topic,
    description=script,
    tags=["ai", "tutorial", topic.lower()],
    category_id="27"  # Education
)
print(f"Video uploaded! https://youtu.be/{video_id}")
```

## YouTube Category IDs

- `1` - Film & Animation
- `2` - Autos & Vehicles
- `10` - Music
- `17` - Sports
- `18` - Short Movies
- `20` - Gaming
- `22` - People & Blogs
- `24` - Entertainment
- `25` - News & Politics
- `26` - Howto & Style
- `27` - Education
- `28` - Science & Technology

[See all categories](https://developers.google.com/youtube/v3/docs/videoCategories)

## File Structure

```
youtube-ai-uploader/
├── uploader.py          # YouTube video upload script
├── api_manager.py       # Centralized API management
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## API Configuration

### OpenAI

Get your API key: https://platform.openai.com/api-keys

Used for:
- Text generation
- Video script writing
- Content ideas

### ElevenLabs

Get your API key: https://elevenlabs.io/

Used for:
- Voice generation
- Voiceovers
- Text-to-speech

### Stability AI

Get your API key: https://platform.stability.ai/

Used for:
- Image generation
- Thumbnail creation
- Visual content

## Authentication

On first run, the YouTube uploader will open a browser window for OAuth authentication. Your token is cached in `token.pickle` and automatically reused for future uploads.

## Security

- `client_secrets.json` - Never commit to git (in .gitignore)
- `token.pickle` - Authentication tokens (in .gitignore)
- `.env` - API keys (in .gitignore)

Always keep your API keys private!

## Troubleshooting

### "OpenAI API Key not configured"
- Check that `.env` file exists
- Verify `OPENAI_API_KEY` is set correctly
- Run `APIManager.status()` to check all APIs

### "YouTube upload fails"
- Ensure `client_secrets.json` exists
- Check that YouTube Data API v3 is enabled
- Try deleting `token.pickle` and authenticating again

### "API rate limit exceeded"
- Wait a few minutes before making new requests
- Check your API usage in respective dashboards

## License

MIT

## Support

For issues and questions:
- GitHub Issues: https://github.com/Sfffff954/youtube-ai-uploader/issues
- OpenAI Docs: https://platform.openai.com/docs
- ElevenLabs Docs: https://elevenlabs.io/docs
- Stability AI Docs: https://platform.stability.ai/docs
- YouTube API Docs: https://developers.google.com/youtube/v3

---

**Happy uploading! 🚀**
