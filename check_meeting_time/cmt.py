import dokuwiki
import os
from dotenv import load_dotenv

load_dotenv()

def get_tag_keyword_list(url="https://mslab.csie.ntu.edu.tw/wiki", page="discord"):
    try:
        wiki = dokuwiki.DokuWiki(
            url, os.getenv("MSLAB_ACCOUNT"), os.getenv("MSLAB_PASSWORD")
        )
    except (dokuwiki.DokuWikiError, Exception) as err:
        print("unable to connect: %s" % err)
        return

    content = (
        wiki.pages.get(page)
        .replace("=====", "===")
        .replace("====", "===")
        .replace("\n", "")
        .split("===")
    )
    content = content[2].replace("||", "|").split("|")[2:]
    mapping = {}
    for i in range(0, len(content) - 2, 3):
        mapping[content[i + 1].strip()] = content[i + 2]

    return mapping

def generate_tag(s="", mapping_list={}):
    mapping = mapping_list
    result = ""
    for discord_id, keyword in mapping.items():
        discord_id = discord_id.strip()
        keyword_list = [key.strip() for key in keyword.split(",")]
        if sum([key in s for key in keyword_list]):
            result += f" <@{discord_id}> "
    return result

def add_color(response):
    # add color to response
    color_response = ""
    is_new = response.split('\n')[0] == "[New Meeting !!]"
    if is_new:
        beg = 1
    else:
        beg = 0
    for line in response.split('\n'):
        if line == "":
            color_response += line + '\n'
        elif "---" in line or "+++" in line or "@@" in line :
            continue
        elif len(line) > 0 and line[0] == '-':  # red
            color_response += f"[2;31m{line[beg:]}[0m\n"
        elif len(line) > 0 and line[0] == '+':  # green
            color_response += f"[2;36m{line[beg:]}[0m\n"
        elif len(line) > 0 and line[0] == ',':  # blue
            color_response += f"[2;34m{line[beg:]}[0m\n"
        elif len(line) > 0 and line[0] == '.':  # shadow red
            color_response += f"[2;35m{line[beg:]}[0m\n"
        elif len(line) > 0 and line[0] == '!':  # yellow
            color_response += f"[2;33m{line[beg:]}[0m\n"
        else:
            color_response += line + '\n'
    return color_response

'''
    return f"""```ansi
[2;31m{tital}[0m  // red
==================
[2;32m[0m[2;34mDate: [0m  // blue
     [0;2m [0m[2;33m{date}[0m  // yellow
[2;32m[2;34mTime: [0m[2;32m[0m
      [2;35m{time}[0m  // shadow red
[2;32m[0m[2;34mDetail:[0m
      [2;36m{detail}[0m // green
```
Link: {link}
"""
'''
def get_latest_five_meeting_detail(
    url="https://mslab.csie.ntu.edu.tw/wiki", page="meeting_time"
):
    try:
        wiki = dokuwiki.DokuWiki(
            url, os.getenv("MSLAB_ACCOUNT"), os.getenv("MSLAB_PASSWORD")
        )
    except (dokuwiki.DokuWikiError, Exception) as err:
        print("unable to connect: %s" % err)
        return

    # wiki.pages.get(page): example
    # ====5/2 Meetings =====
    # |Thur 5/2 |10:00~14:00| Fundation_Pred (10:20), ICL(10:40), Mem_Gen_Ana&Learn(11:00)，prob_TA (12:00), Emer_LLM (13:30)  |https://meet.google.com/fpu-gijb-gem?authuser=1&hs=122&ijlm=1606109463391|
    # |Fri 5/3 |10:00~15:30| LLM_Rec(10:00), Emb_attack(10:20), slides (10:40) |https://meet.google.com/fpu-gijb-gem?authuser=1&hs=122&ijlm=1606109463391|

    # ====4/25 Meetings =====
    # |Thur 4/25 |10:00~14:00| Fundation_Pred (10:00), ICL(10:30),TA(11:00) ,  Emer_LLM (13:30)  |https://meet.google.com/fpu-gijb-gem?authuser=1&hs=122&ijlm=1606109463391|
    # |Fri 4/26 |10:00~15:30| LLM_Rec(9:40), Emb_attack(10:00), Emb_Rec+Graph_min (10:20), Mem_Gen_Ana&Learn(10:40), IL (11:10),  image (11:20) group meeting (12:20), |https://meet.google.com/fpu-gijb-gem?authuser=1&hs=122&ijlm=1606109463391|
    # 
    # ....
    content = (
        wiki.pages.get(page)
        .replace("=====", "===")
        .replace("====", "===")
        .replace("\n", "")
        .split("===")
    )
    # after processing, content is a list of string
    # ['',
    # '5/2 Meetings ',
    # '|Thur 5/2 |10:00~14:00| Fundation_Pred (10:20), ICL(10:40), Mem_Gen_Ana&Learn(11:00)，prob_TA (12:00), Emer_LLM (13:30)  |https://meet.google.com/fpu-gijb-gem?authuser=1&hs=122&ijlm=1606109463391||Fri 5/3 |10:00~15:30| LLM_Rec(10:00), Emb_attack(10:20), slides (10:40) |https://meet.google.com/fpu-gijb-gem?authuser=1&hs=122&ijlm=1606109463391|',
    # '4/25 Meetings ',
    # '|Thur 4/25 |10:00~14:00| Fundation_Pred (10:00), ICL(10:30),TA(11:00) ,  Emer_LLM (13:30)  |https://meet.google.com/fpu-gijb-gem?authuser=1&hs=122&ijlm=1606109463391||Fri 4/26 |10:00~15:30| LLM_Rec(9:40), Emb_attack(10:00), Emb_Rec+Graph_min (10:20), Mem_Gen_Ana&Learn(10:40), IL (11:10),  image (11:20) group meeting (12:20), |https://meet.google.com/fpu-gijb-gem?authuser=1&hs=122&ijlm=1606109463391|',
    # '4/18 Meetings ',
    # '|Thur 4/18 |10:00~14:00| Fundation_Pred (10:00), ICL(10:20), Mem_Gen_Ana&Learn(10:50), Emb_attack(11:20), LLM_Rec(11:40) Emer_LLM (13:30) |https://meet.google.com/fpu-gijb-gem?authuser=1&hs=122&ijlm=1606109463391|',
    # '4/11 Meetings ',
    # '|Thur 4/11 |10:00~14:00| Fundation_Pred (9:30), ICL(10:00), Emb_Rec+Graph_min (10:30),  image (10:50),  |https://meet.google.com/fpu-gijb-gem?authuser=1&hs=122&ijlm=1606109463391||Fri 4/12 |10:00~15:30| Mem_Gen_Ana&Learn(10:00), IL (10:40), group meeting (12:15),   Emer_LLM (13:30), Emb_attack(14:00), LLM_Rec(14:20)|https://meet.google.com/fpu-gijb-gem?authuser=1&hs=122&ijlm=1606109463391|',
    # '3/28 Meetings ',
    # ...
    result = {}
    for i in range(9, 0, -2):
        title = content[i].strip()
        result[title] = []
        elements = content[i + 1].replace("||", "| |").split("|")
        # assert elements = " " | Date | Time | Detail | Link | " " | Date | Time | Detail | Link | " " | ...
        for j in range(1, len(elements), 5):
            result[title].append({"date": elements[j].strip(), "time": elements[j + 1].strip(), "detail": elements[j + 2].strip(), "link": elements[j + 3].strip()})

    # return format:
    # {
    #     '5/2 Meetings': [
    #        {'date': '', 'time': '', 'detail': '', 'link': ''},
    #        {'date': '', 'time': '', 'detail': '', 'link': ''},
    #       ],
    # ...

    return result
