from config import comm_token, user_token, offset
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from fun import tools
from models import *


class Bot:
    def __init__(self, token=comm_token):
        self.vk_session = vk_api.VkApi(token=comm_token)
        self.session_api = self.vk_session.get_api()


    def write_msg(self, user_id, text, attachments=None):
        self.vk_session.method('messages.send',
                               {'user_id': user_id,
                                'message': text,
                                'random_id': get_random_id(),
                                'attachments': attachments

                                })

if __name__ == '__main__':
    bot = Bot(comm_token)


    longpoll = VkLongPoll(bot.vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text.lower() == 'привет':
                    bot.write_msg(event.user_id, 'и тебе привет')
                elif event.text.lower() == 'поиск':
                    tools.user_info(user_id=event.user_id)
                    name_profile = tools.userseach(user_id=event.user_id)
                    for pr_id in name_profile:
                        profile_id = pr_id['id']
                    tools.get_profile( profile_id=profile_id)
                    bot.write_msg(user_id=event.user_id, text=tools.get_profile( profile_id=profile_id), attachments=tools.photos_get(user_id=event.user_id))
                    bot.write_msg(user_id=event.user_id, text=' фото', attachments=tools.photos_get(user_id=event.user_id))

                elif event.text.lower() == 'далее':
                    name_profile = tools.userseach(user_id=event.user_id)
                    for pr_id in name_profile:
                        profile_id = pr_id['id']
                        for i in range(0, 100):
                            offset += 1
                            tools.userseach(user_id=event.user_id)
                            break
                        save_user(profile_id=profile_id, worksheet_id=event.user_id)
                        bot.write_msg(user_id=event.user_id, text=tools.get_profile( profile_id=profile_id))
                        bot.write_msg(user_id=event.user_id,
                                      text=tools.get_profile(profile_id=profile_id),
                                      attachments=tools.photos_get(user_id=event.user_id))
                        bot.write_msg(user_id=event.user_id, text=' фото',
                                      attachments=tools.photos_get(user_id=event.user_id))
                else:
                    bot.write_msg(event.user_id, 'неизвестная команда')







