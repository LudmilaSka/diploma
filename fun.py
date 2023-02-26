import vk_api
from config import user_token, comm_token, offset, line
import datetime
from random import randrange
from vk_api.longpoll import VkLongPoll, VkEventType


class Bot:
    def __init__(self):
        print('Bot was created')
        self.session = vk_api.VkApi(token=user_token)
        self.vk = self.session.get_api()
        self.session_group = vk_api.VkApi(token=comm_token) 
        


    def write_msg(self, user_id, message):
        msg = self.session.method("messages.send",{"user_id" : user_id, 'message': message,'random_id': randrange(10 ** 7) })

    def user_info(self, user_id):
        resp = self.session.method("users.get",{"user_id" : user_id, "fields" : "sex , city , bdate"})


        for i in resp:
            first_name = i.get('first_name')
        for s in resp:
            try:
                sex = s.get('sex')
                if sex == 2:
                    find_sex = 1
                elif sex == 1:
                    find_sex = 2
            except TypeError:
                self.write_msg(user_id, 'Профиль не заполнен ')
        for c in resp:
            try:
                city = c.get('city')
                title_city = city['title']
            except TypeError:
                self.write_msg(user_id, 'Профиль не заполнен ')

        for bd in resp:
            try:
                bdate = bd.get('bdate')
            except TypeError:
                self.write_msg(user_id, 'Профиль не заполнен ')
            date_list = bdate.split('.')
            year = int(date_list[2])
            year_now = int(datetime.date.today().year)
            age_from = ((year_now - year) - 5)
            age_to = ((year_now - year) + 5)
        dict_info = {'sex' : find_sex , 'city' : title_city, 'age_from' : age_from , 'age_to' : age_to}

        return dict_info


    def userseach(self, user_id):
        dict_info = self.user_info(user_id)
        response = self.session.method("users.search", {'sort': 1,
                                                   'sex': dict_info['sex'],
                                                   'status': 1,
                                                   'age_from': dict_info['age_from'],
                                                   'age_to': dict_info['age_to'],
                                                   'has_photo': 1,
                                                   'count': 1,
                                                   'fields': 'is_closed',
                                                   'hometown': dict_info['city']
                                                   })



        for element in response['items']:
            if not element["is_closed"]:
                profile_id = element.get('id')
                return profile_id

    def get_photo(self, user_id):
        owner_id = self.userseach(user_id)

        response = self.session.method('photos.get',
                              {
                                  'access_token': user_token,
                                  'owner_id': owner_id,
                                  'album_id': 'profile',
                                  'extended': 1,
                                  'photo_sizes': 1,
                              })

        dict_photos = dict()
        for i in response['items']:
            photo_id = str(i["id"])
            i_likes = i["likes"]
            if i_likes["count"]:
                likes = i_likes["count"]
                dict_photos[likes] = photo_id

        list_of_ids = sorted(dict_photos.items(), reverse=True)
        list_id_photo = []
        for i in  list_of_ids:
            list_id_photo.append(i[1])
        count = 0
        attachments = []

        for id_photo in list_id_photo:
            count += 1


            if  1 <= count <= 3:
                attachments.append('photo{}_{}'.format(user_id, id_photo))
                return (attachments)
            elif 1 <= count <= 2:
                attachments.append('photo{}_{}'.format(user_id, id_photo))
                return attachments
            elif count == 1:
                attachments.append('photo{}_{}'.format(user_id, id_photo))
                return attachments

    def send_photo(self, user_id, message, attachments):

        response = self.session.method("messages.send",
                                       {
                                        "user_id" : user_id,
                                        'message': message,
                                        'random_id': randrange(10 ** 7),
                                        'attachment': ",".join(attachments)
                                       })



    def show_found_person(self, user_id):
        try:
            self.send_photo(user_id, 'Три фото с максимальными лайками')
            vk_link = 'vk.com/id' + str(self.userseach(user_id))
        except TypeError:
             return f' Похоже просмотренны все профили из БД. \n' \
                    f' Наберите "Искать дальше" для поиска и добавления в БД.'


bot = Bot()



        





