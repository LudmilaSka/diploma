import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from bdorm import Session



Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    profile_id = sq.Column(sq.Integer, unique=True)

def create_tables(engine):
    Base.metadata.create_all(engine)


def save_user(vk_id, profile_id):
    new_user = User(vk_id=user_id, vk_profile=profile_id )
    session.add(new_user)
    session.commit()

def check_profile_id(profile_id):
    current_user_id = session.query(User).filter_by(User.profile_id.IS_NULL).all()
    return current_user_id


    
