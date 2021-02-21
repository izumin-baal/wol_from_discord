import discord
import sys
import time
import pings
import socket
import struct
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
HOST = [
    ["MainPC", "XX:XX:XX:XX:XX:AA", "XXX.XXX.1"],
    ["Server1", "XX:XX:XX:XX:XX:BB", "XXX.XXX.XXX.2"],
    ["Server2", "XX:XX:XX:XX:XX:CC", "XXX.XXX.XXX.3"],
]
"""

# botのトークン
BOT_TOKEN = str(config.get('settings', 'BOT_TOKEN'))
# サーバーID(int型)
SERVER_ID = int(config.get('settings', 'SERVER_ID'))
# 通知させるチャンネルのID
ALERT_CHANNEL = int(config.get('settings', 'ALERT_CHANNEL'))
# ホスト一覧
HOST = [
    ["MainPC", "XX:XX:XX:XX:XX:AA", "XXX.XXX.1"],
    ["Server1", "XX:XX:XX:XX:XX:BB", "XXX.XXX.XXX.2"],
    ["vyos", "XX:XX:XX:XX:XX:BB", "XXX.XXX.XXX.3"],
]
# WoLするセグメントのブロードキャストアドレス
BROADCAST = "XXX.XXX.XXX.XXX"

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

        def send_magic_packet(addr):
            DEFAULT_PORT = 7
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                mac = addr.upper().replace("-", "").replace(":", "")
                buf = b'f' * 12 + (mac * 20).encode()
                magicp = b''
                for i in range(0, len(buf), 2):
                    magicp += struct.pack('B', int(buf[i:i + 2], 16))
                s.sendto(magicp, (BROADCAST, DEFAULT_PORT))

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
            MACaddress = HOST[int(select_result.content)-1][1]
            IPaddress = HOST[int(select_result.content)-1][2]
            await message.channel.send("OK\nsend wol(" + MACaddress + ")\nThis device IP address is " + IPaddress)
        if error_flag != 1:
            send_magic_packet(MACaddress)
            ping_result = 0
            for i in range(6):
                time.sleep(30)
                await message.channel.send("ping...")
                ping = pings.Ping()
                response = ping.ping(IPaddress)
                if response.is_reached():
                    ping_result = 1
                    await message.channel.send("Success!")
                    break
                else:
                    await message.channel.send("unreachable...")
            if ping_result == 1:
                await message.channel.send(f"{message.author.mention}\n:green_circle: Active")
            else:
                await message.channel.send(f"{message.author.mention}\n:red_circle: disabled")

client.run(BOT_TOKEN)