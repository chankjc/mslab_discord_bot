import discord
from discord.ext import tasks, commands
import aiocron
import time
import os
from dotenv import load_dotenv
load_dotenv()

import dokuwiki
import check_meeting_time
import database


def check_webpage(url = "https://mslab.csie.ntu.edu.tw/wiki", page = "group_meeting"):
    try:
        wiki = dokuwiki.DokuWiki(url, os.getenv("MSLAB_ACCOUNT"), os.getenv("MSLAB_PASSWORD"))
    except (dokuwiki.DokuWikiError, Exception) as err:
        print('unable to connect: %s' % err)
        return

    content = wiki.pages.get(page)
    print(content)
