import discord
from discord.ext import tasks, commands
import aiocron
import time
import os
from dotenv import load_dotenv
load_dotenv()

import check_meeting_time
import database

class cronjobs():
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.interval = os.getenv("INTERVAL")
        
        @aiocron.crontab(f"*/{self.interval} * * * *")
        async def CheckMeetingTime():
            change = False
            # log file
            os.system(f"echo \"\" > ./log/temp.txt")
            f = open("./log/temp.txt","a")
            f.write(f"Update time : {time.asctime( time.localtime(time.time()) )} \n\n")
            # get latest webpage
            result = check_meeting_time.get_latest_five_meeting_detail()
            
            for title, content in result.items():
                response = database.check_and_set_Meeting_data(os.getenv("DISCORD_CHANNEL"), title, content )
                f.write(f"check title : {title}")
                if response != "":
                    f.write(f"\n  ===> {title} update !\n")
                    
                    if int(os.getenv("NOTIFY")):
                        channel = client.get_channel(int(os.getenv("DISCORD_CHANNEL")))
                        await channel.send(response)
                    change = True
                else:
                    f.write(f" ==> No change !\n")

            f.write("update finish !!\n")
            f.close()
            if change:
                os.system(f"cp ./log/temp.txt ./log/{time.time()}")
            
class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents = intents,  help_command=None)

    async def setup_hook(self):
        cron = cronjobs(self)

    async def close(self):
        await super().close()

client = DiscordBot()

@client.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="MSLAB meeting time")
    await client.change_presence(status = discord.Status.online, activity = activity)
    print(f"{client.user} login in")

client.run(os.getenv("DISCORD_BOT_TOKEN"))
