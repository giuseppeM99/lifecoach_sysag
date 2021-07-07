import sqlite3
conn = sqlite3.connect('attivita.db')

c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS attivita(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, tipo INTEGER, timestamp INTEGER, durata INTEGER, distanza INTEGER, calorie INTEGER, notificato INTEGER, pulsazioni INTEGER, durata_effettiva INTEGER, distanza_effettiva INTEGER, calorie_effettive INTEGER)''')
conn.commit()

class Attivita:
    NUOTO = 1
    CORSA = 2
    CICLISMO = 3

    def __init__(self, id, tipo = None):
        if tipo is None:
            self.id = id
        else:
            c.execute('''INSERT INTO attivita(user_id, tipo) VALUES (:user_id, :tipo)''', {'user_id': id, 'tipo': tipo})
            conn.commit()
            self.id = c.lastrowid

    def getID(self):
        return self.id

    def getUserID(self):
        c.execute('''SELECT user_id FROM attivita WHERE id = :id''', {'id': self.id})

    def getTipo(self):
        c.execute('''SELECT tipo FROM attivita WHERE id = :id''', {'id': self.id})

    def getTimestamp(self):
        c.execute('''SELECT timestamp FROM attivita WHERE id = :id''', {'id': self.id})

    def getDurata(self):
        c.execute('''SELECT durata FROM attivita WHERE id = :id''', {'id': self.id})

    def getDistanza(self):
        c.execute('''SELECT distanza FROM attivita WHERE id = :id''', {'id': self.id})

    def getCalorie(self):
        c.execute('''SELECT calorie FROM attivita WHERE id = :id''', {'id': self.id})

    def getNotificato(self):
        c.execute('''SELECT notificato FROM attivita WHERE id = :id''', {'id': self.id})

    def getPulsazioni(self):
        c.execute('''SELECT pulsazioni FROM attivita WHERE id = :id''', {'id': self.id})

    def getDurataEffettiva(self):
        c.execute('''SELECT durata_effetiva FROM attivita WHERE id = :id''', {'id': self.id})

    def getDistanzaEffettiva(self):
        c.execute('''SELECT distanza_effettiva FROM attivita WHERE id = :id''', {'id': self.id})

    def getCalorieEffettive(self):
        c.execute('''SELECT calorie_effettive FROM attivita WHERE id = :id''', {'id': self.id})

    def setTimestamp(self, timestamp):
        c.execute('''UPDATE attivita SET timestamp = :timestamp WHERE id = :id''', {'id': self.id, 'timestamp': timestamp})
        conn.commit()

    def setDurata(self, durata):
        c.execute('''UPDATE attivita SET durata = :durata WHERE id = :id''', {'id': self.id, 'durata': durata})
        conn.commit()

    def setDistanza(self, distanza):
        c.execute('''UPDATE attivita SET distanza = :distanza WHERE id = :id''', {'id': self.id, 'distanza': distanza})
        conn.commit()

    def setCalorie(self, calorie):
        c.execute('''UPDATE attivita SET calorie = :calorie WHERE id = :id''', {'id': self.id, 'calorie': calorie})
        conn.commit()

    def setNotificato(self, notificato):
        c.execute('''UPDATE attivita SET notificato = :notificato WHERE id = :id''', {'id': self.id, 'notificato': notificato})
        conn.commit()

    def setPulsazioni(self, pulsazioni):
        c.execute('''UPDATE attivita SET pulsazioni = :pulsazioni WHERE id = :id''', {'id': self.id, 'pulsazioni': pulsazioni})
        conn.commit()

    def setDurataEffettiva(self, durata_effettiva):
        c.execute('''UPDATE attivita SET durata_effettiva = :durata_effettiva WHERE id = :id''', {'id': self.id, 'durata_effettiva': durata_effettiva})
        conn.commit()

    def setDistanzaEffettiva(self, distanza_effettiva):
        c.execute('''UPDATE attivita SET distanza_effettiva = :distanza_effettiva WHERE id = :id''', {'id': self.id, 'distanza_effettiva': distanza_effettiva})
        conn.commit()

    def setCalorieEffettive(self, calorie_effettive):
        c.execute('''UPDATE attivita SET calorie_effettive = :calorie_effettive WHERE id = :id''', {'id': self.id, 'calorie_effettive': calorie_effettive})
        conn.commit()