import config
from config import comm_token, user_token, offset, line
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from fun import tools
from models import *


class Bot:
    def __init__(self, token=comm_token):
        self.vk_session = vk_api.VkApi(token=comm_token)
        self.session_api = self.vk_session.get_api()
        self.offset = offset

    def write_msg(self, user_id, text):
        self.vk_session.method('messages.send',
                               {'user_id': user_id,
                                'message': text,
                                'random_id': get_random_id()})

    def header(self):
        longpoll = VkLongPoll(self.vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text.lower() == 'привет':
                    self.write_msg(event.user_id, 'и тебе привет')
                elif event.text.lower() == 'поиск':
                    name_profile = tools.userseach(user_id=event.user_id, offset=self.offset)
                    profile_id = name_profile.pop()['id']
                    if profile_id in tools.check_in_bd(profile_id=profile_id):
                        self.offset += 11
                        self.write_msg(user_id=event.user_id, text=tools.get_profile(profile_id=profile_id))
                        tools.send_photo(user_id=event.user_id, message='фото',
                                                 attachments=tools.photos_get(profile_id), profile_id=profile_id)
                        save_user(profile_id=profile_id, worksheet_id=event.user_id)

                    else:
                        tools.user_info(user_id=event.user_id)
                        name_profile = tools.userseach(user_id=event.user_id, offset=self.offset)
                        profile_id = name_profile.pop()['id']
                        tools.get_profile(profile_id=profile_id)
                        save_user(profile_id=profile_id, worksheet_id=event.user_id)
                        self.write_msg(user_id=event.user_id, text=tools.get_profile(profile_id=profile_id))
                        tools.send_photo(user_id=event.user_id, message='фото',
                                             attachments=tools.photos_get(profile_id), profile_id=profile_id)
                elif event.text.lower() == 'далее':
                    if len(tools.userseach(user_id=event.user_id, offset=self.offset)) == 0:
                        self.offset += 11
                        name_profile = tools.userseach(user_id=event.user_id, offset=self.offset)
                        profile_id = name_profile['id']
                        if profile_id in tools.check_in_bd(profile_id=profile_id):
                            self.offset += 11
                            self.write_msg(user_id=event.user_id, text=tools.get_profile(profile_id=profile_id))
                            tools.send_photo(user_id=event.user_id, message='фото',
                                             attachments=tools.photos_get(profile_id), profile_id=profile_id)
                            save_user(profile_id=profile_id, worksheet_id=event.user_id)
                        else:
                            self.write_msg(user_id=event.user_id, text=tools.get_profile(profile_id=profile_id))
                            tools.send_photo(user_id=event.user_id, message='фото',
                                             attachments=tools.photos_get(profile_id), profile_id=profile_id)
                            save_user(profile_id=profile_id, worksheet_id=event.user_id)
                    else:
                        name_profile = tools.userseach(user_id=event.user_id, offset=self.offset)
                        profile_id = name_profile.pop()['id']
                        tools.get_profile(profile_id=profile_id)
                        if profile_id in tools.check_in_bd(profile_id=profile_id):
                            self.offset += 11
                            self.write_msg(user_id=event.user_id, text=tools.get_profile(profile_id=profile_id))
                            tools.send_photo(user_id=event.user_id, message='фото',
                                             attachments=tools.photos_get(profile_id), profile_id=profile_id)
                            save_user(profile_id=profile_id, worksheet_id=event.user_id)
                        else:
                            self.write_msg(user_id=event.user_id, text=tools.get_profile(profile_id=profile_id))
                            tools.send_photo(user_id=event.user_id, message='фото',
                                             attachments=tools.photos_get(profile_id), profile_id=profile_id)
                            save_user(profile_id=profile_id, worksheet_id=event.user_id)

                else:
                    self.write_msg(event.user_id, 'неизвестная команда')

if __name__ == '__main__':
    bot = Bot(comm_token)
    bot.header()





