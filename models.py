import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker



Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    profile_id = sq.Column(sq.Integer, unique=True)

def create_tables(engine):
    Base.metadata.create_all(engine)


def save_user(vk_id, profile_id):
    try:
        new_user = User(vk_id=user_id, vk_profile=profile_id )
        session.add(new_user)
        session.commit()
        return True
    except (IntegrityError, InvalidRequestError):
        write_msg(event_id,
                  'Пользователь уже добавлен в базу.')
        return False

def check_profile_id(profile_id):
    try:
        current_user_id = session.query(User).filter_by(User.profile_id.IS_NULL).all()
        return True
    except (IntegrityError, InvalidRequestError):
        write_msg(event_id,
                  'Анкета уже добавлена в базу.')
        return False

    
