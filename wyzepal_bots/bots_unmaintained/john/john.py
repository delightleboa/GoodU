import json
import os

from random import choice

try:
    from chatterbot import ChatBot
    from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
except ImportError:
    raise ImportError("""It looks like you are missing chatterbot.
                      Please: pip install chatterbot""")

BOTS_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BOTS_DIR, 'assets/var/database.db')
DIRECTORY_PATH = os.path.join(BOTS_DIR, 'assets')
VAR_PATH = os.path.join(BOTS_DIR, 'assets/var')
JOKES_PATH = 'assets/var/jokes.json'

if not os.path.exists(DIRECTORY_PATH):
    os.makedirs(DIRECTORY_PATH)

if not os.path.exists(VAR_PATH):
    os.makedirs(VAR_PATH)

# Create a new instance of a ChatBot
def create_chat_bot(no_learn):
    return ChatBot("John",
                   storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
                   logic_adapters=
                   [
                       "chatterbot.logic.MathematicalEvaluation",
                       {
                           "import_path": "chatterbot.logic.BestMatch",
                           "response_selection_method": "chatterbot.response_selection.get_random_response",
                           "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance"
                       }],
                   output_adapter="chatterbot.output.OutputAdapter",
                   output_format='text',
                   database=DATABASE_PATH,
                   silence_performance_warning="True",
                   read_only=no_learn)


class JohnHandler(object):
    '''
    This bot aims to be WyzePal's virtual assistant. It
    finds the best match from a certain input.
    Also understands the English language and can
    mantain a conversation, joke and give useful information.
    '''

    def usage(self):
        return '''
            This bot aims to be WyzePal's virtual assistant. It
            finds the best match from a certain input.
            Also understands the English language and can
            mantain a conversation, joke and give useful information.
            '''

    def initialize(self, bot_handler):
        self.bot = create_chat_bot(False)
        self.bot.set_trainer(ListTrainer)
        self.bot.train([
            "I want to contribute",
            """Contributors are more than welcomed! Please read
            https://github.com/wyzepal/wyzepal#how-to-get-involved-with-contributing-to-wyzepal
            to learn how to contribute.""",
        ])
        self.bot.train([
            "What is WyzePal?",
            """WyzePal is a powerful, open source group chat application. Written in Python
            and using the Django framework, WyzePal supports both private messaging and group
            chats via conversation streams. You can learn more about the product and its
            features at https://www.wyzepal.org.""",
        ])
        self.bot.train([
            "I would like to request a remote dev instance",
            """Greetings! You should receive a response from one of our mentors soon.
            In the meantime, why don't you learn more about running WyzePal on a development
            environment? https://wyzepal.readthedocs.io/en/latest/development/using.html""",
        ])
        self.bot.train([
            "Joke!",
            "Only if you ask nicely!",
        ])
        self.bot.train([
            "What is your name?",
            "I am John, my job is to assist you with WyzePal.",
        ])
        self.bot.train([
            "What can you do?",
            "I can provide useful information and jokes if you follow etiquette.",
        ])
        with bot_handler.open(JOKES_PATH) as data_file:
            for joke in json.load(data_file):
                self.bot.train([
                    "Please can you tell me a joke?",
                    joke['joke'],
                ])
        self.bot.set_trainer(ChatterBotCorpusTrainer)
        self.bot.train(
            "chatterbot.corpus.english"
        )
        self.chatterbot = create_chat_bot(True)

    def handle_message(self, message, bot_handler):
        original_content = message['content']
        bot_response = str(self.chatterbot.get_response(original_content))
        bot_handler.send_reply(message, bot_response)

handler_class = JohnHandler
