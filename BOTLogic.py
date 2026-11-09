import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

import random
import os
from dotenv import load_dotenv

from repositories.user_repositories import UserRepository
from Database import Session

from APILogic.MusicGame.PopularityGame import get_the_answer, get_the_tracks
from APILogic.MusicGame.MusicTags import TAGSelectronic, TAGSmetal, TAGSpop
from APILogic.MovieGame.MovieGame import movie_game
from APILogic.states import MusicGame, DogGame, MovieGame
from APILogic.DogsGame.DogsGame import get_dogs
from APILogic.DogsGame.dog_translations import DOG_BREEDS_RU

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    session = Session()
    repo = UserRepository(session)
    try:
        user = repo.get_by_id(message.from_user.id)
        if not user:
            repo.create_user(tg_id=message.from_user.id, user_name=message.from_user.first_name)
    finally:
        session.close()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Угадай что популярнее', callback_data="game_music")],
        [InlineKeyboardButton(text='Угадай породу', callback_data="game_dogs")],
        [InlineKeyboardButton(text='Угадай фильм по кадру', callback_data="game_films")]
    ])

    

    await message.answer(f'Салам,{message.from_user.first_name}, во что поиграем?\n\n /stats для просмотра статистики\n/ratings для просмотра рейтинга', reply_markup=keyboard)
    await state.set_state(MusicGame.waiting_for_choice)

@dp.message(Command('stats'))
async def show_stats(message: types.Message):
    session = Session()
    repo = UserRepository(session)
    try:
        score = repo.show_score(message.from_user.id)
    finally:
        session.close()
    await message.answer(f'Пользователь: {message.from_user.full_name}\n\nОчков за правильные ответы:{score}')

@dp.message(Command('ratings'))
async def show_ratings(message: types.Message):
    session = Session()
    repo = UserRepository(session)

    try:
        ratings = repo.get_top()
        if not ratings:
            await message.answer('Никто не играл')
            return
    finally:
        session.close()
    text = '**Топ 10 игроков**\n\n'
    for index, user in enumerate(ratings, start=1):
        name = user.name if user.name else 'Аноним'
        text += f'{index}. {name} -- {user.score} очков\n'
    await message.answer(text, parse_mode='Markdown')

@dp.callback_query(MusicGame.waiting_for_choice, F.data.startswith("game_"))
async def game_choice(callback: types.CallbackQuery, state: FSMContext):
    choice = callback.data

    if choice == 'game_music':
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Рок-Метал', callback_data='metal_genre')],
            [InlineKeyboardButton(text='Поп', callback_data='pop_genre')],
            [InlineKeyboardButton(text='Электроника', callback_data='electro_genre')],
            [InlineKeyboardButton(text='Русская музыка', callback_data='rus_genre')]
        ])
        await callback.message.answer("Отлично, выбери жанр", reply_markup=keyboard)
        await state.set_state(MusicGame.waiting_for_answerGenre)
    elif choice == 'game_dogs':
        data = await get_dogs()

        if not data:
            await callback.message.answer('Ошибка сорян')
            return
        
        dogs = data['dogs']
        correct_answer = data['correct_answer']
        photo = data['photo']

        await state.update_data(correct_answer=correct_answer)

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=DOG_BREEDS_RU.get(dogs[0], dogs[0]), callback_data=f'dog_{dogs[0]}')],
            [InlineKeyboardButton(text=DOG_BREEDS_RU.get(dogs[1], dogs[1]), callback_data=f'dog_{dogs[1]}')],
            [InlineKeyboardButton(text=DOG_BREEDS_RU.get(dogs[2], dogs[2]), callback_data=f'dog_{dogs[2]}')],
            [InlineKeyboardButton(text=DOG_BREEDS_RU.get(dogs[3], dogs[3]), callback_data=f'dog_{dogs[3]}')]
        ])

        await callback.message.answer_photo(photo=photo, caption="Угадай что за порода песеля?", reply_markup=keyboard)

        await state.set_state(DogGame.waiting_for_answer)
    elif choice == 'game_films':
        game_data = await movie_game()
        if not game_data:
            await callback.message.answer('Сорян ошибка')
            return
        movies = game_data['movies']
        titles = [m['title'] for m in movies]
        correct_answer = game_data['correct_answer']
        photo = game_data['photo']

        await state.update_data(correct_answer=correct_answer, titles=titles)

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=titles[0], callback_data="movie_0")],
            [InlineKeyboardButton(text=titles[1], callback_data="movie_1")],
            [InlineKeyboardButton(text=titles[2], callback_data="movie_2")],
            [InlineKeyboardButton(text=titles[3], callback_data="movie-3")]
        ])

        await callback.message.answer_photo(photo=photo, caption='Из какого фильмеца кадр?', reply_markup=keyboard)
        await state.set_state(MovieGame.waiting_for_answer)
    await callback.answer()

@dp.callback_query(MovieGame.waiting_for_answer, F.data.startswith('movie_'))
async def film_game_proccessing(callback: types.CallbackQuery, state: FSMContext):
    session = Session()
    repo = UserRepository(session)

    data = await state.get_data()
    titles = data.get('titles')
    correct_answer = data.get('correct_answer')
    user_idx = int(callback.data.replace('movie_', ''))
    user_choice = titles[user_idx]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Играть еще раз', callback_data='again_movie')],
        [InlineKeyboardButton(text='В меню', callback_data='main_menu')]
    ])
    if user_choice == correct_answer:
        await callback.message.answer('Красава, все правильно', reply_markup=keyboard)
        try:
            repo.add_points(callback.from_user.id, 1)
        finally:
            session.close()
    else:
        await callback.message.answer(f'Неправильно, правильный ответ: {correct_answer}', reply_markup=keyboard)

    await state.set_state(MovieGame.waiting_for_choice)
    await callback.answer()

@dp.callback_query(MovieGame.waiting_for_choice, F.data.in_({'again_movie', 'main_menu'}))
async def choice_film(callback: types.CallbackQuery, state: FSMContext):
    user_choice = callback.data

    if user_choice == 'again_movie':
        game_data = await movie_game()
        if not game_data:
            await callback.message.answer('Сорян ошибка')
            return
        movies = game_data['movies']
        titles = [m['title'] for m in movies]
        correct_answer = game_data['correct_answer']
        photo = game_data['photo']

        await state.update_data(correct_answer=correct_answer, titles=titles)

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=titles[0], callback_data="movie_0")],
            [InlineKeyboardButton(text=titles[1], callback_data="movie_1")],
            [InlineKeyboardButton(text=titles[2], callback_data="movie_2")],
            [InlineKeyboardButton(text=titles[3], callback_data="movie_3")]
        ])

        await callback.message.answer_photo(photo=photo, caption='Из какого фильмеца кадр?', reply_markup=keyboard)
        await state.set_state(MovieGame.waiting_for_answer)

    elif user_choice == 'main_menu':
        await callback.message.answer('Напиши /start')

    await callback.answer()
@dp.callback_query(DogGame.waiting_for_answer, F.data.startswith('dog_'))
async def dogplay_proccess(callback: types.CallbackQuery, state: FSMContext):
    session = Session()
    repo = UserRepository(session)

    data = await state.get_data()
    correct_answer = data.get('correct_answer')
    user_choice = callback.data.replace('dog_', '')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Играть еще раз', callback_data='again_dog')],
        [InlineKeyboardButton(text='В меню',callback_data='main_menu' )]
    ])

    if user_choice == correct_answer:
        await callback.message.answer('Красава, ответ правильный', reply_markup=keyboard)
        try:
            repo.add_points(callback.from_user.id, 1)
        finally:
            session.close()
    else:
        await callback.message.answer(f'Неправильно. Правильный ответ: {DOG_BREEDS_RU.get(correct_answer, correct_answer)}', reply_markup=keyboard)

    await state.set_state(DogGame.waiting_for_choice)
    await callback.answer()

@dp.callback_query(DogGame.waiting_for_choice, F.data.in_({'again_dog', 'main_menu'}))
async def after_dog_choice(callback: types.CallbackQuery, state: FSMContext):
    user_choice = callback.data

    if user_choice == 'main_menu':
        await callback.message.answer('Напиши /start')
    elif user_choice == 'again_dog':
        data = await get_dogs()

        if not data:
            await callback.message.answer('Ошибка сорян')
            return
        
        dogs = data['dogs']
        correct_answer = data['correct_answer']
        photo = data['photo']

        await state.update_data(correct_answer=correct_answer)

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=DOG_BREEDS_RU.get(dogs[0], dogs[0]), callback_data=f'dog_{dogs[0]}')],
            [InlineKeyboardButton(text=DOG_BREEDS_RU.get(dogs[1], dogs[1]), callback_data=f'dog_{dogs[1]}')],
            [InlineKeyboardButton(text=DOG_BREEDS_RU.get(dogs[2], dogs[2]), callback_data=f'dog_{dogs[2]}')],
            [InlineKeyboardButton(text=DOG_BREEDS_RU.get(dogs[3], dogs[3]), callback_data=f'dog_{dogs[3]}')]
        ])

        await callback.message.answer_photo(photo=photo, caption="Угадай что за порода песеля?", reply_markup=keyboard)

        await state.set_state(DogGame.waiting_for_answer)
    await callback.answer()
@dp.callback_query(MusicGame.waiting_for_answerGenre, F.data.endswith('_genre'))
async def play_proccess(callback: types.CallbackQuery, state: FSMContext):
    genre = callback.data
    tag = genre.replace('_genre', '')

    if tag == 'rus':
        tag = 'russian'
    elif tag == 'metal':
        tag = random.choice(TAGSmetal)
    elif tag == 'pop':
        tag = random.choice(TAGSpop)
    elif tag == 'electro':
        tag = random.choice(TAGSelectronic)

    tracks = await get_the_tracks(tag)


    if not tracks or tracks == 'Ошибка':
        await callback.message.answer('Ошибка')
        return
    
    correct_answer = await get_the_answer(tracks)
    await state.update_data(correct_answer=correct_answer, tag=tag)

    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=tracks[0]['name'])],
        [KeyboardButton(text=tracks[1]['name'])]
        ], resize_keyboard=True
    )

    await callback.message.answer(
        f"Что популярнее?\nЖанр: {tag}\n\n{tracks[0]['name']} - {tracks[0]['artist']}\n------------------------------------------\n{tracks[1]['name']} - {tracks[1]['artist']}", reply_markup=keyboard
    )

    await state.set_state(MusicGame.waiting_for_answer)
    await callback.answer()

@dp.message(MusicGame.waiting_for_answer)
async def answer_musgame(message: types.Message, state: FSMContext):
    session = Session()
    repo = UserRepository(session)

    data = await state.get_data()
    correct_answer = data.get('correct_answer')
    tag = data.get('tag')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Играть еще раз', callback_data=f'again_{tag}')],
        [InlineKeyboardButton(text='Выбрать другой жанр', callback_data='change_genre')],
        [InlineKeyboardButton(text='В меню', callback_data='main_menu')]
    ])

    if message.text == correct_answer:
        await message.answer('Красава, ответ правильный', reply_markup=keyboard)
        try:
            repo.add_points(message.from_user.id, 1)
        finally:
            session.close()
    else:
        await message.answer(f'Не правильно. {correct_answer} популярнее', reply_markup=keyboard)

    await state.set_state(MusicGame.waiting_for_choice)

@dp.callback_query(MusicGame.waiting_for_choice, F.data.startswith('again_') | F.data.in_({'change_genre', 'main_menu'}))
async def after_game_choice(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data

    if action.startswith('again_'):
        tag = action.replace('again_', '')
        tracks = await get_the_tracks(tag)

        if not tracks or tracks == 'Ошибка':
            await callback.message.answer('Ошибка')
            return
    
        correct_answer = await get_the_answer(tracks)
        await state.update_data(correct_answer=correct_answer, tag=tag)

        keyboard = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text=tracks[0]['name'])],
            [KeyboardButton(text=tracks[1]['name'])]
            ], resize_keyboard=True
        )

        await callback.message.answer(
            f'Что популярнее?\nЖанр: {tag}\n\n{tracks[0]['name']} - {tracks[0]['artist']}\n------------------------------------------\n{tracks[1]['name']} - {tracks[1]['artist']}', reply_markup=keyboard
        )

        await state.set_state(MusicGame.waiting_for_answer)
        await callback.answer()
    elif action == 'change_genre':
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Рок-Метал', callback_data='metal_genre')],
            [InlineKeyboardButton(text='Поп', callback_data='pop_genre')],
            [InlineKeyboardButton(text='Электроника', callback_data='electro_genre')],
            [InlineKeyboardButton(text='Русская музыка', callback_data='rus_genre')]]
        )

        await callback.message.answer('Выбери жанр', reply_markup=keyboard)
        await state.set_state(MusicGame.waiting_for_answerGenre)

    elif action == 'main_menu':
        await state.clear()
        await callback.message.answer('Напиши /start')

    await callback.answer()

async def main():
    print('Бот запущен . . .')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
