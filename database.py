from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Use PostgreSQL on Railway (DATABASE_URL set automatically), SQLite locally
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./english_learning.db")

# Railway provides postgres:// but SQLAlchemy needs postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    level = Column(String, default="intermediate")  # beginner / intermediate / advanced
    created_at = Column(DateTime, default=datetime.utcnow)
    progress = relationship("UserProgress", back_populates="user")
    quiz_attempts = relationship("QuizAttempt", back_populates="user")


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    level = Column(String, default="intermediate")  # beginner / intermediate / advanced
    reading_text = Column(Text, nullable=False)
    is_published = Column(Boolean, default=False)
    week_number = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    words = relationship("Word", back_populates="lesson", cascade="all, delete-orphan")
    progress = relationship("UserProgress", back_populates="lesson")
    quiz_attempts = relationship("QuizAttempt", back_populates="lesson")


class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    english = Column(String, nullable=False)
    hebrew = Column(String, nullable=False)
    example_sentence = Column(Text)
    phonetic = Column(String)
    word_type = Column(String)  # noun, verb, adjective, etc.
    lesson = relationship("Lesson", back_populates="words")


class UserProgress(Base):
    __tablename__ = "user_progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    reading_done = Column(Boolean, default=False)
    words_studied = Column(Boolean, default=False)
    quiz_stage1_done = Column(Boolean, default=False)
    quiz_stage2_done = Column(Boolean, default=False)
    stage1_score = Column(Float, default=0.0)
    stage2_score = Column(Float, default=0.0)
    completed_at = Column(DateTime, nullable=True)
    user = relationship("User", back_populates="progress")
    lesson = relationship("Lesson", back_populates="progress")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    stage = Column(Integer, nullable=False)  # 1 or 2
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    user_answer = Column(Text)
    is_correct = Column(Boolean, default=False)
    attempted_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="quiz_attempts")
    lesson = relationship("Lesson", back_populates="quiz_attempts")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
