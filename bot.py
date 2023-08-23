import discord
from discord.ext import tasks, commands
import aiocron
import arrow
import os
import logging
import logging.handlers

logger_meeting_time = logging.getLogger('meeting_time')
logger_meeting_time.setLevel(logging.DEBUG)

meeting_time_log_file = "./log/latest_check_for_meeting_time.txt"
handler = logging.handlers.RotatingFileHandler(f"{meeting_time_log_file}", maxBytes=1000, backupCount=5)
logger_meeting_time.addHandler(handler)

from dotenv import load_dotenv
load_dotenv()

import check_meeting_time.check_meeting_time as cmt
import database.database as db

class cronjobs:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.interval = os.getenv("INTERVAL")

        @aiocron.crontab(f"*/{self.interval} * * * *")
        async def CheckMeetingTime():
            change = False

            logger_meeting_time.info(f"Update time : {arrow.now()} \n\n")
            # get latest webpage
            result = cmt.get_latest_five_meeting_detail()

            for title, content in result.items():
                response = db.check_and_set_Meeting_data(
                    os.getenv("DISCORD_CHANNEL"), title, content['detail']
                )
                logger_meeting_time.info(f"check title : {title}")
                if response != "":
                    logger_meeting_time.info(f"\n  ===> {title} update !\n")

                    if int(os.getenv("NOTIFY")):
                        channel = client.get_channel(int(os.getenv("DISCORD_CHANNEL")))
                        await channel.send(content['detail_with_tag'])
                    change = True
                else:
                    logger_meeting_time.info(f" ==> No change !\n")

            logger_meeting_time.info("update finish !!\n")
            
            if change:
                os.system(f"cp ./log/latest_check_for_meeting_time.txt ./log/{arrow.now()}_check_for_meeting_time.txt")


class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents, help_command=None)

    async def setup_hook(self):
        cron = cronjobs(self)

    async def close(self):
        await super().close()


client = DiscordBot()


@client.event
async def on_ready():
    activity = discord.Activity(
        type=discord.ActivityType.watching, name="MSLAB meeting time"
    )
    await client.change_presence(status=discord.Status.online, activity=activity)
    print(f"{client.user} login in")


client.run(os.getenv("DISCORD_BOT_TOKEN"))
