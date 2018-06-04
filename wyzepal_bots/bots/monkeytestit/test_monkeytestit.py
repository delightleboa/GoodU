from unittest import mock

import wyzepal_bots.bots.monkeytestit.monkeytestit
from wyzepal_bots.test_lib import BotTestCase


class TestMonkeyTestitBot(BotTestCase):
    bot_name = "monkeytestit"

    def test_bot_responds_to_empty_message(self):
        message = dict(
            content='',
            type='stream',
        )
        with mock.patch.object(
                wyzepal_bots.bots.monkeytestit.monkeytestit.MonkeyTestitBot,
                'initialize', return_value=None):
            with self.mock_config_info({'api_key': "magic"}):
                res = self.get_response(message)
                self.assertTrue("Unknown command" in res['content'])

    def test_website_fail(self):
        message = dict(
            content='check https://website.com',
            type='stream',
        )
        with mock.patch.object(
                wyzepal_bots.bots.monkeytestit.monkeytestit.MonkeyTestitBot,
                'initialize', return_value=None):
            with self.mock_config_info({'api_key': "magic"}):
                with self.mock_http_conversation('website_result_fail'):
                    res = self.get_response(message)
                    self.assertTrue("Status: tests_failed" in res['content'])

    def test_website_success(self):
        message = dict(
            content='check https://website.com',
            type='stream',
        )
        with mock.patch.object(
                wyzepal_bots.bots.monkeytestit.monkeytestit.MonkeyTestitBot,
                'initialize', return_value=None):
            with self.mock_config_info({'api_key': "magic"}):
                with self.mock_http_conversation('website_result_success'):
                    res = self.get_response(message)
                    self.assertTrue("success" in res['content'])
