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

def init_db():
    Base.metadata.create_all(engine)

init_db()