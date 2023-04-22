import os
import openai
import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters

openai.api_key = os.getenv("OPENAI_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


class ChatGptTelegramBot:
    def __init__(self):
        self.bot = telegram.Bot(token=TELEGRAM_TOKEN)
        self.dispatcher = Dispatcher(self.bot, None)
        self.dispatcher.add_handler(
            MessageHandler(Filters.text, self.reply_handler))
        self.messages = []

    def reply_handler(self, update, bot):
        try:
            text = update.message.text
            if text == "ChatGPT: clear" or text == "ChatGPT: Clear":
                self.messages = []
                update.message.reply_text("Clear ChatGPT messages complete")
            elif text.startswith("ChatGPT: "):
                text = text[9:]
                res = self.chat_ai(text)
                print(f"ME: {text}")
                print(f"AI: {res}")
                update.message.reply_text(res)
        except Exception as e:
            print(e)

    def chat_ai(self, input_str):
        if len(self.messages) > 10:
            self.messages = self.messages[-10:]
        self.messages.append({"role": "user", "content": input_str})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=0.9,
            top_p=1,
            max_tokens=512,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=None
        )
        ai_msg = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": ai_msg})
        print(self.messages)  # debug
        return ai_msg
