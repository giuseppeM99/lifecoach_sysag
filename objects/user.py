import sqlite3
conn = sqlite3.connect('user.db')

c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS user(user_id INTEGER PRIMARY KEY, state STRING, eta INTEGER)''')
conn.commit()

class User:
    def __init__(self, user):

        print('User object %s created' % user.id)
        self.id = user.id
        c.execute('''INSERT OR IGNORE INTO user(user_id) VALUES(?)''', (self.id,))

    def getState(self):

        c.execute('''SELECT state FROM user WHERE user_id = ?''', (self.id,))
        u = c.fetchone()
        if u is not None:
            return u[0]
        return None

    def setState(self, newState):
        c.execute('''UPDATE user SET state = :state WHERE user_id = :user_id''', {'user_id': self.id, 'state': newState})
        conn.commit()
        return True

    def setEta(self, eta):
        c.execute('''UPDATE user SET eta = :eta WHERE user_id = :user_id''', {'user_id': self.id, 'eta': eta})
        conn.commit()

    def getEta(self):
        c.execute('''SELECT eta FROM user WHERE user_id = ?''', (self.id,))
        u = c.fetchone()
        if u is not None:
            return u[0]
        return None
