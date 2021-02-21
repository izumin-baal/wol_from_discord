import discord
import sys
from configparser import ConfigParser
from datetime import datetime, timedelta

config = ConfigParser()
config.read('config.ini', encoding='utf-8')
""" config.iniの中身
[settings]
# botのトークン
BOT_TOKEN = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# サーバーID(int型)
SERVER_ID = 00000000000000000000000
# 通知させるチャンネルのID
ALERT_CHANNEL = 00000000000000000000000
HOST = {
    "MainPC": ["XX:XX:XX:XX:XX:AA", "XXX.XXX.XXX.1"],
    "Server1": ["XX:XX:XX:XX:XX:BB", "XXX.XXX.XXX.2"],
    "Server2": ["XX:XX:XX:XX:XX:CC", "XXX.XXX.XXX.3"]
}
"""

# botのトークン
BOT_TOKEN = str(config.get('settings', 'BOT_TOKEN'))
# サーバーID(int型)
SERVER_ID = int(config.get('settings', 'SERVER_ID'))
# 通知させるチャンネルのID
ALERT_CHANNEL = int(config.get('settings', 'ALERT_CHANNEL'))
# ホスト一覧
HOST = [
    ["MainPC", "XX:XX:XX:XX:XX:AA", "XXX.XXX.XXX.1"],
    ["Server1", "XX:XX:XX:XX:XX:BB", "XXX.XXX.XXX.2"],
    ["Server2", "XX:XX:XX:XX:XX:CC", "XXX.XXX.XXX.3"],
]

client = discord.Client()

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == '!wol':
        msg = ""
        error_flag = 0
        for num,value in enumerate(HOST):
            msg = msg + str(num + 1) + ": " + value[0] + "\n"
        reply_select = msg + "\n" + "Which? :"
        await message.channel.send(reply_select)
        def select(m):
            if m.content.isdecimal():
                if int(m.content) <= len(HOST) and int(m.content) > 0:
                    return m.channel == message.channel and m.author != client.user
                else:
                    return False
            else:
                return False
        try:
            select_result = await client.wait_for('message', check=select, timeout=10.0)
        except:
            await message.channel.send("Timeout...")
            error_flag = 1
        else:
            await message.channel.send("OK\nsend wol(" + HOST[int(select_result.content)-1][1] + ")\nThis device IP address is " + HOST[int(select_result.content)-1][2])


    if message.content == '!dis':
        sys.exit()
        


client.run(BOT_TOKEN)