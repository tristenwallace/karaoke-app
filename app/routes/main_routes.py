from flask import Blueprint, request, redirect, url_for, render_template, flash, jsonify
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
    song_queue = SongsQueue.query.filter_by(session_id=session_obj.id, played=False).order_by(SongsQueue.order).all()
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


@bp.route('/session/<session_code>/next_song', methods=['POST'])
def next_song(session_code):
    current_song_id = request.json.get('currentSongId')
    result = sessions.advance_to_next_song(session_code, current_song_id)

    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify({'success': False, 'message': result['message']}), 404 if result['message'] == 'End of queue' else 400


@bp.route('/session/<session_code>/reorder', methods=['POST'])
def reorder_queue(session_code):
    data = request.json
    dragged_id = data.get('draggedId')
    target_id = data.get('targetId')

    success, message = sessions.reorder_songs_in_queue(session_code, dragged_id, target_id)
    if success:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'error': message}), 400 if message == "One or more songs not found" else 500


# temporary route that has song search capabilities
@bp.route('/search')
def temp_search():
    return render_template('search.html')