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

    mapping_list = get_tag_keyword_list()
    content = (
        wiki.pages.get(page)
        .replace("=====", "===")
        .replace("====", "===")
        .replace("\n", "")
        .split("===")
    )
    result = {}
    for i in range(9, 0, -2):
        title = content[i].strip()
        elements = content[i + 1].replace("||", "| |").split("|")
        detail = ""
        detail += title + "\n"
        detail += "==================" + "\n"
        detail_with_tag = str(detail)

        for element in elements:
            if element != "":
                detail += element.strip() + "\n"
                detail_with_tag += element.strip() + "\n"

                tag = generate_tag(s=element.strip(), mapping_list=mapping_list)
                if tag != "":
                    detail_with_tag += tag + "\n"

                detail += "---" + "\n"
                detail_with_tag += "---" + "\n"

        result[title] = {"detail_with_tag": detail_with_tag, "detail": detail}

    return result
