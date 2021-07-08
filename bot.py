
from dotenv import load_dotenv
load_dotenv()

import botogram
from os import getenv
from utils import wit, durataH
from objects.user import User
from objects.attivita import Attivita
from dateutil import parser
from datetime import datetime

LOG_CHANNEL = getenv('LOG_CHANNEL')
bot = botogram.create(getenv('TG_TOKEN'))


bot.about = "Questo chatbot aiuta l'utente a monitorare l'andamento di una o più attività sportive a scelta tra " \
            "nuoto, ciclismo e corsa, affinchè esse possano essere svolte rispettando la programmazione iniziale e " \
            "i parametri standard riguardanti l'allenamento previsto."


def riepilogo(chat, message, a, u):
    chat.send('Ok! Adesso ti dico come è andata...\n')

    # controllo durata
    if a.getDurataEffettiva() > a.getDurata() + 300:
        chat.send("Hai svolto l'attività per più tempo previsto. Cerca sempre di non esagerare perchè il tuo corpo potrebbe risentirne.")
    elif a.getDurata() + 300 >= a.getDurataEffettiva() >= a.getDurata() - 300:
        chat.send("Complimenti! Hai svolto l'attività rispettando la durata prevista.")
    else:
        chat.send("Purtroppo hai svolto l'attività per meno tempo previsto. La prossima volta, magari, cerca di rispettare la durata prestabilita.")

    # controllo percorso
    if a.getDistanzaEffettiva() > a.getDistanza():
        chat.send("Per quanto riguarda il percorso, hai superato la distanza impostata da te all'inizio. Cerca sempre di adeguarti il più possibile alla programmazione iniziale.")
    elif a.getDistanzaEffettiva() == a.getDistanza():
        chat.send("Per quanto riguarda il percorso, hai rispettato la distanza impostata da te all'inizio. Ottimo!")
    else:
        chat.send("Per quanto riguarda il percorso, non hai raggiunto la distanza impostata da te all'inizio. La prossima volta, magari, prova a percorrere un tratto più lungo.")

    # controllo pulsazioni (formula di Tanaka)
    if a.getPulsazioni() >= 208 - 0.7 * u.getEta():
        chat.send("Secondo la formula di Tanaka, hai superato il limite di pulsazioni massime per la tua età. Ti consiglio di andare da un medico il più presto possibile!")
    else:
        chat.send("Secondo la formula di Tanaka, rientri nel range di pulsazioni massime per la tua età. Tuttavia, ti consiglio comunque di consultare un medico o un esperto del settore per più sicurezza.")

    # controllo calorie
    if a.getCalorieEffettive() > a.getCalorie() + 20:
        chat.send("Per quanto riguarda le calorie invece, avresti potuto diminuire l'intensità dell'attività dato che hai bruciato più calorie di quanto mi avevi detto all'inizio.")
    elif a.getCalorie() + 20 >= a.getCalorieEffettive() >= a.getCalorie() - 20:
        chat.send("Per quanto riguarda le calorie invece, hai bruciato circa le stesse calorie che mi avevi detto all'inizio. Bravo, continua così!")
    else:
        chat.send("Per quanto riguarda le calorie invece, avresti potuto aumentare l'intensità dell'attività dato che hai bruciato meno calorie di quanto mi avevi detto all'inizio.")


@bot.command("start")
def start_command(chat, message, args):
    # resetto lo stato
    u = User(message.sender)
    u.setState(None)


    # if u.getEta() is None:
    #    kb = botogram.Buttons()
    #    kb[0].callback("Imposta la tua età", "set_eta")
    #    chat.send('Ciao, prima di potermi usare devi dirmi quanti anni hai, se vuoi procedere digita clicca qui', attach=kb)
    #    return

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


# @bot.command("set_eta")
# def eta_command(chat, message):
#     u = User(message.sender)
#     chat.send('Ora inviami la tua età')
#     u.pushState('set_eta')
#
# @bot.callback("set_eta")
# def eta_command(chat, query):
#     chat.delete_message(query.message)
#     u = User(query.sender)
#     chat.send('Ora inviami la tua età')
#     u.pushState('set_eta')

@bot.callback("nuoto")
def nuoto_callback(query, chat):
    u = User(query.sender)
    a = Attivita(query.sender.id, Attivita.NUOTO)
    chat.delete_message(query.message)

    u.pushState(a.getID())
    u.pushState('add_dataora')

    chat.send("Bene, quando hai intenzione di andare a nuotare? Dimmi pure la data e l'ora")


@bot.callback("corsa")
def corsa_callback(query, chat):
    u = User(query.sender)
    a = Attivita(query.sender.id, Attivita.CORSA)
    chat.delete_message(query.message)

    u.pushState(a.getID())
    u.pushState('add_dataora')

    chat.send("Bene, quando hai intenzione di andare a correre? Dimmi pure la data e l'ora")


@bot.callback("ciclismo")
def ciclismo_callback(query, chat):
    u = User(query.sender)
    a = Attivita(query.sender.id, Attivita.CICLISMO)
    chat.delete_message(query.message)

    u.pushState(a.getID())
    u.pushState('add_dataora')

    chat.send("Bene, quando hai intenzione di andare in bici? Dimmi pure la data e l'ora")


@bot.callback("sbagliato")
def sbagliato_callback(query, chat):
    User(query.sender).setState(None)
    chat.send("Perdonami \U0001F605 \nProva a dirmi di nuovo quale attività vuoi svolgere, magari in maniera più "
              "precisa, in modo tale che io possa comprendere al meglio \U0001F609")


def pstate_set_eta(chat, message, user):
    numeri = [int(s) for s in message.text.split() if s.isdigit()]
    if len(numeri) == 1:
        chat.send('Ok, hai %s anni, se vuoi modificarla puoi usare il comando /set_eta' % numeri[0])
        user.setEta(numeri[0])
        user.popState(True)
    else:
        chat.send('Non credo di aver capito bene, puoi ripetere')


def dataora(chat, message, u):
    res = wit(message.text)
    if res['entities']['wit$datetime:time'] is not None and res['entities']['wit$datetime:time'][0] is not None:
        data = parser.parse(res['entities']['wit$datetime:time'][0]['value'])
        oggi = datetime.now()

        if data.timestamp() < oggi.timestamp():
            chat.send("Non puoi aggiungere un'azione nel passato, inserisci una data presente")
            return

        u.popState(True)
        Attivita(u.popState()).setTimestamp(int(data.timestamp()))
        chat.send("Ok, ho programmato l'attività per il "+data.strftime('%d/%m/%Y')+" alle ore "+data.strftime('%H:%M')+"\nOra dimmi per quanto tempo hai intenzione di fare attività")
        u.pushState('add_durata')
        # inserire e chiedere conferma
    else:
        chat.send("Non ho capito, per favore inserisci la data e l'ora dell'attività che vuoi svolgere")


def durata(chat, message, u):
    res = wit(message.text)
    if res['entities']['wit$duration:duration'] is not None and res['entities']['wit$duration:duration'][0] is not None:
        durata = res['entities']['wit$duration:duration'][0]['normalized']['value']

        u.popState(True)
        Attivita(u.popState()).setDurata(durata)
        chat.send("Ok, ho impostato la durata dell'attività "+durataH(durata))
        chat.send("Ora dimmi quante calorie pianifichi di perdere durante questa attività")
        u.pushState('add_calorie')
    else:
        chat.send("Non ho capito, per favore inserisci la durata dell'attività (esempio 30 minuti)")

def calorie(chat, message, u):
    if "no" in message.text.lower():
        chat.send("Ok, non conteremo le calorie")
        u.setState(None)

    numeri = [int(s) for s in message.text.split() if s.isdigit()]
    if len(numeri) == 1:
        calorie = numeri[0]
        u.popState(True)
        chat.send('Ok, hai intenzione di perdere %s calorie' % calorie)
        Attivita(u.popState()).setCalorie(calorie)
        u.setState(None)
    else:
        chat.send("Non ho capito, per favore inserisci un numero (per esempio 100 calorie), se non vuoi inserire le calorie scrivi <b>No</b>")
        return
    chat.send("Bene, ti avviserò quando dovrai fare attività")

def durataEffettiva(chat, message, u):
    res = wit(message.text)
    if res['entities']['wit$duration:duration'] is not None and res['entities']['wit$duration:duration'][0] is not None:
        durata = res['entities']['wit$duration:duration'][0]['normalized']['value']

        u.popState(True)
        Attivita(u.popState()).setDurataEffettiva(durata)
        chat.send("Ok, ho impostato la durata effettiva dell'attività "+durataH(durata))
        if Attivita(u.popState()).getCalorie() is not None:
            chat.send("Ora dimmi quante calorie hai perso durante questa attività")
            u.pushState('add_calorie_effettive')
        else:
            chat.send("Ora dimmi quante pulsazioni al minuto hai fatto in media")
            u.pushState('add_pulsazioni')
    else:
        chat.send("Non ho capito, per favore inserisci la durata effettiva dell'attività (esempio 30 minuti)")

def calorieEffettive(chat, message, u):
    numeri = [int(s) for s in message.text.split() if s.isdigit()]
    if len(numeri) == 1:
        calorie = numeri[0]
        u.popState(True)
        chat.send('Ok, hai perso %s calorie' % calorie)
        Attivita(u.popState()).setCalorieEffettive(calorie)
        chat.send("Ora dimmi quante pulsazioni al minuto hai fatto in media")
        u.pushState('add_pulsazioni')
    else:
        chat.send("Non ho capito, per favore inserisci un numero (per esempio 100 calorie)")
        return

def pulsazioni(chat, message, u):
    numeri = [int(s) for s in message.text.split() if s.isdigit()]
    if len(numeri) == 1:
        bpm = numeri[0]
        u.popState(True)
        chat.send('Ok, hai un ritmo cardiaco di %s battiti al minuto' % bpm)
        Attivita(u.popState()).setPulsazioni(bpm)
        a = Attivita(u.popState())
        u.setState(None)
        riepilogo(bot, chat, a, u)
    else:
        chat.send("Non ho capito, per favore inserisci un numero (per esempio 100 battiti)")
        return


@bot.command("lista")
def lista(chat, message, args):
    lista = Attivita.listaTotale(message.sender.id)
    text = ""
    for att in lista:
        if att.getTimestamp() is None:
            att.delete()
            continue
        text = text + str(att.getID()) + ") " + att.getTipoStr() + " del " + datetime.utcfromtimestamp(att.getTimestamp()).strftime("%d/%m/%Y %H:%M") + "\n"
    if len(text) != 0:
        chat.send(text)
    else:
        chat.send("Nessuna attività da vedere")


@bot.command("risultati")
def risultati(chat, message, args):
    if len(args) == 0:
        return
    a = Attivita(int(args[0]))
    if a.getUserID() == message.sender.id:
        u = User(message.sender)
        u.pushState(a.getID())
        u.pushState('add_durata_effettiva')
        chat.send("Ok, dimmi ora per quanto tempo hai fatto attività")

@bot.process_message
def process_message(chat, message):
    u = User(message.sender)

    state = u.popState()
    if state is not None:
        print('Ha uno stato: %s' % state)
        if state == 'set_eta':
            pstate_set_eta(chat, message, u)
        elif state == 'add_dataora':
            dataora(chat, message, u)
        elif state == 'add_durata':
            durata(chat, message, u)
        elif state == 'add_calorie':
            calorie(chat, message, u)
        elif state == 'add_durata_effettiva':
            durataEffettiva(chat, message, u)
        elif state == 'add_calorie_effettive':
            calorieEffettive(chat, message, u)
        elif state == 'add_pulsazioni':
            pulsazioni(chat, message, u)
        else:
            u.setState(None)
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
    #                     + 'Message: <pre>' + message.text + '</pre>\n'
    #                     + 'Res : <pre>'+tres+'</pre>')


#@bot.timer(60)
#def timer(bot):
#    print("mi eseguo ogni 60 secondi")

if __name__ == "__main__":
    bot.run()
