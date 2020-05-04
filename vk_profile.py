import requests
import json
import sys

with open('ACCESS_TOKEN.txt', 'r') as file:
    ACCESS_TOKEN = file.read()


def help():
    print('ввод:\npy vk_profile.py [ID пользователя] (парамметры)')
    print('параметры:\n-subscriptions публичные страницы пользователся\n-friends друзья\n-albums альбомы')
    print('Пример ввода:\npy vk_profile.py 0 -friends')

class VkApi:
    ALL_API_METHODS = ['-subscriptions', '-friends', '-albums']

    def __init__(self, username=0):
        r = requests.post(
            f'https://api.vk.com/method/users.get?user_ids={username}&fields=city,domain&access_token={ACCESS_TOKEN}&v=5.103')
        if r.status_code == 200:
            self.user_baseinfo = json.loads(r.content)['response'][0]
            self.user_id = self.user_baseinfo['id']
        else:
            print('не удалось получить страницу пользователя')

    def get_userinfo(self, parameters=[]):
        if '-all' in parameters:
            parameters = VkApi.ALL_API_METHODS
        self.get_user_base_info()
        if '-subscriptions' in parameters:
            VkApi.get_user_subscriptions_info(
            self.get_request('users.getSubscriptions', 'user_id',
                             'extended=1')['items']),
        if '-friends' in parameters:
            VkApi.get_friends_info(
                self.get_request('friends.get', 'user_id',
                                 'fields=city,domain')[
                    'items']),
        if '-albums' in parameters:
            VkApi.get_album_info(
                self.get_request('photos.getAlbums', 'owner_id')['items'])


    def get_request(self, method, id_field_name, parameters=''):
        r = requests.post(
            f'https://api.vk.com/method/{method}?{id_field_name}={self.user_id}&{parameters}&access_token={ACCESS_TOKEN}&v=5.103')
        if r.status_code == 200:
            return json.loads(r.content)['response']
        return None

    def get_user_base_info(self):
        print('%12s%20d' % ('id:', self.user_id))
        print('%12s%20s' % ('first name:', self.user_baseinfo.get('first_name')))
        print('%12s%20s' % ('last name:', self.user_baseinfo.get('last_name')))
        print('%12s%20s' % ('city:', VkApi.try_get_city(self.user_baseinfo)))

    @staticmethod
    def get_user_subscriptions_info(subscriptions_list):
        print('subscriptions list:\n%10s%40s%20s' % ('id', 'name', 'type'))
        if subscriptions_list:
            for subscriptions in subscriptions_list:
                id = subscriptions.get("id")
                name = subscriptions.get("name")
                type = subscriptions.get("type")
                print(
                    '%10s%40s%20s' % (id, name, type))
            return True
        else:
            print('не удалось получить список публичных страниц')
            return False

    @staticmethod
    def get_friends_info(friend_list):
        print('friendList:\n%10s%20s%20s%20s' % (
            'id', 'first name', 'last name', 'city'))
        if friend_list:
            for friend in friend_list:
                friend_id = friend.get("id")
                first_name = friend.get("first_name")
                last_name = friend.get("last_name")
                city = VkApi.try_get_city(friend)
                print(
                    '%10s%20s%20s%20s' % (
                    friend_id, first_name, last_name, city))
        else:
            print('не удалось получить список друзей')

    @staticmethod
    def try_get_city(container: dict):
        city_info = container.get("city")
        if city_info:
            return city_info.get('title')
        return city_info

    @staticmethod
    def get_album_info(album_list):
        print('Album list:\n%10s%10s%50s' % (
            'name', 'size', 'description'))
        if album_list:
            for album in album_list:
                title = album.get("title")
                size = album.get("size")
                description = album.get("description")
                formatted_description = ''
                if description:
                    for i in range(len(description)):
                        if i % 50 != 0 or i == 0:
                            formatted_description += description[i]
                        else:
                            formatted_description += f'{description[i]}\n\t\t\t\t\t\t'
                print('%10s%10d%50s' % (title, size, formatted_description))
                return True
        else:
            print('не удалось получить список альбомов')
            return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        help()
    username = sys.argv[1]
    if username in ['-help', '-h']:
        help()
    else:
        vk_api = VkApi(username)
        if len(sys.argv) > 2:
            vk_api.get_userinfo(sys.argv)
        else:
            vk_api.get_userinfo()
