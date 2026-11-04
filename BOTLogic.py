import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, types
from APILogic import get_the_answer, get_the_tracks, TAGS
import os
from dotenv import load_dotenv
from aiogram.filters import Command
import random
from states import MusicGame

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    try:
        await state.clear()
        tag = random.choice(TAGS)
        tracks = await get_the_tracks(tag)
        if tracks:
            await message.answer(f'Песни получены')
        correct_answer = await get_the_answer(tracks)
        if correct_answer:
            await state.update_data(correct_answer=correct_answer)
            await message.answer(f'Ответ получен')
        keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=tracks[0]['name'])], [KeyboardButton(text=tracks[1]['name'])]], resize_keyboard=True)
        await message.answer(f'{message.from_user.first_name}, как думаешь что популярнее (Жанр: {tag}): {tracks[0]["name"]} -- {tracks[0]["artist"]} ИЛИ {tracks[1]["name"]} -- {tracks[1]["artist"]} ???', reply_markup=keyboard)
        await state.set_state(MusicGame.waiting_for_answer)
    except Exception as e:
        await message.answer('Сорян ошибка')

@dp.message(MusicGame.waiting_for_answer)
async def answer_the_musicgame(message:types.Message, state: FSMContext):
    data = await state.get_data()
    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/start')]], resize_keyboard=True)
    if message.text == data['correct_answer']:
        await message.answer('Красава ответ правильный', reply_markup=keyboard)
        await state.clear()
    else:
        await message.answer(f'Увы ответ не правильный.{data["correct_answer"]} популярнее', reply_markup=keyboard)
        await state.clear()
        
async def main():
    print('Бот запущен . . .')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
