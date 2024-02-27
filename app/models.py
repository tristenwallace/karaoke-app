from .extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False) #FOR DEVELOPMENT: Host logic requires unique users
    email = db.Column(db.String(120), unique=True, nullable=True)
    history = db.relationship('History', backref='user', lazy=True)
    # Consider adding a relationship to Participant if needed

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_code = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    participants = db.relationship('Participant', backref='session', lazy=True)
    songs = db.relationship('SongsQueue', backref='session', lazy=True)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=db.func.now())
    songs_added = db.relationship('SongsQueue', backref='added_by_participant', lazy=True)

class SongsQueue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    song_title = db.Column(db.String(120), nullable=False)
    artist = db.Column(db.String(120), nullable=False)
    video_link = db.Column(db.String(255))
    video_thumbnail = db.Column(db.String(255))
    is_embeddable = db.Column(db.Boolean, default=False)
    added_by = db.Column(db.Integer, db.ForeignKey('participant.id'), nullable=True)
    queued_at = db.Column(db.DateTime, default=db.func.now())
    order = db.Column(db.Integer)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    song_title = db.Column(db.String(120), nullable=False)
    artist = db.Column(db.String(120), nullable=False)
    video_link = db.Column(db.String(255))
    played_at = db.Column(db.DateTime, default=db.func.now())