from flask import Blueprint, request, redirect, url_for, render_template, flash
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
    session = sessions.get_session_by_code(session_code)
    if session is None:
        # Handle the case where the session does not exist
        pass  # Implement as needed
    return render_template('session.html', session=session)

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

@bp.route('/search')
def temp_search():
    return render_template('search.html')