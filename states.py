from aiogram.fsm.state import State, StatesGroup

class MusicGame(StatesGroup):
    waiting_for_answer = State()
    