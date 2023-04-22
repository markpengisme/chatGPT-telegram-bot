from flask import Flask, request
import telegram
from ChatGptTelegramBot import ChatGptTelegramBot

app = Flask(__name__)
chatGptTelegramBot = ChatGptTelegramBot()


@app.route('/hook', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        update = telegram.Update.de_json(
            request.get_json(force=True), chatGptTelegramBot.bot)
        chatGptTelegramBot.dispatcher.process_update(update)
    return 'ok'
