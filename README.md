# DiscordからPCやサーバーを起動させるbot

## 事前準備
- ライブラリのインストール
>pip install pings
>pip install discord
>pip install ConfigParser

- config.iniを準備
```
[settings]
# botのトークン
BOT_TOKEN = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# サーバーID(int型)
SERVER_ID = 000000000000000000
# 通知させるチャンネルのID
ALERT_CHANNEL = 0000000000000000000000
```
- ホスト名とIPアドレスとMACアドレスを配列に入れる(wol.py)
※Wake on LANの動作するMACアドレス

- ブロードキャストアドレスを入れる。(wol.py)

- Botを自分のサーバに入れる。

## 動作
- `!wol`でWake on LAN
- `!ping`でPing

## 注意
- 尋ねられてから10秒以内に答えないとタイムアウト


