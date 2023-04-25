import vk_api
from config import user_token, offset
import datetime
from vk_api.exceptions import ApiError
from vk_api.utils import get_random_id
from models import *


class VkTools:
    def __init__(self, user_token):
        self.session_user = vk_api.VkApi(token=user_token)

    def user_info(self, user_id):
        try:
            resp = self.session_user.method("users.get", {"user_id": user_id, "fields": "sex , city , bdate"})
        except ApiError:
            return

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
        dict_info = {'sex': find_sex, 'city': title_city, 'age_from': age_from, 'age_to': age_to}
        return dict_info

    def userseach(self, user_id):
        dict_info = self.user_info(user_id)
        try:

            profiles = self.session_user.method("users.search", {'sort': 1,
                                               'sex': dict_info['sex'],
                                               'status': 1,
                                               'age_from': dict_info['age_from'],
                                               'age_to': dict_info['age_to'],
                                               'has_photo': 1,
                                               'count': 100,
                                               'fields': 'is_closed',
                                               'hometown': dict_info['city'],
                                                'offset': 1
                                               })
        except ApiError:
            return
        profiles = profiles['items']
        result = []
        for profile in profiles:
            if profile['is_closed'] == False:
                result.append({'id': profile['id'] })
                save_user(profile_id=profile['id'], worksheet_id=user_id)
        # print(result)
        return result

    def get_profile(self, profile_id):

        get_pr = self.session_user.method('users.get', {'user_ids': profile_id})
        for f in get_pr:
            first_name = f.get('first_name')
        for l in get_pr:
            last_name = l.get('last_name')
        for i in get_pr:
            id = i.get('id')
            vk_link = 'vk.com/id' + str(id)
        return ( f'{first_name + " " + last_name + " " + vk_link }' )


    def photos_get(self, user_id):
        photos = self.session_user.method('photos.get', {'album_id': 'profile',
                                               'owner_id': user_id,
                                                'extended': 1})
        try:
            photos_info = photos['items']

        except KeyError:
            return
        dict_photos = dict()
        for i in photos['items']:
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


    def send_photo(self, user_id, message, attachments=None):

        response = self.session_user.method("messages.send",
                                       {
                                        "user_id" : user_id,
                                        'message': message,
                                        'random_id': get_random_id(),
                                        'attachment': self.photos_get(user_id)
                                       })





tools = VkTools(user_token)
# tools.check_profile(68343, 784208873, offset)
#tools.userseach(68343)

# tools.photos_get(68343)


    # print(tools.userseach(68343))
    # info = tools.user_info(user_id='user_id')
    # if info:
    #     print(tools.user_info(68343))
    # else:
    #     pass #Сообщаем об ошибке заполните профиль
    # profiles = tools.userseach(68343)
    # print(profiles)
# photos = tools.photos_get(68343)
tools.get_profile(784453676)
tools.show_found_person(784453676)
# tools.person_id(offset)