from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from config import ADMINS
from services.indexer import index_file
from core.security import encode_id

@Client.on_message(
    filters.private
    & filters.user(ADMINS)
    & filters.media
)
async def smart_handler(client, m):

    result = await index_file(client, m)

    bot = await client.get_me()

    if result[0] == "EXISTS":

        fid = result[1]

        link = (
            f"https://t.me/"
            f"{bot.username}"
            f"?start={encode_id(fid)}"
        )

        return await m.reply(
            "✅ Already Indexed",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔗 Get Link",
                        url=link
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🗑 Delete",
                        callback_data=f"del_{fid}"
                    )
                ]
            ])
        )

    elif result[0] == "INDEXED_CHANNEL":
        await m.reply("✅ Indexed")

    elif result[0] == "UPLOADED":
        await m.reply("🚀 Uploaded & Indexed")
