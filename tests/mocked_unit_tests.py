'''
    unomocked_unit_tests.py
    
    This file tests all unmocked methods used in bot.py and validate.py
'''

import unittest
import unittest.mock as mock

import requests, json, os, dotenv, validators
from datetime import date, datetime

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import bot


KEY_INPUT = "input"
KEY_EXPECTED = "expected"

class MockedFuntranslateRequestResponse:
    def __init__(self, url):
        self.url = url
    def json(self):
        return {"success": {"total": 1},
        "contents": {
        "translated": "What art thee doing?",
        "text": "what are you doing?",
        "translation": "shakespeare"
        }
        }

class FuntranslateQueryTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: "!! funtranslate what are you doing?",
                KEY_EXPECTED: "What art thee doing?"
            },
        ]
    
    def mocked_api_search_json(self, url):
        return MockedFuntranslateRequestResponse(url)

    def test_funtranslate_command(self):
        for test_case in self.success_test_params:
            with mock.patch('requests.get', self.mocked_api_search_json):
                translated_message = bot.funtranslate_command(test_case[KEY_INPUT])
                
            expected = test_case[KEY_EXPECTED]
            print("expected is {}".format(expected))
            print("translated message is {}".format(translated_message))
            self.assertEqual(translated_message, expected)


if __name__ == '__main__':
    unittest.main()