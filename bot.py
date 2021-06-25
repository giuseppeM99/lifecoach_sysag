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


bot.about = "Questo chatbot aiuta l'utente a monitorare l'andamento di una o più attività sportive a scelta tra " \
            "nuoto, ciclismo e corsa, affinchè esse possano essere svolte rispettando la programmazione iniziale e " \
            "i parametri standard riguardanti l'allenamento previsto."


@bot.command("start")
def start_command(chat, message, args):
    btns = botogram.Buttons()
    btns[0].callback("Nuoto \U0001F3CA", "nuoto")
    btns[1].callback("Corsa \U0001F3C3", "corsa")
    btns[2].callback("Ciclismo \U0001F6B4", "ciclismo")
    utente = message.sender.first_name
    chat.send(f"Ciao {utente} \U0001F604, benvenuto/a nel LifeCoach Chatbot di @AlexPlus117, @antony_9, @giuseppeM99, "
              f"@jolly000 e @Xander9000.\n\nD'ora in poi ti aiuterò a gestire le attività sportive che vorrai svolgere."
              f"\nPuoi decidere tra queste 3 attività:\n- Nuoto \U0001F3CA \n- Corsa \U0001F3C3 \n"
              f"- Ciclismo \U0001F6B4 \n\nTerrò conto delle risposte che darai alle mie domande e dei parametri che mi"
              f" fornirai alla fine dell'allenamento per aiutarti a monitorare e gestire l'andamento "
              f"dell'esercizio \U0001F4C8 \n\nOra puoi scrivermi la prima attività che hai intenzione di svolgere "
              f"oppure, visto che è la prima volta, puoi selezionarla tramite i pulsanti qui sotto \U0001F609",
              attach=btns)


@bot.callback("nuoto")
def nuoto_callback(query, chat, message):
    chat.send("L'intent è il nuoto")


@bot.callback("corsa")
def corsa_callback(query, chat, message):
    chat.send("L'intent è la corsa")


@bot.callback("ciclismo")
def ciclismo_callback(query, chat, message):
    chat.send("L'intent è il ciclismo")


@bot.callback("sbagliato")
def sbagliato_callback(query, chat, message):
    chat.send("Perdonami \U0001F605 \nProva a dirmi di nuovo quale attività vuoi svolgere, magari in maniera più "
              "precisa, in modo tale che io possa comprendere al meglio \U0001F609")


@bot.process_message
def process_message(chat, message):
    btns_nuoto = botogram.Buttons()
    btns_nuoto[0].callback("Sì \U0001F44D", "nuoto")
    btns_nuoto[0].callback("No \U0001F44E", "sbagliato")

    btns_corsa = botogram.Buttons()
    btns_corsa[0].callback("Sì \U0001F44D", "corsa")
    btns_corsa[0].callback("No \U0001F44E", "sbagliato")

    btns_ciclismo = botogram.Buttons()
    btns_ciclismo[0].callback("Sì \U0001F44D", "ciclismo")
    btns_ciclismo[0].callback("No \U0001F44E", "sbagliato")

    if chat.id < 0:
        return
    if not message.text:
        return
    messaggio_utente = message.text
    messaggio_tradotto = translator.translate(messaggio_utente, lang_src='it', lang_tgt='en')
    if messaggio_tradotto is None:
        return
    res = wit.message(messaggio_tradotto)

    if not res['intents']:
        chat.send("Non ho capito quale attività hai scelto \U0001F605 \n\nRicordati che puoi selezionare "
                  "solo queste attività:\n- Nuoto \U0001F3CA \n- Corsa \U0001F3C3 \n- Ciclismo \U0001F6B4 \n\n"
                  "Potresti ripetere?")

    elif res['intents'][0]['name'] == 'add_swimming':
        chat.send("Hai selezionato l'attività di nuoto \U0001F3CA \nConfermi la scelta?", attach=btns_nuoto)

    elif res['intents'][0]['name'] == 'add_running':
        chat.send("Hai selezionato l'attività di corsa \U0001F3C3 \nConfermi la scelta?", attach=btns_corsa)

    elif res['intents'][0]['name'] == 'add_cycling':
        chat.send("Hai selezionato l'attività di ciclismo \U0001F6B4 \nConfermi la scelta?", attach=btns_ciclismo)

    # tres = html.escape(json.dumps(res, indent=True))
    # chat.send("<pre>"+tres+"</pre>")
    # bot.chat(LOG_CHANNEL).send('User: '+ message.sender.first_name + '\n'
    #                     + 'Message: <pre>' + messaggio_utente + '</pre>\n'
    #                     + 'Res : <pre>'+tres+'</pre>')


if __name__ == "__main__":
    bot.run()
