import processing_message.openaiapi as openaiapi
from processing_message.record import GetRecord, SaveRecord

def get_reply(message):
    # get user id or group id as user id
    channel_id = message.channel.id
    # replace mention to bot name
    message.content = message.content.replace("@MSLAB Discord bot", "SD").replace("@MSLAB Meeting Time", "SD")
    # get record
    history = GetRecord(channel_id)
    now = {"role":"user", "content": message.content}
    # connect api
    response = openaiapi.ChatCompletion(history + [now])
    # save record
    SaveRecord(channel_id, [now] + [response])

    return response.content