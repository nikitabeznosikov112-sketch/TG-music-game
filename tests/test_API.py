from APILogic.MusicGame.PopularityGame import get_the_answer, get_the_tracks
from APILogic.DogsGame.DogsGame import get_dogs
from APILogic.MovieGame.MovieGame import movie_game
from unittest.mock import AsyncMock, patch
import pytest
import httpx

@pytest.mark.asyncio
async def test_get_the_tracks():
    mock_response = httpx.Response(
        status_code=200,
        json={
            'tracks': {
                'track': [
                    {'name': 'Song1', 'artist': {'name': 'Artist1'}},
                    {'name': 'Song2', 'artist': {'name': 'Artist2'}},
                    {'name': 'Song3', 'artist': {'name': 'Artist3'}},
                    {'name': 'Song4', 'artist': {'name': 'Artist4'}}
                ]
            }
        }
    )

    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = mock_response

        result = await get_the_tracks('rock')

        assert result != 'Ошибка'
        assert len(result) == 2
        assert 'name' in result[0]
        assert 'artist' in result[0]
        assert 'name' in result[1]
        assert 'artist' in result[1]

@pytest.mark.asyncio
async def test_get_the_tracks_error_API():
    mock_response = AsyncMock()
    mock_response.status_code = 500
    mock_response.json.return_value = {'error': 'Server error'}

    with patch('httpx.AsyncClient.get', new_callable=AsyncMock) as mock_get:
        mock_get.return_value == mock_response

        result = await get_the_tracks('rock')

        assert result == 'Ошибка в API'

@pytest.mark.asyncio
async def test_get_the_tracks_error_LOGIC():
    mock_response = httpx.Response(
        status_code=200,
        json={
            'tracks': {
                'track': [
                    {'naMe': 'Song1', 'artist': {'name': 'Artist1'}},
                    {'nAme': 'Song2', 'artist': {'name': 'Artist2'}},
                    {'Name': 'Song3', 'artist': {'name': 'Artist3'}},
                    {'namE': 'Song4', 'artist': {'name': 'Artist4'}}
                ]
            }
        }
    )

    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = mock_response

        result = await get_the_tracks('rock')

        assert result == 'Ошибка'

@pytest.mark.asyncio
async def test_get_the_answer():
    tracks = [{'name': 'Track1', 'artist': 'Artist1'}, {'name': 'Track2', 'artist': 'Artist2'}]

    mock_response1 = httpx.Response(status_code=200, json={'track': {'listeners': 1000}})
    mock_response2 = httpx.Response(status_code=200, json={'track': {'listeners': 3000}})

    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.side_effect = [mock_response1, mock_response2]

        result = await get_the_answer(tracks)

        assert result ==  'Track2'

@pytest.mark.asyncio
async def test_get_dogs():
    mock_response = httpx.Response(
        status_code=200,
        json={'message': 'photo'}
    )

    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = mock_response

        result = await get_dogs()

        assert result is not None
        assert isinstance(result, dict)
        assert 'photo' in result
        assert 'correct_answer' in result
        assert 'dogs' in result
        assert result['photo'] == 'photo'

@pytest.mark.asyncio
async def test_get_dogs_error_API():
    mock_response = httpx.Response(
        status_code=500,
        json={'message': 'photo'}
    )

    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = mock_response

        result = await get_dogs()

        assert result == 'Ошибка в API'

@pytest.mark.asyncio
async def test_get_dogs_error_LOGIC():
    mock_response = httpx.Response(
        status_code=200,
        json={'imagePHoto': 'photo'}
    )

    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = mock_response

        result = await get_dogs()

        assert result == 'Ошибка'

@pytest.mark.asyncio
async def test_movie_game():
    mock_response1 = httpx.Response(status_code=200, json={'results': [{'title': 'name1', 'id': 0}, {'title': 'name2', 'id': 1}, {'title': 'name3', 'id': 2}, {'title': 'name4', 'id': 3}, {'title': 'name5', 'id': 4},]})
    mock_response2 = httpx.Response(status_code=200, json={'backdrops': [{'file_path': '/someimage.jpg'}]})

    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.side_effect = [mock_response1, mock_response2]
        result = await movie_game()

        assert result != 'Ошибка в получении фильмов'
        assert result != 'Ошибка в получении постера'
        assert result != 'Ошибка' 
        assert 'movies' in result
        assert 'correct_answer' in result
        assert 'photo' in result

@pytest.mark.asyncio
async def test_movie_game_ERROR_MOVIE():
    mock_response1 = httpx.Response(status_code=404, json={'results': [{'title': 'name1', 'id': 0}, {'title': 'name2', 'id': 1}, {'title': 'name3', 'id': 2}, {'title': 'name4', 'id': 3}, {'title': 'name5', 'id': 4},]})
    mock_response2 = httpx.Response(status_code=200, json={'backdrops': [{'file_path': '/someimage.jpg'}]})

    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.side_effect = [mock_response1, mock_response2]
        result = await movie_game()

        assert result == 'Ошибка в получении фильмов'

@pytest.mark.asyncio
async def test_movie_game_ERROR_PHOTO():
    mock_response1 = httpx.Response(status_code=200, json={'results': [{'title': 'name1', 'id': 0}, {'title': 'name2', 'id': 1}, {'title': 'name3', 'id': 2}, {'title': 'name4', 'id': 3}, {'title': 'name5', 'id': 4},]})
    mock_response2 = httpx.Response(status_code=500, json={'backdrops': [{'file_path': '/someimage.jpg'}]})

    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.side_effect = [mock_response1, mock_response2]
        result = await movie_game()

        assert result == 'Ошибка в получении кадра'

@pytest.mark.asyncio
async def test_movie_game_ERROR_LOGIC():
    mock_response1 = httpx.Response(status_code=200, json={'LLLLLLLL': [{'title': 'name1', 'id': 0}, {'title': 'name2', 'id': 1}, {'title': 'name3', 'id': 2}, {'title': 'name4', 'id': 3}, {'title': 'name5', 'id': 4},]})
    mock_response2 = httpx.Response(status_code=200, json={'OOOOOOOOO': [{'file_path': '/someimage.jpg'}]})

    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.side_effect = [mock_response1, mock_response2]
        result = await movie_game()

        assert result == 'Ошибка'
