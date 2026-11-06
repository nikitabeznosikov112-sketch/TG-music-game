import httpx
import random
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

API_KEY = os.getenv('API_KEY_LAST_FM')
USER_AGENT = "MyMusicApp/1.0"
headers = {'User-Agent': USER_AGENT}

url = "http://ws.audioscrobbler.com/2.0"

async def get_the_tracks(tag):
    params = {
        'method': 'tag.getTopTracks',
        'api_key': API_KEY,
        'limit': 200,
        'tag': tag,
        'format': 'json'
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()

                track_list = data['tracks']['track']
                track1, track2 = random.sample(track_list, 2)

                name1 = track1['name']
                artist1 = track1['artist']['name']
                volume1 = track1["image"][1]['#text']

                name2 = track2['name']
                artist2 = track2['artist']['name']
                volume2 = track2["image"][1]

                print (tag, name1, artist1, name2, artist2 )
                return [{'name': name1, 'artist': artist1, 'volume': volume1},{'name': name2, 'artist': artist2, 'volume': volume2}]
        

            else:
                print(response.status_code)
                return 'Ошибка'
        except Exception as e:
            print (e)
            return 'Ошибка'
    
async def get_the_answer(tracks):
    trackname1 = tracks[0]['name']
    trackartist1 = tracks[0]['artist']

    params = {
        'method': 'track.getInfo',
        'track': trackname1,
        'artist': trackartist1,
        'api_key': API_KEY,
        'format': 'json'
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, headers=headers)

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
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()

                listeners2 = int(data['track']['listeners'])
            else:
                print(response.status_code)
        except Exception as e:
            print(e)

    if listeners1 > listeners2:
        print(tracks[0]['name'])
        return tracks[0]['name']
    else:
        print(tracks[1]['name'])
        return tracks[1]['name']

async def main():
    tracks = await get_the_tracks('rock')
    
    if tracks and tracks != 'Ошибка':
        print(f'Трек1 {tracks[0]["name"]} - {tracks[0]["artist"]}')
        print(f'Трек2 {tracks[1]["name"]} - {tracks[1]["artist"]}')

        answer = await get_the_answer(tracks)
        print(f'Правильный ответ (популярнее): {answer}')
    else:
        print('Ошибка')

if __name__ == "__main__":
    asyncio.run(main())
