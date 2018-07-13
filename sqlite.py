import sqlite3
import os


class DataBase():
    DB_NAME = 'minerboard_bot.db'
    DB_PATH = r'C:\Users\OZOAR\Desktop\BotTest\DB'

    @staticmethod
    def db_create():
        con = sqlite3.connect(os.path.join(DataBase.DB_PATH, DataBase.DB_NAME))
        cur = con.cursor()
        data = 'CREATE TABLE' \
               ' users ' \
               '(id INTEGER PRIMARY KEY,' \
               ' nickname TEXT,' \
               ' username TEXT,' \
               ' user_id  TEXT,' \
               ' language TEXT,' \
               ' UNIQUE(username, user_id))'

        try:
            cur.execute(data)
            con.commit()
            print('Success.' + DataBase.DB_NAME + ' created.')
        except sqlite3.OperationalError:
            print(DataBase.DB_NAME + " is already exists.\n")

    @staticmethod
    def db_insert(data):
        con = sqlite3.connect(os.path.join(DataBase.DB_PATH, DataBase.DB_NAME))
        cur = con.cursor()
        try:
            cur.execute('INSERT OR IGNORE INTO users VALUES (?,?,?,?,?)', data)
            con.commit()
            print('Success. Data selected from ' + DataBase.DB_NAME)
        except Exception as err:
            print(DataBase.DB_NAME + " occurred any troubles.\n" + str(err))

    @staticmethod
    def db_select(user_id='', full=0):
        con = sqlite3.connect(os.path.join(DataBase.DB_PATH, DataBase.DB_NAME))
        cur = con.cursor()
        data = None
        try:
            if full:
                data = cur.execute('SELECT * FROM users')
                con.commit()
                print('Success. Data selected from ' + DataBase.DB_NAME)
                return data
            data = cur.execute("SELECT * FROM users WHERE user_id = '" + user_id + "'")
            con.commit()
            return data
        except Exception:
            print(DataBase.DB_NAME + " occurred any troubles.\n")
            return data

    @staticmethod
    def db_delete(user_id):
        con = sqlite3.connect(os.path.join(DataBase.DB_PATH, DataBase.DB_NAME))
        cur = con.cursor()
        try:
            cur.execute('DELETE FROM users WHERE user_id = ' + str(user_id))
            con.commit()
            print('user ' + str(user_id) + ' has been deleted from ' + DataBase.DB_NAME)
            return True
        except Exception as err:
            print(err)
            print(DataBase.DB_NAME + " occurred any troubles.\n")
            return False

# c = DataBase()
# c.db_create()
# c.db_insert([None,'vadim','@ozoar','391058952','ru-ru'])
# print(c.db_delete(391058952))
# print(c.db_select(full=1).fetchall())
