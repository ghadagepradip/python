from sqlalchemy import TIMESTAMP, Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import Relationship
from database import Base



class post(Base):
    __tablename__ = 'post'

    id = Column(Integer,primary_key=True,nullable=False)
    title =Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,nullable=False,server_default='FALSE')
    created_at = Column(TIMESTAMP(timezone=True),nullable=True,server_default='now()')
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="cascade"),nullable=False)
    owner =Relationship('users')


class users(Base):
    __tablename__ = 'users'

    id = Column(Integer,nullable=False,primary_key=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=True,server_default='now()')


class votes(Base):
    __tablename__ = 'votes'

    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer,ForeignKey("post.id",ondelete="CASCADE"),primary_key=True)



