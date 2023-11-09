import discord
from discord.ext import tasks, commands
import aiocron
import arrow
import os
import time
import logging
import logging.handlers
import random

logger_meeting_time = logging.getLogger("meeting_time")
logger_meeting_time.setLevel(logging.DEBUG)

meeting_time_log_file = "./log/latest_check_for_meeting_time.txt"
handler = logging.handlers.RotatingFileHandler(
    f"{meeting_time_log_file}", maxBytes=1000, backupCount=5
)
logger_meeting_time.addHandler(handler)

from dotenv import load_dotenv

load_dotenv()

import check_meeting_time.check_meeting_time as cmt
import check_server_status.check_server_status as css
import processing_message.processing_message as pm
import database.database as db
import papergpt.papergpt as pg
import addemoji.addemoji as ae

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
                    os.getenv("DISCORD_MEETINGTIME_NOTIFICATION_CHANNEL"), title, content["detail"]
                )
                logger_meeting_time.info(f"check title : {title}")
                if response != "":
                    logger_meeting_time.info(f"\n  ===> {title} update !\n")

                    if int(os.getenv("NOTIFY")):
                        channel = client.get_channel(int(os.getenv("DISCORD_MEETINGTIME_NOTIFICATION_CHANNEL")))
                        await channel.send(content["detail_with_tag"])
                    change = True
                else:
                    logger_meeting_time.info(f" ==> No change !\n")

            logger_meeting_time.info("update finish !!\n")

            if change:
                os.system(
                    f"cp ./log/latest_check_for_meeting_time.txt ./log/{arrow.now()}_check_for_meeting_time.txt"
                )
        

        @aiocron.crontab(f"* * * * *")
        async def CheckServerState():
            channel = bot.get_channel(int(os.getenv("DISCORD_SERVER_STATE_CHANNEL")))
            
            message = await channel.fetch_message(int(os.getenv("DISCORD_SERVER_STATE_CHANNEL_MESSAGE_Joule_cuda6")))
            await message.edit(content=css.update_status())
            time.sleep(6)

            message = await channel.fetch_message(int(os.getenv("DISCORD_SERVER_STATE_CHANNEL_MESSAGE_Hulk")))
            cmd = "ssh Hulk bash < ./workstation/nv.sh  > ./log/hulk_gpu.log"
            os.system(cmd)
            result = "error!"
            with open("./log/hulk_gpu.log", "r") as f:
                result = f.read()
            await message.edit(content=result)
            time.sleep(6)

            message = await channel.fetch_message(int(os.getenv("DISCORD_SERVER_STATE_CHANNEL_MESSAGE_Turing")))
            cmd = "ssh Turing bash < ./workstation/nv.sh  > ./log/turing_gpu.log"
            os.system(cmd)
            result = "error!"
            with open("./log/turing_gpu.log", "r") as f:
                result = f.read()
            await message.edit(content=result)
            time.sleep(6)

            message = await channel.fetch_message(int(os.getenv("DISCORD_SERVER_STATE_CHANNEL_MESSAGE_Turing_1")))
            cmd = "ssh Turing bash < ./workstation/nv_1.sh  > ./log/turing_1_gpu.log"
            os.system(cmd)
            result = "error!"
            with open("./log/turing_1_gpu.log", "r") as f:
                result = f.read()
            await message.edit(content=result)
            time.sleep(6)
            
            message = await channel.fetch_message(int(os.getenv("DISCORD_SERVER_STATE_CHANNEL_MESSAGE_Leibniz")))
            cmd = "ssh Leibniz bash < ./workstation/nv.sh  > ./log/leibniz_gpu.log"
            os.system(cmd)
            result = "error!"
            with open("./log/leibniz_gpu.log", "r") as f:
                result = f.read()
            await message.edit(content=result)
            time.sleep(6)

            message = await channel.fetch_message(int(os.getenv("DISCORD_SERVER_STATE_CHANNEL_MESSAGE_Leibniz_1")))
            cmd = "ssh Leibniz bash < ./workstation/nv_1.sh  > ./log/leibniz_1_gpu.log"
            os.system(cmd)
            result = "error!"
            with open("./log/leibniz_1_gpu.log", "r") as f:
                result = f.read()
            await message.edit(content=result)
            time.sleep(6)

class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="%", intents=intents, help_command=None)

    async def setup_hook(self):
        cron = cronjobs(self)

    async def close(self):
        await super().close()


client = DiscordBot()


@client.event
async def on_ready():
    await client.tree.sync()
    await client.change_presence(status=discord.Status.online, activity=activity)
    print(f"{client.user} login in")


# https://discordpy.readthedocs.io/en/stable/api.html#discord.Message
@client.event
async def on_message(message):
    await client.process_commands(message)
    # emoji = ae.emoji_response(message.content)
    # if emoji:
    #    await message.add_reaction(emoji)
    if message.author == client.user:
        return
    if client.user.id not in [member.id for member in message.mentions]:
        return

    # sent typing status
    await message.channel.typing()

    reply = pm.get_reply(message)
    if reply != None:
        await message.channel.send(reply)


"""
@client.command()
async def send(ctx, channel_id, *msg):
    channel = client.get_channel(int(channel_id))
    await channel.send(" ".join(msg))
"""


@client.tree.command(name="send", description="send message, [channel id] [*message]")
async def send(interaction: discord.Interaction, channel_id: str, msg: str):
    try:
        await interaction.response.send_message()
    except:
        pass
    channel = client.get_channel(int(channel_id))
    await channel.send(msg)
    

@client.tree.command(name="edit", description="Edit message, [channel id] [message id] [*message]")
async def send(interaction: discord.Interaction, channel_id: str, msg_id:str, msg: str):
    try:
        await interaction.response.send_message()
    except:
        pass
    channel = client.get_channel(int(channel_id))
    message = await channel.fetch_message(int(msg_id))
    await message.edit(content=msg)
    

@client.tree.command(name="react", description="Add reaction, [channel id] [message id] [emoji]")
async def react(interaction: discord.Interaction, channel_id: str, msg_id:str, emoji: str):
    try:
        await interaction.response.send_message()
    except:
        pass
    channel = client.get_channel(int(channel_id))
    message = await channel.fetch_message(int(msg_id))
    await message.add_reaction(emoji)
    

@client.tree.command(name="papergpt", description="MSLAB PaperGPT, [*input]")
async def papergpt(interaction: discord.Interaction, input: str):
    try:
        await interaction.response.send_message()
    except:
        pass
    channel = client.get_channel(int(interaction.channel_id))
    resp = pg.gen_papergpt_response(input)
    await channel.send(resp)
    
@client.tree.command(name = "join", description="Join voice channel")
async def join(interaction: discord.Interaction, index: int):
    try:
        await interaction.response.send_message()
    except:
        pass
    channel = interaction.guild.voice_channels[index]
    if client.voice_clients:
        await client.voice_clients[0].move_to(channel)
    else:
        await channel.connect()
    

@client.tree.command(name="leave", description="Leave voice channel")
async def leave(interaction: discord.Interaction):
    try:
        await interaction.response.send_message()
    except:
        pass
    voice_clients = client.voice_clients[0]
    await voice_clients.disconnect()
    
@client.tree.command(name="sync", description="Sync command")
async def sync(interaction: discord.Interaction):
    try:
        await interaction.response.send_message("Sync success!")
    except:
        pass
    await client.tree.sync()


    

client.run(os.getenv("DISCORD_BOT_TOKEN"))
