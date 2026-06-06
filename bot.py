import os
import asyncio
import uvicorn

from pyrogram import Client, idle
print("PYROGRAM VERSION =", pyrogram.__version__)

from config import *
from database.db import init_db
from api.server import api

# Initialize DB
init_db()

# Pyrogram Client
# app = Client(
#     "elite_bot",
#     api_id=API_ID,
#     api_hash=API_HASH,
#     bot_token=BOT_TOKEN,
#     plugins=dict(root="plugins")
# )
app = Client(
    "elite_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins"),
    in_memory=True
)

async def start_services():

    # Start Telegram Bot
    await app.start()

    me = await app.get_me()

    print(f"✅ Bot Started: @{me.username}")

    # FastAPI Config
    config = uvicorn.Config(
        api,
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                8000
            )
        ),
        loop="asyncio"
    )

    server = uvicorn.Server(config)

    # Run API server in background
    api_task = asyncio.create_task(
        server.serve()
    )

    # Keep bot alive
    await idle()

    # Shutdown properly
    await app.stop()

    await api_task

asyncio.run(start_services())
