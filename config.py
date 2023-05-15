import sqlalchemy


user_token = '' # токен пользователя
comm_token = '' # токен сообщества

offset = 1
line = range(0, 1000)

DSN = "postgresql://postgres:12345678@localhost:5432/bd_vkinder1"
engine = sqlalchemy.create_engine(DSN)