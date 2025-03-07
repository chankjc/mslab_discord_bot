import logging
import logging.handlers
import os
import random
import time

import aiocron
import arrow
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

import addemoji.addemoji as ae
import check_server_status.check_server_status as css
import papergpt.papergpt as pg
import processing_message.processing_message as pm
from check_meeting_time import cmt
from database import db

load_dotenv()

logger_meeting_time = logging.getLogger("meeting_time")
logger_meeting_time.setLevel(logging.DEBUG)

meeting_time_log_file = "./log/latest_check_for_meeting_time.txt"
handler = logging.handlers.RotatingFileHandler(
    f"{meeting_time_log_file}", maxBytes=1000, backupCount=5
)
logger_meeting_time.addHandler(handler)


class cronjobs:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.interval = os.getenv("INTERVAL")

        @aiocron.crontab(f"*/{self.interval} * * * *")
        async def CheckMeetingTime():
            change = False

            logger_meeting_time.info(f"Update time : {arrow.now()} \n\n")
            # get latest webpage
            results = cmt.get_latest_five_meeting_detail()
            tag_mapping = cmt.get_tag_keyword_list()

            for title, contents in results.items():
                response = db.check_and_set_Meeting_data(
                    os.getenv("DISCORD_MEETINGTIME_NOTIFICATION_CHANNEL"), title, contents
                )
                logger_meeting_time.info(f"Title : {title}\n")
                # logger_meeting_time.info(f"Contents : {contents}\n")
                # logger_meeting_time.info(f"Response : {response}\n")
                # If the response is not None, it means that the meeting is new or updated
                # add color, add tag
                # else, response is None
                if response:
                    response = cmt.add_color(response)
                    tag = cmt.generate_tag(response, mapping_list = tag_mapping)
                    response = tag + "\n" + response + "\n"

                    logger_meeting_time.info(f"\n  ===> {title} update !\n")                    
                    if int(os.getenv("NOTIFY")):
                        channel = client.get_channel(int(os.getenv("DISCORD_MEETINGTIME_NOTIFICATION_CHANNEL")))
                        await channel.send(response)
                    change = True
                else:
                    logger_meeting_time.info(f" ==> No change !\n")

            logger_meeting_time.info("update finish !!\n")

            if change:
                os.system(
                    f"cp ./log/latest_check_for_meeting_time.txt ./log/{arrow.now()}_check_for_meeting_time.txt"
                )


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
    # await message.channel.typing()

    # reply = pm.get_reply(message)
    # if reply != None:
    #     await message.channel.send(reply)


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
