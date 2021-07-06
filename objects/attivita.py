import sqlite3
conn = sqlite3.connect('attivita.db')

c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS attivita(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, tipo INTEGER, timestamp INTEGER, durata INTEGER, distanza INTEGER, calorie INTEGER)''')
conn.commit()

class Attivita:
    NUOTO = 1
    CORSA = 2
    CICLISMO = 3

    def __init__(self, user_id, tipo):
        c.execute('''INSERT INTO attivita(user_id, tipo) VALUES (:user_id, :tipo)''', {'user_id': user_id, 'tipo': tipo})
        conn.commit()
        self.id = c.lastrowid

    def __init__(self, id):
        self.id = c.id

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
