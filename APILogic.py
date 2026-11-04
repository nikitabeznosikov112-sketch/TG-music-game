import requests
import random
from dotenv import load_dotenv
import os

load_dotenv()

TAGS = ['rock', 'hiphop', 'indie', 'jazz', '80-s', 'acoustic', 'rnb', 'dance', 'hardcore', 'rap', 'country', 'alternative']
API_KEY = os.getenv('API_KEY')
USER_AGENT = "MyMusicApp/1.0"
headers = {'User-Agent': USER_AGENT}

url = "http://ws.audioscrobbler.com/2.0"

def get_the_tracks(tag):

    params = {
        'method': 'tag.getTopTracks',
        'api_key': API_KEY,
        'limit': 50,
        'tag': tag,
        'format': 'json'
    }

    try:
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()

            track_list = data['tracks']['track']
            track1, track2 = random.sample(track_list, 2)

            name1 = track1['name']
            artist1 = track1['artist']['name']

            name2 = track2['name']
            artist2 = track2['artist']['name']

            print (tag, name1, artist1, name2, artist2 )
            return [{'name': name1, 'artist': artist1},{'name': name2, 'artist': artist2}]
        

        else:
            print(response.status_code)
            return 'Ошибка'
    except Exception as e:
        print (e)
        return 'Ошибка'
    
def get_the_answer(tracks):
    trackname1 = tracks[0]['name']
    trackartist1 = tracks[0]['artist']

    params = {
        'method': 'track.getInfo',
        'track': trackname1,
        'artist': trackartist1,
        'api_key': API_KEY,
        'format': 'json'
    }

    try:
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()

            listeners1 = int(data['track']['listeners'])
        else:
            print(response.status_code)
    except Exception as e:
        print(e)


    trackname2 = tracks[1]['name']
    trackartist2 = tracks[1]['artist']

    params = {
        'method': 'track.getInfo',
        'track': trackname2,
        'artist': trackartist2,
        'api_key': API_KEY,
        'format': 'json'
    }

    try:
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()

            listeners2 = int(data['track']['listeners'])
        else:
            print(response.status_code)
    except Exception as e:
        print(e)

    if listeners1 > listeners2:
        return tracks[0]['name']
    else:
        return tracks[1]['name']

tracks = get_the_tracks('rock')
if tracks and tracks != 'Ошибка':

    print(f'Трек1 {tracks[0]["name"]} - {tracks[0]["artist"]}')
    print(f'Трек2 {tracks[1]["name"]} - {tracks[1]["artist"]}')

    answer = get_the_answer(tracks)
    print(f'правильный ответ(поплуярнее): {answer}')
else:
    print('Ошибка')
            
