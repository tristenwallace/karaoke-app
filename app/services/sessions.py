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

        # Determine the new song's order by finding the current maximum order in the queue and adding 1
        max_order = db.session.query(db.func.max(SongsQueue.order)).filter_by(session_id=session.id).scalar()
        new_order = (max_order or 0) + 1

        new_song = SongsQueue(
            session_id=session.id,
            song_title=song_title,
            artist=artist,
            video_link=video_url,
            video_thumbnail=video_thumbnail,
            is_embeddable=is_embeddable,
            order=new_order  # Set the new song's order
        )
        
        db.session.add(new_song)
        db.session.commit()
        return {'success':True}
    return {'success':False}


def reorder_songs_in_queue(session_code, dragged_id, target_id):
    session = Session.query.filter_by(session_code=session_code).first()
    if not session:
        return False, "Session not found"

    try:
        # Fetch all songs in the current session ordered by their current order
        songs_in_queue = SongsQueue.query.filter_by(session_id=session.id).order_by(SongsQueue.order).all()
        song_ids_in_order = [song.id for song in songs_in_queue]

        # Find the current indexes of the dragged and target songs
        dragged_index = song_ids_in_order.index(int(dragged_id))
        target_index = song_ids_in_order.index(int(target_id))

        # Move the dragged song to its new position
        song_ids_in_order.insert(target_index, song_ids_in_order.pop(dragged_index))

        # Update the order of all songs in the queue
        for new_order, song_id in enumerate(song_ids_in_order, start=1):
            song = SongsQueue.query.get(song_id)
            song.order = new_order

        db.session.commit()
        
        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def advance_to_next_song(session_code, current_song_id):
    current_song = SongsQueue.query.get(current_song_id)
    if current_song:
        # Mark the current song as played
        current_song.played = True
        db.session.commit()

        # Fetch the next song in the queue
        next_song = SongsQueue.query.filter(
            SongsQueue.session_id == current_song.session_id,
            SongsQueue.id > current_song_id,
            SongsQueue.played == False
        ).order_by(SongsQueue.order).first()

        if next_song:
            # Prepare and return the next song details
            return {
                'success': True,
                'nextSongId': next_song.id,
                'videoLink': next_song.video_link,
                'isEmbeddable': next_song.is_embeddable,
                'thumbnailUrl': next_song.video_thumbnail
            }
        else:
            # No more songs in the queue
            return {'success': False, 'message': 'End of queue'}
    else:
        return {'success': False, 'message': 'Current song not found'}