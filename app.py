from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name, URL
from telebot.mastermind import get_response

from classifier import Classifier


global bot
global TOKEN
global clf

TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
clf = Classifier()

app = Flask(__name__)


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    print("got text message :", text)

    response = clf.get_result_message(text)
    bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)

    return 'ok'


@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    app.run(threaded=True)
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        print("webhook setup ok")
    else:
        print("webhook setup failed")
