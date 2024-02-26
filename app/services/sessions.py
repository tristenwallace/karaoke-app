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