from chatterbot import ChatBot

# bot = ChatBot('Buddy',
#             logic_adapters=[{
#             'import_path': 'chatterbot.logic.BestMatch',
#             'default_response': 'I am sorry, but I do not understand.',
#             'maximum_similarity_threshold': 0.90
#         }],
#             read_only = True,
#             preprocessors=['chatterbot.preprocessors.clean_whitespace',
#                         'chatterbot.preprocessors.unescape_html',
#                         'chatterbot.preprocessors.convert_to_ascii']
#                         )

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# Creating ChatBot Instance
chatbot = ChatBot(
    'CoronaBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch',
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand. I am still learning.',
            'maximum_similarity_threshold': 0.90
        }
    ],
    database_uri='sqlite:///database.sqlite3'
)

 # Training with Personal Ques & Ans
training_data_quesans = open('nxthen/training_data/chatbot_data.txt').read().splitlines()

training_data = training_data_quesans

trainer = ListTrainer(chatbot)
trainer.train(training_data)

# Training with English Corpus Data
trainer_corpus = ChatterBotCorpusTrainer(chatbot)
trainer_corpus.train(
    'chatterbot.corpus.english'
)

