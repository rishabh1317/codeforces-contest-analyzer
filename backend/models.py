from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class AnalysisCache(Base):
    __tablename__ = "analysis_cache"
    id = Column(Integer, primary_key=True, index=True)
    handle = Column(String, index=True)
    platform = Column(String, index=True)
    cached_json = Column(String)  # Store as JSON string
    last_updated = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    handle = Column(String, unique=True, index=True)
    platform = Column(String) # "codeforces" or "leetcode"
    rating = Column(Integer, nullable=True)
    max_rating = Column(Integer, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow)
    submissions = relationship("Submission", back_populates="user")

class Problem(Base):
    __tablename__ = "problems"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)
    problem_id = Column(String, unique=True, index=True) # e.g. "1900-A"
    name = Column(String)
    rating = Column(Integer, nullable=True)
    tags = Column(String) # comma separated tags
    submissions = relationship("Submission", back_populates="problem")

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    problem_id = Column(Integer, ForeignKey("problems.id"))
    verdict = Column(String)
    language = Column(String)
    creation_time = Column(Integer)
    user = relationship("User", back_populates="submissions")
    problem = relationship("Problem", back_populates="submissions")

class ContestCache(Base):
    __tablename__ = "contest_cache"
    contest_id = Column(Integer, primary_key=True, index=True)
    total_participants = Column(Integer)
