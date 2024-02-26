from .extensions import db
from .models import User, Session, Participant, SongsQueue, History
from datetime import datetime

def seed_database():
    # Seed User
    user1 = User(username='john_doe', email='john@example.com')
    db.session.add(user1)
    
    # Commit here if you need user IDs for foreign keys in subsequent seeds
    db.session.commit()

    # Seed Session
    session1 = Session(session_code='ABC123')
    db.session.add(session1)
    db.session.commit()
    
    # Seed Participant
    participant1 = Participant(session_id=session1.id, user_id=user1.id)
    db.session.add(participant1)
    db.session.commit()
    
    # Seed SongsQueue
    song1 = SongsQueue(session_id=session1.id, song_title='Song Title', artist='Artist Name', video_link='http://example.com', video_thumbnail='http://example.com/img.jpg', added_by=participant1.id)
    db.session.add(song1)
    
    # Seed History
    history1 = History(user_id=user1.id, song_title='Song Title', artist='Artist Name', video_link='http://example.com')
    db.session.add(history1)
    
    # Commit the transaction
    db.session.commit()

    print("Database seeded successfully.")