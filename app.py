import os
import openai
from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

bot = telegram.Bot(token=TELEGRAM_TOKEN)
app = Flask(__name__)


@app.route('/hook', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return 'ok'


openai.api_key = OPENAI_KEY


def chat_ai(input_str):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Human: {input_str} \n AI:",
    temperature=0.9,
    max_tokens=999,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
    )

    print(response)
    res = response['choices'][0]['text']
    if res.startswith("？") or res.startswith("?"):
        res = res[1:]
    return res.strip()


def reply_handler(update ,bot):
    """Reply message."""
    try:
        text = update.message.text
        if text.startswith("ChatGPT: "):
          text = text[4:]
          print(text)
          res = chat_ai(text)
          print(res)
          update.message.reply_text(res)

    except Exception as e:
        print(e)

dispatcher = Dispatcher(bot, None)
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))