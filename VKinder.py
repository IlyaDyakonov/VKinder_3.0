from TOKEN import TOKEN_VK, TOKEN_app, TOKEN_my
import requests
import vk_api
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType
import time
import datetime


class VKinder_3:
    def __init__(self):
        print("Bot was created")
        self.vk = vk_api.VkApi(token=TOKEN_VK)  # АВТОРИЗАЦИЯ СООБЩЕСТВА
        self.longpoll = VkLongPoll(self.vk)  # РАБОТА С СООБЩЕНИЯМИ

    def pull_name(self, user_id):
        """Получение имени и фамилии пользователя, который написал боту."""
        url = f"https://api.vk.com/method/users.get"
        param = {
            "user_ids": user_id,
            "access_token": TOKEN_VK,
            "v": "5.131",
        }
        res = requests.get(url, params=param)
        response = res.json()
        information_dict = response["response"]
        for i in information_dict:
            first_name = i.get("first_name")
            last_name = i.get("last_name")
            return first_name, last_name

    def pull_user_age(self, user_id):
        """Парсим возраст пользователя, и выдаём ему в поиске его же возраст.
        Если год рождения скрыт - то будем спрашивать какой возраст для поиска ему нужен.
        """
        url = f"https://api.vk.com/method/users.get"
        param = {
            "user_ids": user_id,
            "access_token": TOKEN_VK,
            "v": "5.131",
            "fields": "bdate",
        }
        res = requests.get(url, params=param)
        response = res.json()
        information_dict = response["response"]
        for i in information_dict:
            date = i.get("bdate")
        date_list = date.split(".")
        if len(date_list) == 3:
            year = int(date_list[2])
            year_now = int(datetime.date.today().year)
            age = year_now - year
            return age
        elif len(date_list) == 2 or date not in information_dict:
            age_min = input("Введите возраст для поиска: ")
            return age_min

    def pull_user_city(self, user_id):
        """Парсим пользователя, вытаскиваем его город, в этом городе и выдадим ему найденых людей."""
        url = f"https://api.vk.com/method/users.get"
        param = {
            "user_ids": user_id,
            "access_token": TOKEN_VK,
            "v": "5.131",
            "fields": "city",
        }
        res = requests.get(url, params=param)
        response = res.json()
        information_dict = response["response"]
        for i in information_dict:
            city = i.get("city")
            city_title = city.get("title")
            city_id = city.get("id")
            return city_id

    def pull_user_gender(self, user_id):
        """Достаём пол пользователя и меняем на противоположный."""
        url = f"https://api.vk.com/method/users.get"
        param = {
            "user_ids": user_id,
            "access_token": TOKEN_VK,
            "fields": "sex",
            "v": "5.131",
        }
        res = requests.get(url, params=param)
        response = res.json()
        information_dick = response["response"]
        for i in information_dick:
            if i.get("sex") == 2:
                sex = 1
                return sex
            elif i.get("sex") == 1:
                sex = 2
                return sex

    def search_user(self, user_id):
        """По данным которым получили выше, ищем пользователей.
        Если страница у найденного пользователя открыта, выбираем данные, если закрыта - идём дальше."""
        url = f"https://api.vk.com/method/users.search"
        param = {
            "access_token": TOKEN_my,
            "v": "5.131",
            "age_from": self.pull_user_age(user_id),
            "city_id": self.pull_user_city(user_id),
            "sex": self.pull_user_gender(user_id),
            "fields": "is_closed, id, first_name, last_name",
            "status": "1" or "6",
            "count": 500,
        }
        res = requests.get(url, params=param)
        response = res.json()
        information_dick = response["response"]["items"]
        for person in information_dick:
            if person.get("is_closed") == False:
                first_name = person.get("first_name")
                last_name = person.get("last_name")
                vk_id_viewed = person.get("id")
                vk_link = "vk.com/id" + str(person.get("id"))
                print(f"Found user: {first_name} {last_name} ({vk_link})")
                return vk_id_viewed
            else:
                continue

    def get_photos_id(self, user_id):
        """Достаём фотки пользователя."""
        url = f'https://api.vk.com/method/photos.getAll'
        param = {
            "access_token": TOKEN_my,
            "owner_id": user_id,
            "extended": 1,
            "count": 50,
            'v': '5.131'
        }
        res = requests.get(url, params=param)
        response = res.json()
        photos_dict = dict()
        dict_1 = response["response"]["items"]
        for i in dict_1:
            photo_id = i.get("id")
            photo_like = i.get("likes")
            if photo_like.get("count"):
                like = photo_like.get("count")
                photos_dict[like] = photo_id
            list_of_ids = sorted(photos_dict.items(), reverse=True)
            return list_of_ids

    # def get_photo_1(self, user_id):
    #     """Достаём фото 1"""
    #     # photo_1, photo_2, photo_3 = self.get_photos_id(user_id)[:3]
    #     photo_list = self.get_photos_id(user_id)
    #     count = 0
    #     for i in photo_list:
    #         count += 1
    #         if count == 1:
    #             return i[1]

    # def get_photo_2(self, user_id):
    #     """Достаём фото 2"""
    #     photo_list = self.get_photos_id(user_id)
    #     count = 0
    #     for i in photo_list:
    #         count += 1
    #         if count == 2:
    #             return i[1]

    # def get_photo_3(self, user_id):
    #     """Достаём фото 3"""
    #     photo_list = self.get_photos_id(user_id)
    #     count = 0
    #     for i in photo_list:
    #         count += 1
    #         if count == 3:
    #             return i[1]

    def get_top_3_photos(self, user_id):
        """Достаём 3 фотографии с максимальными лайками"""
        photo_list = self.get_photos_id(user_id)
        sorted_photos = sorted(photo_list, key=lambda x: x[1], reverse=True)
        top_3_photos = [photo[0] for photo in sorted_photos[:3]]
        return top_3_photos

id = 5222465
# id = 231313454
# id = 39677170

VK = VKinder_3()
result_name = VK.pull_name(id)
result_find_age = VK.pull_user_age(id)
result_find_city = VK.pull_user_city(id)
result_find_gender = VK.pull_user_gender(id)
result_search_user = VK.search_user(id)
result_photos_id = VK.get_photos_id(id)
# result_photo_1 = VK.get_photo_1(id)
# result_photo_2 = VK.get_photo_2(id)
# result_photo_3 = VK.get_photo_3(id)
result_get_top_3_photos = VK.get_top_3_photos(id)
print(
    result_name,
    result_find_age,
    result_find_city,
    result_find_gender,
    result_search_user,
    result_photos_id,
    # result_photo_1,
    # result_photo_2,
    # result_photo_3
    result_get_top_3_photos
)