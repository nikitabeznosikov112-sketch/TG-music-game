from sqlalchemy import create_engine, Column, String, Integer, BigInteger
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite:///bot.db', echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, unique=True, nullable=False)
    name = Column(String, nullable=False)
    score = Column(Integer, default=0)

    def __repr__(self):
        return f'<User {self.name}: {self.score}>'

def init_db():
    Base.metadata.create_all(engine)

def get_user(tg_id):
    session = Session()
    try:
        user = session.query(User).filter_by(tg_id=tg_id).first()
        return user
    finally:
        session.close()

def create_user(tg_id, user_name):
    session = Session()

    try:
        user = User(tg_id=tg_id, name=user_name, score=0)
        session.add(user)
        session.commit()
        return user
    finally:
        session.close()

def add_score(tg_id, points):
    session = Session()

    try:
        user = session.query(User).filter_by(tg_id=tg_id).first()
        if user:
            user.score += points
            session.commit()
    finally:
        session.close()

def show_score(tg_id):
    session = Session()

    try:
        user = session.query(User).filter_by(tg_id=tg_id).first()
        if user:
            return user.score
        else:
            return 'Пользователь не найден'
    finally:
        session.close()

def get_ratings(limit=10):
    session = Session()

    try:
        top_users = session.query(User).order_by(User.score.desc()).limit(limit).all()
        return top_users
    finally:
        session.close()
init_db()