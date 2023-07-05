import sqlalchemy
from sqlalchemy.orm import sessionmaker

# from DataBase import create_tables, Users, ViewedUser
from DataBase import create_tables, Users
from VKinder import VKinder_3, id


DSN = "postgresql://postgres:13245342@localhost:5432/VKinder"

engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()
session.commit()

vkinder = VKinder_3()
vk_id_value = vkinder.pull_name(id)
VK_user = Users(vk_id=vk_id_value)  # создаём пользователя который написал боту (id автоматом пропишется)

session.add(VK_user)  # создаём в бд
session.commit()
vk_viewed_id_value = vkinder.search_user(id)

VK_id_viewed1 = Users(vk_id=vk_viewed_id_value)
VK_user.vk_viewed_id = vk_viewed_id_value
session.commit()  # отправляем коммит что бы создалось


session.close()
