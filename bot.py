import botogram
import json
import html
from os import getenv
from dotenv import load_dotenv
from wit import Wit

load_dotenv()

bot = botogram.create(getenv('TG_TOKEN'))
wit = Wit(getenv('WIT_TOKEN'))

@bot.command("hello")
def hello_command(chat, message, args):
    """Dice ciao in inglese"""
    chat.send("Hello world!")

@bot.process_message
def process_message(chat, message):
    chat.send("<pre>"+html.escape(json.dumps(wit.message(message.text), indent=True))+"</pre>")

if __name__ == "__main__":
    bot.run()
