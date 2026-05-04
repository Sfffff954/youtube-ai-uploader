import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google_api_python_client import discovery

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def authenticate():
    """Authentifiziere mit YouTube API"""
    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def upload_video(file_path, title, description, tags=None, category_id='22'):
    """
    Lade ein Video zu YouTube hoch
    
    Args:
        file_path: Pfad zur Videodatei
        title: Video-Titel
        description: Video-Beschreibung
        tags: Liste von Tags (optional)
        category_id: YouTube Kategorie ID (default: 22 = Short Movies)
    """
    creds = authenticate()
    youtube = discovery.build('youtube', 'v3', credentials=creds)
    
    if tags is None:
        tags = []
    
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': 'public'
        }
    }
    
    media = discovery.MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f'Upload Progress: {int(status.progress() * 100)}%')
    
    print(f'✅ Video erfolgreich hochgeladen! Video ID: {response["id"]}')
    return response

if __name__ == '__main__':
    upload_video(
        'video.mp4',
        'Mein erstes AI Video',
        'Dies ist mein erstes automatisch hochgeladenes Video'
    )
