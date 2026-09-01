from sqlalchemy import Column, Integer, String, Text

from .database import Base


class Post(Base):

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)