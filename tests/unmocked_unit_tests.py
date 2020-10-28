'''
    unomocked_unit_tests.py
    
    This file tests all unmocked methods used in bot.py and validate.py
'''

import unittest
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import bot, validate

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_IS_BOT = "is bot"
KEY_BOT_REPLY = " bot reply"
KEY_IS_LINK = "is link"
KEY_IS_IMAGE = "is image"
KEY_RENDERED_RESPONSE = "after render"

TEST_LINK1 = "https://i2.wp.com/ceklog.kindel.com/wp-content/uploads/2013/02/firefox_2018-07-10_07-50-11.png"
TEST_LINK2 = "https://canvas.njit.edu/"

class BotTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: "!! help",
                KEY_EXPECTED: {
                    KEY_IS_BOT: True,
                    KEY_BOT_REPLY: bot.BOT_HELP_REPLY,
                    KEY_IS_LINK: False,
                    KEY_IS_IMAGE: False,
                    KEY_RENDERED_RESPONSE: "!! help"
                }
            },
            {
                KEY_INPUT: "!about me",
                KEY_EXPECTED: {
                    KEY_IS_BOT: False,
                    KEY_BOT_REPLY: None,
                    KEY_IS_LINK: False,
                    KEY_IS_IMAGE: False,
                    KEY_RENDERED_RESPONSE: "!about me"
                }
            },
            {
                KEY_INPUT: "!! dfkj",
                KEY_EXPECTED: {
                    KEY_IS_BOT: True,
                    KEY_BOT_REPLY: bot.BOT_INVALID_COMMAND_REPLY.format("!! dfkj"),
                    KEY_IS_LINK: False,
                    KEY_IS_IMAGE: False,
                    KEY_RENDERED_RESPONSE: "!! dfkj"

                }
            },
            {
                KEY_INPUT: TEST_LINK1,
                KEY_EXPECTED: {
                    KEY_IS_BOT: False,
                    KEY_BOT_REPLY: None,
                    KEY_IS_LINK: True,
                    KEY_IS_IMAGE: True,
                    KEY_RENDERED_RESPONSE: bot.RENDERED_LINK_TEMPLATE.format(TEST_LINK1, TEST_LINK1)+\
                    bot.RENDERED_IMAGE_TEMPLATE.format(TEST_LINK1, TEST_LINK1)
                }
            },
            {
                KEY_INPUT: TEST_LINK2,
                KEY_EXPECTED: {
                    KEY_IS_BOT: False,
                    KEY_BOT_REPLY: None,
                    KEY_IS_LINK: True,
                    KEY_IS_IMAGE: False,
                    KEY_RENDERED_RESPONSE: bot.RENDERED_LINK_TEMPLATE.format(TEST_LINK2, TEST_LINK2)
                }
            }
        ]
        
        self.failure_test_params = [
            {
                KEY_INPUT: "!! help",
                KEY_EXPECTED: {
                    KEY_IS_BOT: False,
                    KEY_BOT_REPLY: bot.BOT_INVALID_COMMAND_REPLY.format("!! help"),
                    KEY_IS_LINK: True,
                    KEY_IS_IMAGE: True,
                    KEY_RENDERED_RESPONSE: bot.RENDERED_LINK_TEMPLATE.format("!! help", "!! help")
                }
            },
            {
                KEY_INPUT: "!about me",
                KEY_EXPECTED: {
                    KEY_IS_BOT: True,
                    KEY_BOT_REPLY: bot.BOT_INVALID_COMMAND_REPLY.format("!about me"),
                    KEY_IS_LINK: True,
                    KEY_IS_IMAGE: True,
                    KEY_RENDERED_RESPONSE: bot.RENDERED_LINK_TEMPLATE.format("!about me", "!about me")
                }
            },
            {
                KEY_INPUT: "!! dfkj",
                KEY_EXPECTED: {
                    KEY_IS_BOT: False,
                    KEY_BOT_REPLY: None,
                    KEY_IS_LINK: True,
                    KEY_IS_IMAGE: True,
                    KEY_RENDERED_RESPONSE: bot.RENDERED_LINK_TEMPLATE.format("!! dfkj", "!! dfkj")
                }
            },
            {
                KEY_INPUT: TEST_LINK1,
                KEY_EXPECTED: {
                    KEY_IS_BOT: True,
                    KEY_BOT_REPLY: bot.BOT_INVALID_COMMAND_REPLY.format(TEST_LINK1),
                    KEY_IS_LINK: False,
                    KEY_IS_IMAGE: False,
                    KEY_RENDERED_RESPONSE: TEST_LINK1
                }
            },
            {
                KEY_INPUT: TEST_LINK2,
                KEY_EXPECTED: {
                    KEY_IS_BOT: True,
                    KEY_BOT_REPLY: bot.BOT_INVALID_COMMAND_REPLY.format(TEST_LINK2),
                    KEY_IS_LINK: False,
                    KEY_IS_IMAGE: True,
                    KEY_RENDERED_RESPONSE: TEST_LINK2
                }
            }
        ]


    def test_is_bot_command_success(self):
        for test in self.success_test_params:
            response = bot.is_bot_command(test[KEY_INPUT])
            expected = test[KEY_EXPECTED][KEY_IS_BOT]
            
            self.assertEqual(response, expected)

    def test_is_bot_command_failure(self):
        for test in self.failure_test_params:
            response = bot.is_bot_command(test[KEY_INPUT])
            expected = test[KEY_EXPECTED][KEY_IS_BOT]
            
            self.assertNotEqual(response, expected)
    
    def test_bot_reply_success(self):
        for test in self.success_test_params:
            response = bot.bot_reply(test[KEY_INPUT]) if bot.is_bot_command(test[KEY_INPUT]) else None
            expected = test[KEY_EXPECTED][KEY_BOT_REPLY]
            
            self.assertEqual(response, expected)
    
    def test_bot_reply_failure(self):
        for test in self.failure_test_params:
            response = bot.bot_reply(test[KEY_INPUT]) if bot.is_bot_command(test[KEY_INPUT]) else None
            expected = test[KEY_EXPECTED][KEY_BOT_REPLY]
            
            self.assertNotEqual(response, expected)
    
    def test_is_link_success(self):
        for test in self.success_test_params:
            response = bot.is_link(test[KEY_INPUT])
            expected = test[KEY_EXPECTED][KEY_IS_LINK]
            
            self.assertEqual(response, expected)
    
    def test_is_link_failure(self):
        for test in self.failure_test_params:
            response = bot.is_link(test[KEY_INPUT])
            expected = test[KEY_EXPECTED][KEY_IS_LINK]
            
            self.assertNotEqual(response, expected)
    
    def test_is_image_success(self):
        for test in self.success_test_params:
            response = bot.is_image(test[KEY_INPUT])
            expected = test[KEY_EXPECTED][KEY_IS_IMAGE]
            
            self.assertEqual(response, expected)
    
    def test_is_image_failure(self):
        for test in self.failure_test_params:
            response = bot.is_image(test[KEY_INPUT])
            expected = test[KEY_EXPECTED][KEY_IS_IMAGE]
            
            self.assertNotEqual(response, expected)
    
    def test_render_success(self):
        for test in self.success_test_params:
            response = bot.render(test[KEY_INPUT])
            expected = test[KEY_EXPECTED][KEY_RENDERED_RESPONSE]
            
            self.assertEqual(response, expected)
    
    def test_render_failure(self):
        for test in self.failure_test_params:
            response = bot.render(test[KEY_INPUT])
            expected = test[KEY_EXPECTED][KEY_RENDERED_RESPONSE]
            
            self.assertNotEqual(response, expected)


    


if __name__ == '__main__':
    unittest.main()