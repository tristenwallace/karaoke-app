from .youtube import search_youtube
from app.extensions import db
from app.models import User, Session, Participant, SongsQueue, History
import string
import random

def generate_session_code(length=12):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def create_new_session(username):
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.flush()

    session_code = generate_session_code()
    new_session = Session(session_code=session_code)
    db.session.add(new_session)
    db.session.flush()  # Flush to get the new session's ID
    
    new_participant = Participant(session_id=new_session.id, user_id=new_user.id)
    db.session.add(new_participant)
    db.session.flush()

    db.session.commit()

    return new_session

def get_session_by_code(session_code):
    return Session.query.filter_by(session_code=session_code).first()


def add_song_to_session_queue(session_code, song_title, artist):
    session = Session.query.filter_by(session_code=session_code).first()
    if session:
        # Optionally, search for the song on YouTube to get the video URL and thumbnail
        search_result = search_youtube(f"{song_title} {artist}")
        
        # Check if search_youtube returned an error
        if 'error' in search_result:
            # Handle the error, e.g., by logging it and informing the user
            print(search_result['error'])  # Log the error for debugging
            return {'success':False,
                    'message':search_result['error']}
        
        video_url = search_result.get('video_url', '')
        video_thumbnail = search_result.get('thumbnail_url', '')
        is_embeddable = search_result.get('is_embeddable', '')

        new_song = SongsQueue(
            session_id=session.id,
            song_title=song_title,
            artist=artist,
            video_link=video_url,
            video_thumbnail=video_thumbnail,
            is_embeddable=is_embeddable
        )
        db.session.add(new_song)
        db.session.commit()
        return {'success':True}
    return {'success':False}