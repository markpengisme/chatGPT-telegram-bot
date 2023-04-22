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

messages = []


def chat_ai(input_str):
    if len(messages) > 10:
        messages = messages[-10:]
    messages.append({"role": "user", "content": input_str})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.9,
        top_p=1,
        max_tokens=512,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=None
    )
    ai_msg = response.choices[0].message.content.replace('\n', '')
    messages.append({"role": "assistant", "content": ai_msg})
    print(messages)  # debug
    return ai_msg


def create_image(input_str):
    response = openai.Image.create(
        prompt=input_str,
        n=1,
        size="1024x1024"
    )
    print(response)
    res = response['data'][0]['url']
    return res.strip()


def reply_handler(update, bot):
    """Reply message."""
    try:
        text = update.message.text
        if text == "ChatGPT: clear" or text == "ChatGPT: Clear":
            messages = []
            update.message.reply_text("Clear ChatGPT messages complete")
        elif text.startswith("ChatGPT: "):
            text = text[9:]
            res = chat_ai(text)
            print(f"ME: ${text}")
            print(f"AI: ${res}")
            update.message.reply_text(res)
        elif text.startswith("DALLE: "):
            text = text[7:]
            res = create_image(text)
            print(f"ME: ${text}")
            print(f"AI: ${res}")
            update.message.reply_text(res)
    except Exception as e:
        print(e)


dispatcher = Dispatcher(bot, None)
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))
