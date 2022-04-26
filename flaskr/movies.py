from flask import Blueprint, request, render_template
from flaskr.db import get_movies, get_movie_by_id
import config, json, os
from google.cloud import translate_v2 as translate
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"GoogleCloudKey.json"

bp = Blueprint('movies', __name__, url_prefix='/movies')

DEVELOPER_KEY = config.API_KEY
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(query_term, max_results, page_token=None):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)
    if page_token:
        search_response = youtube.search().list(
            q=query_term,
            part = 'id,snippet',
            maxResults = max_results,
            pageToken = page_token
        ).execute()
    else:
        search_response = youtube.search().list(
            q=query_term,
            part = 'id,snippet',
            maxResults = max_results,
        ).execute()
  
    videos = []
    for search_result in search_response["items"]:
        if search_result['id']['kind'] == 'youtube#video':
            videos.append(search_response['items'][0]['id']['videoId'])
            
    return videos

# https://werkzeug.palletsprojects.com/en/2.0.x/routing/
# Rules that end with a slash are “branches”, others are “leaves”. 
# If strict_slashes is enabled (the default), 
# visiting a branch URL without a trailing slash will redirect to the URL with a slash appended.
@bp.route('/', methods=['GET'], strict_slashes=False)
def movie_list():
    movies = get_movies()
    return render_template('movies.html', movies=movies)

@bp.route('/<int:movieid>/', methods=['GET'], strict_slashes=False)
def movie_id(movieid):
    movie=get_movie_by_id(movieid)
    list_of_videos=youtube_search(movie[0]["title"], 1)
    return render_template('movie.html', movie=movie[0], list_of_videos=list_of_videos[0])

@bp.route('/translate/<int:movieid>/', methods=['GET'], strict_slashes=False)
def translate_movie(movieid):
    movie=get_movie_by_id(movieid)
    translate_client = translate.Client()
    target = "zh-TW"
    text = movie[0]['overview']
    output = translate_client.translate(
        text,
        target_language=target
    )
    text = movie[0]['title']
    outputTitle = translate_client.translate(
        text,
        target_language=target
    )
    return render_template('translate.html', movie=movie[0], output=output, outputTitle=outputTitle)