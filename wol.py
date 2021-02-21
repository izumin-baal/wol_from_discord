import discord
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
"""

# botのトークン
BOT_TOKEN = str(config.get('settings', 'BOT_TOKEN'))
# サーバーID(int型)
SERVER_ID = int(config.get('settings', 'SERVER_ID'))
# 通知させるチャンネルのID
ALERT_CHANNEL = int(config.get('settings', 'ALERT_CHANNEL'))

client = discord.Client()

@client.event
async def on_message(message):
    if message.author.bot:
        return
    


client.run(BOT_TOKEN)