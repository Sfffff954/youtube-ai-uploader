# YouTube AI Video Uploader

Ein minimales Python-Tool zum automatischen Hochladen von Videos zu YouTube über die YouTube Data API.

## Installation

1. **Dependencies installieren:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Google Cloud Setup:**
   - Gehe zu https://console.cloud.google.com/
   - Erstelle ein neues Projekt
   - Aktiviere die "YouTube Data API v3"
   - Gehe zu "Credentials" → "OAuth 2.0 Client ID" → "Desktop Application"
   - Lade die JSON-Datei herunter und speichere sie als `client_secrets.json`

## Verwendung

```python
from uploader import upload_video

upload_video(
    'path/to/video.mp4',
    'Video Titel',
    'Video Beschreibung',
    tags=['tag1', 'tag2'],
    category_id='22'
)
```

## Parameter

- `file_path`: Pfad zur MP4-Videodatei
- `title`: Video-Titel
- `description`: Video-Beschreibung
- `tags`: Liste von Tags (optional)
- `category_id`: YouTube Kategorie ID (default: 22 = Short Movies)

## Kategorie IDs

- 2 = Auto & Vehicles
- 10 = Music
- 15 = Pets & Animals
- 17 = Sports
- 18 = Short Movies
- 19 = Travel & Events
- 20 = Gaming
- 21 = Videoblogging
- 22 = Short Movies
- 24 = Entertainment
- 25 = News & Politics
- 26 = Howto & Style
- 27 = Education
- 28 = Science & Technology

## Sicherheit

- `client_secrets.json` und `token.pickle` werden nicht ins Repository gepusht (siehe `.gitignore`)
- Token werden lokal gespeichert
