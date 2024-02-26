from flask import Blueprint, request, redirect, url_for, render_template, flash
from ..models import SongsQueue
from app.services import sessions

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        new_session = sessions.create_new_session(username)
        return redirect(url_for('main.session', session_code=new_session.session_code))
    return render_template('index.html')


@bp.route('/session/<session_code>')
def session(session_code):
    session_obj = sessions.get_session_by_code(session_code)
    if session_obj is None:
        # Handle the case where the session does not exist
        return "Session not found", 404
    song_queue = SongsQueue.query.filter_by(session_id=session_obj.id).all()
    return render_template('session.html', 
                            session=session_obj, 
                            song_queue=song_queue
                            )


@bp.route('/session/<session_code>/add_song', methods=['POST'])
def add_song_to_queue(session_code):
    song_title = request.form.get('song_title')
    artist = request.form.get('artist')

    result = sessions.add_song_to_session_queue(session_code, song_title, artist)
    
    if result['success']:
        flash('Song added to queue successfully', 'success')  # Display success message
        return redirect(url_for('main.session', session_code=session_code))
    else:
        flash(result['message'], 'danger')  # Display error message
        return redirect(url_for('main.session', session_code=session_code))


# temporary route that has song search capabilities
@bp.route('/search')
def temp_search():
    return render_template('search.html')