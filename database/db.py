import sqlite3
import difflib

database_dir = "./database"
database = f"{database_dir}/database.db"


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

def build_compare_string(content):
    assert 'date' in content
    assert 'time' in content
    assert 'detail' in content
    assert 'link' in content

    return f"""```ansi==================
Date:
        {content['date']}
Time:
        {content['time']}
Detail:
        {content['detail']}
Link: 
        {content['link']}
```
"""

def prepare_color_string(content):
    assert 'date' in content
    assert 'time' in content
    assert 'detail' in content
    assert 'link' in content

    return f"""```ansi==================
,Date:
!        {content['date']}
,Time:
+        {content['time']}
,Detail:
+        {content['detail']}
,Link: 
.        {content['link']}
```
""" 

def compare_diff(string1, string2):
    diff = difflib.unified_diff(string1.splitlines(), string2.splitlines())
    diff_line = ""
    for line in diff:
        diff_line += line.replace('\n', '') + '\n'
    return diff_line

def check_and_set_Meeting_data(channel_id, title, contents):
    assert channel_id != ""
    assert title != ""

    compare_content_str = f"{title}\n"
    for content in contents:
        compare_content_str += build_compare_string(content)

    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute(
        f'select content from Meeting_Time where channel_id == "{channel_id}" and title == "{title}"'
    )
    query = cur.fetchall()

    result = ""
    if len(query) == 0:
        cur.execute(
            f'insert into Meeting_Time (channel_id, title, content) values ("{channel_id}", "{title}", "{compare_content_str}")'
        )
        result = "[New Meeting !!]\n\n"
        for content in contents:
            result += prepare_color_string(contents)
    else:
        if query[0][0] != compare_content_str:
            old_content_str = query[0][0]
            cur.execute(
                f'update Meeting_Time set content = "{compare_content_str}" where channel_id = "{channel_id}" and title = "{title}"'
            )

            compare_diff_str = compare_diff(old_content_str, compare_content_str)
            result = "[Meeting Update !!]\n\n" + compare_diff_str
        else:
            result = None

    con.commit()
    con.close()

    return result
