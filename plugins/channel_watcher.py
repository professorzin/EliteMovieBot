from pyrogram import Client, filters
from services.indexer import index_file
from config import CHANNEL_ID

@Client.on_message(
    filters.chat(CHANNEL_ID)
    & filters.media
)
async def auto_index(client, m):

    await index_file(client, m)
