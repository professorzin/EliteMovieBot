import asyncio

from pyrogram import Client, filters

from database.files import get_file

from core.membership import (
    can_use,
    increase_usage
)

from core.force_sub import check_sub

from config import AUTO_DELETE_TIME

@Client.on_callback_query(
    filters.regex("^file_")
)
async def send_file(client, q):

    if not await check_sub(
        client,
        q.from_user.id
    ):
        return await q.answer(
            "🚫 Join required channels",
            show_alert=True
        )

    if not can_use(q.from_user.id):
        return await q.answer(
            "❌ Daily limit reached",
            show_alert=True
        )

    fid = int(
        q.data.split("_")[1]
    )

    f = get_file(fid)

    if not f:
        return await q.answer("Missing")

    msg = await client.copy_message(
        q.message.chat.id,
        f[0],
        f[1]
    )

    increase_usage(q.from_user.id)

    await asyncio.sleep(
        AUTO_DELETE_TIME
    )

    await msg.delete()
