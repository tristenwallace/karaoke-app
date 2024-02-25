from flask import Blueprint, request, jsonify
from app.services.youtube import search_youtube

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/search', methods=['GET'])
def youtube_search():
    print("YouTube search route accessed.")
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'Missing query parameter'}), 400

    result = search_youtube(query)
    if 'error' not in result:
        return jsonify(result)
    else:
        return jsonify({'error': result['error']}), 404