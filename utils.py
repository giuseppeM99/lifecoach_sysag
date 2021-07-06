from itranslate import itranslate as itrans
import json
from wit import Wit
from os import getenv
witInstance = Wit(getenv('WIT_TOKEN'))


def traduci(message):
    try:
        print(message)
        res = itrans(message, from_lang='it', to_lang='en')
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
