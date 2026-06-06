print("DEBUG FILE VERSION 999")
from pyrogram import Client, filters

print("debug.py loaded")

@Client.on_message(filters.all)
async def debug(client, message):
    print("UPDATE RECEIVED")
    print(message)
    print("DEBUG FILE VERSION 999")

@Client.on_message()
async def debug(client, message):
    print("UPDATE RECEIVED:", message.text)
