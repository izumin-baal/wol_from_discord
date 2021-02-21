import discord
from datetime import datetime, timedelta

# 定義
# botのトークン
BOT_TOKEN = "*************************************"
# サーバーID(int型)
SERVER_ID = 000000000000
# 通知させるチャンネルのID
ALERT_CHANNEL = 00000000000
# 通話参加時のみ付与させるロールのID
ROLE_ID = 00000000
# 通知を除外させたいメンバーID(Rhythmとか)
EXCLUDE_ID = 000000000

client = discord.Client()

@client.event
async def on_message(message):
    if message.author.bot:
        return
    


client.run(BOT_TOKEN)
