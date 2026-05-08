import asyncio
import uvicorn

from pyrogram import Client

from config import *
from database.db import init_db
from api.server import api

init_db()

app = Client(
    "elite_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

async def main():

    await app.start()

    config = uvicorn.Config(
        api,
        host="0.0.0.0",
        port=8000
    )

    server = uvicorn.Server(config)

    await server.serve()

asyncio.run(main())
