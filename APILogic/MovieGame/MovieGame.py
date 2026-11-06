import httpx
import os
from dotenv import load_dotenv
import asyncio
import random 

load_dotenv()

url_for_getting_films = 'https://api.themoviedb.org/3/movie/popular'
headers = {
    "accept": "application/json",
    "Authorization": os.getenv('AUTHORIZATION_KEY_TMDB')
}
params = {'languages': 'ru-RU', 'page': 1}
async def movie_game():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url_for_getting_films, headers=headers, params=params)

            if response.status_code != 200:
                return None

            movies = response.json()['results']
            game_movies = random.sample(movies, 4)

            random.shuffle(game_movies)

            correct_movie = game_movies[0]
            movie_id = correct_movie['id']

            url_for_getting_answer = f'https://api.themoviedb.org/3/movie/{movie_id}/images'

            image_response = await client.get(url_for_getting_answer, headers=headers)

            photo_url = None

            if image_response.status_code == 200:
                data = image_response.json()
                images = data.get('backdrops', [])

                if images:
                    photo = random.choice(images)
                    photo_url = f"https://image.tmdb.org/t/p/w780{photo['file_path']}"
                else:
                    photo_url = f"https://image.tmdb.org/t/p/w500{correct_movie['poster_path']}"

            return {
                'movies': game_movies,
                'correct_answer': correct_movie['title'],
                'photo': photo_url
            }
        except Exception as e:
            print(e)
