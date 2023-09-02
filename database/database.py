import hashlib
import sqlite3
import datetime

database_dir = "./database"
database = f"{database_dir}/database.db"


def hash_string(data):
    data = data.encode("utf-8")
    result = hashlib.sha256(data).hexdigest()
    return result


def CreateTable():
    con = sqlite3.connect(database)
    cur = con.cursor()
    # cur.execute('create table Meeting_Time (channel_id, title, content)')
    # cur.execute('drop table Meeting_Time')
    # result = cur.execute('select name from sqlite_master where type="table"')
    # print(cur.fetchall())
    con.commit()
    con.close()


# CreateTable()


def check_and_set_Meeting_data(channel_id, title, content):
    assert channel_id != ""
    assert title != ""
    assert content != ""
    content_hash = hash_string(content)

    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute(
        f'select content from Meeting_Time where channel_id == "{channel_id}" and title == "{title}"'
    )
    query = cur.fetchall()

    result = ""
    if len(query) == 0:
        cur.execute(
            f'insert into Meeting_Time (channel_id, title, content) values ("{channel_id}", "{title}", "{content_hash}")'
        )
        result = "[New Meeting !!]\n\n" + content
    else:
        if query[0][0] != content_hash:
            cur.execute(
                f'update Meeting_Time set content = "{content_hash}" where channel_id = "{channel_id}" and title = "{title}"'
            )
            result = "[Meeting Update !!]\n\n" + content
    con.commit()
    con.close()

    return result
