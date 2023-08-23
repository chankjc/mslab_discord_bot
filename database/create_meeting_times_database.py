import hashlib
import sqlite3
import datetime

database_dir = "./database"
database = f"{database_dir}/database.db"

def CreateTable():
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('create table Meeting_Time (channel_id, title, content)')
    con.commit()
    con.close()

CreateTable()