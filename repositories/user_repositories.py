from sqlalchemy.orm import Session
from database import User, Session as DbSession

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, tg_id: int):
        '''Вернуть пользователя по айди'''
        return self.session.query(User).filter_by(tg_id=tg_id).first()

    def create(self, tg_id: int, name: str):
        '''Создает пользователя'''
        new_user = User(tg_id=tg_id, name=name, score=0)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def add_points(self, tg_id: int, score: int):
        '''Добавляет очки пользователю'''
        user = self.get_by_id(tg_id)
        if user:
            user.score += score
            self.session.commit()

    def show_score(self, tg_id: int):
        '''Показывает счет пользователя'''
        user = self.session.query(User).filter_by(tg_id=tg_id).first()
        if user:
            return user.score

    def get_top(self, limit: int = 10):
        '''Выдает рейтинг'''
        return self.session.query(User).order_by(User.score.desc()).limit(limit).all()

    def get_status(self, tg_id: int):
        user = self.session.query(User).filter_by(tg_id=tg_id).first()
        if user:
            return user.subscription