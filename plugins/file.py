import asyncio

from pyrogram import Client, filters

from database.files import get_file

from core.membership import (
    can_use,
    increase_usage
)

from core.force_sub import check_sub

from config import AUTO_DELETE_TIME


async def auto_delete(msg):
    try:
        await asyncio.sleep(AUTO_DELETE_TIME)
        await msg.delete()
    except:
        pass


@Client.on_callback_query(
    filters.regex(r"^file_\d+$")
)
async def send_file(client, q):

    # Force Subscribe Check
    if not await check_sub(
        client,
        q.from_user.id
    ):
        return await q.answer(
            "🚫 Join required channels first",
            show_alert=True
        )

    # Premium / Daily Limit Check
    if not can_use(q.from_user.id):
        return await q.answer(
            "❌ Daily limit reached",
            show_alert=True
        )

    try:
        fid = int(
            q.data.split("_")[1]
        )

    except:
        return await q.answer(
            "❌ Invalid file",
            show_alert=True
        )

    f = get_file(fid)

    if not f:
        return await q.answer(
            "❌ File not found",
            show_alert=True
        )

    try:

        msg = await client.copy_message(
            chat_id=q.message.chat.id,
            from_chat_id=f[0],
            message_id=f[1]
        )

        increase_usage(
            q.from_user.id
        )

        await q.answer(
            "✅ File sent"
        )

        # Background auto delete
        asyncio.create_task(
            auto_delete(msg)
        )

    except Exception as e:

        print(
            "SEND_FILE_ERROR:",
            e
        )

        await q.answer(
            "❌ Failed to send file",
            show_alert=True
        )




# import asyncio

# from pyrogram import Client, filters

# from database.files import get_file

# from core.membership import (
#     can_use,
#     increase_usage
# )

# from core.force_sub import check_sub

# from config import AUTO_DELETE_TIME

# @Client.on_callback_query(
#     filters.regex("^file_")
# )
# async def send_file(client, q):

#     if not await check_sub(
#         client,
#         q.from_user.id
#     ):
#         return await q.answer(
#             "🚫 Join required channels",
#             show_alert=True
#         )

#     if not can_use(q.from_user.id):
#         return await q.answer(
#             "❌ Daily limit reached",
#             show_alert=True
#         )

#     fid = int(
#         q.data.split("_")[1]
#     )

#     f = get_file(fid)

#     if not f:
#         return await q.answer("Missing")

#     msg = await client.copy_message(
#         q.message.chat.id,
#         f[0],
#         f[1]
#     )

#     increase_usage(q.from_user.id)

#     await asyncio.sleep(
#         AUTO_DELETE_TIME
#     )

#     await msg.delete()
