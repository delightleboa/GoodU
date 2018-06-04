from unittest.mock import patch
import sys
from typing import Dict, Any, Optional
from wyzepal_bots.test_lib import BotTestCase, get_bot_message_handler, StubBotHandler

class TestWitaiBot(BotTestCase):
    bot_name = 'witai'

    MOCK_CONFIG_INFO = {
        'token': '12345678',
        'handler_location': '/Users/abcd/efgh',
        'help_message': 'Qwertyuiop!'
    }

    MOCK_WITAI_RESPONSE = {
        '_text': 'What is your favorite food?',
        'entities': {
            'intent': [{
                'confidence': 1.0,
                'value': 'favorite_food'
            }]
        }
    }

    def test_normal(self) -> None:
        with self.mock_config_info(self.MOCK_CONFIG_INFO):
            get_bot_message_handler(self.bot_name).initialize(StubBotHandler())

            with patch('wit.Wit.message') as message:
                message.return_value = self.MOCK_WITAI_RESPONSE

                with patch('wyzepal_bots.bots.witai.witai.get_handle') as handler:
                    handler.return_value = mock_handle

                    self.verify_reply(
                        'What is your favorite food?',
                        'pizza'
                    )

    # This overrides the default one in `BotTestCase`.
    def test_bot_responds_to_empty_message(self) -> None:
        with self.mock_config_info(self.MOCK_CONFIG_INFO):
            get_bot_message_handler(self.bot_name).initialize(StubBotHandler())

            with patch('wit.Wit.message') as message:
                message.return_value = self.MOCK_WITAI_RESPONSE

                with patch('wyzepal_bots.bots.witai.witai.get_handle') as handler:
                    handler.return_value = mock_handle

                    self.verify_reply('', 'Qwertyuiop!')

def mock_handle(res: Dict[str, Any]) -> Optional[str]:
    if res['entities']['intent'][0]['value'] == 'favorite_food':
        return 'pizza'
    if res['entities']['intent'][0]['value'] == 'favorite_drink':
        return 'coffee'

    return None
