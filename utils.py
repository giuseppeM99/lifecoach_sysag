from google_trans_new import google_translator
import json
from wit import Wit
from os import getenv

witInstance = Wit(getenv('WIT_TOKEN'))

translator = google_translator()

def traduci(message):
    try:
        res = translator.translate(message, lang_src='it', lang_tgt='en')
        return res
    except json.decoder.JSONDecodeError:
        print('translation error')
        return None
    return None

def wit(message, contesto = None):
    trad = traduci(message)
    if trad is None:
        return None
    return witraw(trad, contesto)

def witraw(message, contesto = None):
    return witInstance.message(message, contesto)

