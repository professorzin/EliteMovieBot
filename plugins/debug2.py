from pyrogram import Client, filters

print("debug2.py loaded")

@Client.on_message(filters.private)
async def private_debug(client, message):
    print("PRIVATE MESSAGE:", message.text)
