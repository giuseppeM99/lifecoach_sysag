import botogram
import json
import html
from os import getenv
from dotenv import load_dotenv
from wit import Wit
from google_trans_new import google_translator

load_dotenv()

LOG_CHANNEL = getenv('LOG_CHANNEL')
bot = botogram.create(getenv('TG_TOKEN'))
wit = Wit(getenv('WIT_TOKEN'))
translator = google_translator()


@bot.command("hello")
def hello_command(chat, message, args):
    """Dice ciao in inglese"""
    chat.send("Hello world!")

@bot.command("que")
def que_command(chat, message, args):
    chat.send("Colvoque")

@bot.process_message
def process_message(chat, message):
    if chat.id < 0:
        return
    if not message.text:
        return
    messaggio_utente = message.text
    messaggio_tradotto = translator.translate(messaggio_utente, lang_tgt='en')
    if messaggio_tradotto is None:
        return
    res = wit.message(messaggio_tradotto)
    tres = html.escape(json.dumps(res, indent=True))
    chat.send("<pre>"+tres+"</pre>")
    bot.chat(LOG_CHANNEL).send('User: '+ message.sender.first_name + '\n'
                        + 'Message: <pre>' + messaggio_utente + '</pre>\n'
                        + 'Res : <pre>'+tres+'</pre>')

if __name__ == "__main__":
    bot.run()
