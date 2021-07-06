import sqlite3
conn = sqlite3.connect('user.db')

c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS user(user_id INTEGER PRIMARY KEY, state STRING, eta INTEGER)''')
conn.commit()

class User:
    STATE_SEP = ','
    def __init__(self, user):
        self.id = user.id
        c.execute('''INSERT OR IGNORE INTO user(user_id) VALUES(?)''', (self.id,))
        conn.commit()

    def pushState(self, nextState):
        curState = self.getState()
        print(curState)
        if curState is None:
            curState = nextState
        else:
            curState = self.STATE_SEP.join([nextState, *str(curState).split(',')])
        self.setState(curState)


    def popState(self, remove = False):
        curState = self.getState()
        if curState is None:
            return False
        splitted = str(curState).split(',')
        prevState = splitted.pop(0)
        if remove:
            newState = None
            if len(splitted) > 0:
                newState = self.STATE_SEP.join(splitted)
            self.setState(newState)
        return prevState

    def getState(self):
        c.execute('''SELECT state FROM user WHERE user_id = ?''', (self.id,))
        u = c.fetchone()
        if u is False:
            u = None
        if u is not None:
            return u[0]
        return None

    def setState(self, newState):
        if newState is False:
            newState = None
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
