import sqlalchemy as sq
import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DSN, engine



engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
class User(Base):
    __tablename__ = 'user'

    id = sq.Column (sq.Integer, primary_key=True)
    profile_id = sq.Column(sq.Integer )
    worksheet_id = sq.Column(sq.Integer)

    def __str__(self):
        return f'User  {self.profile_id}, {self.worksheet_id}'

def save_user(profile_id, worksheet_id):
    to_bd = User(profile_id=profile_id, worksheet_id=worksheet_id)
    session.add(to_bd)
    session.commit()

def check_profile_id(profile_id):
    from_bd = session.query(User).filter(User.profile_id == profile_id).all()
    return from_bd

if __name__ == '__main__':
    Base.metadata.create_all(engine)






