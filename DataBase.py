import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()       # наследование для классов. Регистрирует наследников и может создать соответствующие таблицы в БД

class Users(Base):
    __tablename__ = "users"        # название таблицы которая будет создана в postgres
            # ниже атрибуты нашей таблицы
    id = sq.Column(sq.Integer, primary_key = True)      # колонка id, типа ИНТеджер и ограничение ПРИМАРИ КЕЙ
    vk_id = sq.Column(sq.String(length = 48), unique = True)     # колонка vk_id, тип СТРока с длиной символов в 48 и требование уникальности.
    vk_viewed_id = sq.Column(sq.String(length = 30), unique = True)
    like = sq.Column(sq.Boolean())

    # users = relationship("ViewedUser", back_populates="viewed")       # связь между таблиц с помощью relationship

    def __str__(self):
        return f'Users {self.id}: ({self.vk_id}, {self.vk_viewed_id}, {self.like})'

# class ViewedUser(Base):
#     __tablename__ = "ViewedUsers"

#     id = sq.Column(sq.Integer, primary_key = True)
#     vk_id = sq.Column(sq.String(length = 30), unique = True)
#     like = sq.Column(sq.Boolean())
#     users_id = sq.Column(sq.Integer, sq.ForeignKey("users.id"), nullable = False)         # Внешний ключ. ФоренКей(таблица_на_которую_ссылаемся.название_столбика_на_который_ссылаемся)

#     viewed = relationship("Users", back_populates = "users")       # обратная связь через back_populates. "Course" - линк на класс.

#     def __str__(self):
#         return f'ViewedUser {self.id}: ({self.vk_id}, {self.like}, {self.users_id})'


def create_tables(engine):          # Функция для создания таблиц. принимает параметр engine - наш движок
    Base.metadata.drop_all(engine)          # удалить существующие таблицы из нашей БД!
    Base.metadata.create_all(engine)        # умный метод create_all создаст таблицы, если они уже есть, не будет ошибки.