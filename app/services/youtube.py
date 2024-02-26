import os
import requests

def search_youtube(query: str) -> str:
    """
    Search for a video on YouTube and return the first result's video URL.

    Args:
        query (str): The search query (song name, artist, etc.).
        api_key (str): The YouTube Data API key.

    Returns:
        str: The URL of the first search result video.
    """
    api_key = os.getenv('YOUTUBE_API_KEY')
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': 'Karafun ' + query,
        'type': 'video',
        'maxResults': 1,
        'key': api_key
    }
    
    
    print("Searching Youtube...")
    
    try:
        search_response = requests.get(search_url, params=params)
        search_result = search_response.json()
        
        # Check if the response status code indicates a successful request
        if search_response.status_code == 200:
            response_json = search_response.json()
            print(search_result)
            if 'items' in search_result and len(search_result['items']) > 0:
                video_id = search_result['items'][0]['id']['videoId']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                thumbnail_url = search_result['items'][0]['snippet']['thumbnails']['high']['url']

                # Check if the video is embeddable
                is_embeddable = is_video_embeddable(video_id, api_key)

                return {
                    'video_url': video_url,
                    'thumbnail_url': thumbnail_url,
                    'is_embeddable': is_embeddable
                }
            else:
                return {"error": "No results found"}
        
        # Handle HTTP errors
        else:
            error_message = f"Failed to search YouTube, status code: {search_response.status_code}"
            if search_result.get('error'):
                error_message += f", message: {search_result['error']['message']}"
            return error_message

    # Handle request exceptions, such as network errors
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while searching YouTube: {str(e)}"}
    


def is_video_embeddable(video_id: str, api_key: str) -> bool:
    videos_url = "https://www.googleapis.com/youtube/v3/videos"
    videos_params = {
        'part': 'status',
        'id': video_id,
        'key': api_key
    }

    try:
        videos_response = requests.get(videos_url, params=videos_params)
        videos_response.raise_for_status()  # Check for HTTP errors
        videos_result = videos_response.json()

        if 'items' in videos_result and len(videos_result['items']) > 0:
            
            # Visually troubleshoot video embeddability 
            print(f"embeddable: {videos_result['items'][0]['status']['embeddable']}")
            print(f"uploadStatus: {videos_result['items'][0]['status']['uploadStatus']}")
            print(f"privacyStatus: {videos_result['items'][0]['status']['privacyStatus']}")
            print(f"publicStatsViewable: {videos_result['items'][0]['status']['publicStatsViewable']}")
            return videos_result['items'][0]['status']['embeddable']

    except requests.exceptions.RequestException:
        return False