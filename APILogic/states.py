from aiogram.fsm.state import State, StatesGroup

class MusicGame(StatesGroup):
    waiting_for_choice = State()
    waiting_for_answer = State() 
    waiting_for_answerGenre = State()

class DogGame(StatesGroup):
    waiting_for_answer = State()
    waiting_for_choice = State()

class MovieGame(StatesGroup):
    waiting_for_answer = State()
    waiting_for_choice = State()