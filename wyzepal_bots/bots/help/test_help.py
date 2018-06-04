from wyzepal_bots.test_lib import BotTestCase

from typing import Any

class TestHelpBot(BotTestCase):
    bot_name = "help"

    def test_bot(self) -> None:
        help_text = "Info on WyzePal can be found here:\nhttps://github.com/wyzepal/wyzepal"
        requests = ["", "help", "Hi, my name is abc"]

        dialog = [
            (request, help_text)
            for request in requests
        ]

        self.verify_dialog(dialog)
