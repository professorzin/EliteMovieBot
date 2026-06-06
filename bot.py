import os
import asyncio
import logging
import uvicorn
import pyrogram

from pyrogram import Client, idle

print("PYROGRAM VERSION =", pyrogram.__version__)

logging.basicConfig(level=logging.INFO)

from config import *
from database.db import init_db
from api.server import api

# Initialize Database
init_db()

# Pyrogram Client
app = Client(
    name="elite_bot_v2",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins"),
    in_memory=True
)


async def start_services():
    try:
        print("Starting Pyrogram...")

        await app.start()

        me = await app.get_me()

        print(f"✅ Bot Started: @{me.username}")

        # Diagnostic
        try:
            dialogs = []

            async for dialog in app.get_dialogs():
                dialogs.append(dialog)

            print(f"📨 Dialog Count: {len(dialogs)}")

        except Exception as e:
            print("❌ Dialog Check Error:", repr(e))

        # FastAPI Server
        config = uvicorn.Config(
            api,
            host="0.0.0.0",
            port=int(os.environ.get("PORT", 8000)),
            loop="asyncio",
            log_level="info"
        )

        server = uvicorn.Server(config)

        api_task = asyncio.create_task(
            server.serve()
        )

        print("🚀 Services Running")

        # Keep Bot Alive
        await idle()

        print("🛑 Stopping Bot")

        await app.stop()

        await api_task

    except Exception as e:
        print("❌ STARTUP ERROR:", repr(e))
        raise


if __name__ == "__main__":
    asyncio.run(start_services())












# import os
# import asyncio
# import uvicorn
# import pyrogram

# from pyrogram import Client, idle
# print("PYROGRAM VERSION =", pyrogram.__version__)

# from config import *
# from database.db import init_db
# from api.server import api

# # Initialize DB
# init_db()

# # Pyrogram Client
# # app = Client(
# #     "elite_bot",
# #     api_id=API_ID,
# #     api_hash=API_HASH,
# #     bot_token=BOT_TOKEN,
# #     plugins=dict(root="plugins")
# # )
# app = Client(
#     "elite_bot",
#     api_id=API_ID,
#     api_hash=API_HASH,
#     bot_token=BOT_TOKEN,
#     plugins=dict(root="plugins"),
#     in_memory=True
# )

# async def start_services():

#     # Start Telegram Bot
#     await app.start()

#     me = await app.get_me()

#     print(f"✅ Bot Started: @{me.username}")

#     # FastAPI Config
#     config = uvicorn.Config(
#         api,
#         host="0.0.0.0",
#         port=int(
#             os.environ.get(
#                 "PORT",
#                 8000
#             )
#         ),
#         loop="asyncio"
#     )

#     server = uvicorn.Server(config)

#     # Run API server in background
#     api_task = asyncio.create_task(
#         server.serve()
#     )

#     # Keep bot alive
#     await idle()

#     # Shutdown properly
#     await app.stop()

#     await api_task

# asyncio.run(start_services())
