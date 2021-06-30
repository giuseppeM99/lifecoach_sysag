
from dotenv import load_dotenv
load_dotenv()

import botogram
from os import getenv
from utils import wit
from objects.user import User

LOG_CHANNEL = getenv('LOG_CHANNEL')
bot = botogram.create(getenv('TG_TOKEN'))



bot.about = "Questo chatbot aiuta l'utente a monitorare l'andamento di una o più attività sportive a scelta tra " \
            "nuoto, ciclismo e corsa, affinchè esse possano essere svolte rispettando la programmazione iniziale e " \
            "i parametri standard riguardanti l'allenamento previsto."

def checkEta(user):
    if User(user).getEta() is None:
        bot.chat(user.id).send('Per poter funzionare devo sapere la tua età, puoi dirmi quanti anni hai?')
        User(user).setState('set_eta')

@bot.command("start")
def start_command(chat, message, args):
    # resetto lo stato
    User(message.sender).setState(None)
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
def nuoto_callback(query, chat):
    User(query.sender).setState('add_nuoto')
    chat.send("L'intent è il nuoto")
    checkEta(query.sender)


@bot.callback("corsa")
def corsa_callback(query, chat):
    User(query.sender).setState('add_corsa')
    chat.send("L'intent è la corsa")


@bot.callback("ciclismo")
def ciclismo_callback(query, chat):
    User(query.sender).setState('add_ciclismo')
    chat.send("L'intent è il ciclismo")


@bot.callback("sbagliato")
def sbagliato_callback(query, chat):
    User(query.sender).setState(None)
    chat.send("Perdonami \U0001F605 \nProva a dirmi di nuovo quale attività vuoi svolgere, magari in maniera più "
              "precisa, in modo tale che io possa comprendere al meglio \U0001F609")


@bot.process_message
def process_message(chat, message):
    u = User(message.sender)

    state = u.getState()
    if state is not None:
        print('Ha uno stato: %s' %state)
        if state == 'set_eta':
            numeri = [int(s) for s in message.text.split() if s.isdigit()]
            if len(numeri) == 1:
                chat.send('Ok, hai %s anni' %numeri[0])
                u.setEta(numeri[0])
                u.setState()
            else:
                chat.send('Non credo di aver capito bene, puoi ripetere')
        #vedere che fare qua in base agli state
        return

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

    res = wit(message.text)

    print(res)
    if res is None or not res['intents']:
        chat.send("Non ho capito quale attività hai scelto \U0001F605 \n\nRicordati che puoi selezionare "
                  "solo queste attività:\n- Nuoto \U0001F3CA \n- Corsa \U0001F3C3 \n- Ciclismo \U0001F6B4 \n\n"
                  "Potresti ripetere?")

    elif res['intents'][0]['name'] == 'add_swimming':
        chat.send("Confermi di aver selezionato un'attività di nuoto? \U0001F3CA", attach=btns_nuoto)

    elif res['intents'][0]['name'] == 'add_running':
        chat.send("Confermi di aver selezionato un'attività di corsa? \U0001F3C3", attach=btns_corsa)

    elif res['intents'][0]['name'] == 'add_cycling':
        chat.send("Confermi di aver selezionato un'attività di ciclismo? \U0001F6B4", attach=btns_ciclismo)

    # tres = html.escape(json.dumps(res, indent=True))
    # chat.send("<pre>"+tres+"</pre>")
    # bot.chat(LOG_CHANNEL).send('User: '+ message.sender.first_name + '\n'
    #                     + 'Message: <pre>' + messaggio_utente + '</pre>\n'
    #                     + 'Res : <pre>'+tres+'</pre>')

if __name__ == "__main__":
    bot.run()
