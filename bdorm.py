import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import User



DSN = "postgresql://postgres:12345678@localhost:5432/bd_vkinder"
engine = sqlalchemy.create_engine(DSN)

if __name__ == '__main__':
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()





session.close()
