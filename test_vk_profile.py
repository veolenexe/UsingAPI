import unittest
from vk_profile import VkApi


class TestVkApi(unittest.TestCase):

    def test_try_get_city_correct(self):
        correct = {'city': {'title': 'DA'}}
        assert VkApi.try_get_city(correct) == 'DA'

    def test_try_get_city_wrong1(self):
        correct = {'town': {'tilte': 'DA'}}
        assert VkApi.try_get_city(correct) is None

    def test_try_get_city_Wrong2(self):
        correct = {'city': {'asd': "asd"}}
        assert VkApi.try_get_city(correct) is None

    def test_albumList_correct(self):
        correct = [{'title': 'asd', 'size': 123, 'description': 'asdastfwr'},
                   {'title': 'awesd', 'size': 123, 'description': 'asdastfwr'},
                   {'title': 'asdsd', 'size': 123, 'description': 'asdastfwr'}]
        assert VkApi.get_album_info(correct)

    def test_albumList_empty(self):
        wrong = None
        assert not VkApi.get_album_info(wrong)

    def test_get_user_subscriptions_info_correct(self):
        correct = [{'id': '1', 'name': "12332", 'type': 'post'},
                   {'id': '2', 'name': "12233", 'type': 'post'},
                   {'id': '3', 'name': "11123", 'type': 'post'}]
        assert VkApi.get_user_subscriptions_info(correct)
