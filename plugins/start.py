from pyrogram import Client, filters

from core.security import decode_id
from database.files import get_file

@Client.on_message(
    filters.command("start")
)
async def start(client, m):

    if len(m.command) > 1:

        fid = decode_id(
            m.command[1]
        )

        if not fid:
            return await m.reply(
                "❌ Invalid Link"
            )

        f = get_file(fid)

        if not f:
            return await m.reply(
                "❌ File Missing"
            )

        await client.copy_message(
            m.chat.id,
            f[0],
            f[1]
        )

        return

    text = (
        "🚀 ELITE MOVIE BOT\n\n"
        "🔎 Send movie name to search.\n"
        "💎 Premium Plans Available."
    )

    await m.reply(text)
