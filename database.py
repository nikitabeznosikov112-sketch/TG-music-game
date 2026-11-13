from sqlalchemy import create_engine, Column, String, Integer, BigInteger, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, unique=True, nullable=False)
    name = Column(String, nullable=False)
    score = Column(Integer, default=0)
    subscription = Column(Boolean, nullable=False, default=False)
