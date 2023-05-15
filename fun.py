import vk_api
from config import user_token, offset, comm_token
import datetime
from vk_api.exceptions import ApiError
from vk_api.utils import get_random_id
from models import *


class VkTools:
    def __init__(self, user_token):
        self.session_user = vk_api.VkApi(token=user_token)
        self.vk_session = vk_api.VkApi(token=comm_token)

    def user_info(self, user_id):
        try:
            resp = self.session_user.method("users.get", {
                                            "user_id": user_id,
                                           "fields": "sex , city , bdate"})
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

    def userseach(self, user_id, offset):
        dict_info = self.user_info(user_id)
        try:
            profiles = self.session_user.method("users.search", {'sort': 1,
                                               'sex': dict_info['sex'],
                                               'status': 1,
                                               'age_from': dict_info['age_from'],
                                               'age_to': dict_info['age_to'],
                                               'has_photo': 1,
                                               'count': 10,
                                               'fields': 'is_closed',
                                               'hometown': dict_info['city'],
                                                'offset': offset
                                               })
        except ApiError:
            return
        profiles = profiles['items']
        result = []
        for profile in profiles:
            if profile['is_closed'] == False:
                result.append({'id': profile['id'] })
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

    def photos_get(self, profile_id):
        photos = self.session_user.method('photos.get', {'album_id': 'profile',
                                               'owner_id': profile_id,
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
        for i in list_of_ids:
            list_id_photo.append(i[1])
        count = 0
        attachments = []
        for id_photo in list_id_photo:
            count += 1
            if 1 <= count <= 3:
                attachments.append('photo{}_{},'.format(profile_id, id_photo))
            elif 1 <= count <= 2:
                attachments.append('photo{}_{},'.format(profile_id, id_photo))
            elif count == 1:
                attachments.append('photo{}_{}'.format(profile_id, id_photo))
        attachments = ''.join(attachments)
        return attachments


    def send_photo(self, user_id, message, attachments, profile_id):

        response = self.vk_session.method("messages.send", {
                                        'user_id': user_id,
                                        'message': message,
                                        'random_id': get_random_id(),
                                        'attachment': self.photos_get(profile_id)
                                       })






tools = VkTools(user_token)
