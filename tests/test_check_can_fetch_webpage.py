import discord
from discord.ext import tasks, commands
import aiocron
import os
from dotenv import load_dotenv
load_dotenv()
import dokuwiki

def test_check_can_fetch_webpage(url="https://mslab.csie.ntu.edu.tw/wiki", page="group_meeting"):
    try:
        wiki = dokuwiki.DokuWiki(
            url, os.getenv("MSLAB_ACCOUNT"), os.getenv("MSLAB_PASSWORD")
        )
    except (dokuwiki.DokuWikiError, Exception) as err:
        assert False

    content = wiki.pages.get(page)
    assert content != ""

