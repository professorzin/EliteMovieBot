from pyrogram import Client, filters

from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database.db import connect
from config import RESULTS_PER_PAGE

from services.limiter import (
    check_cooldown
)


def build_results(query, page):

    conn = connect()
    cur = conn.cursor()

    query = "%" + " ".join(
        query.split()
    ) + "%"

    cur.execute("""
    SELECT id,file_name
    FROM files
    WHERE file_name LIKE ?
    LIMIT ?
    OFFSET ?
    """, (
        query,
        RESULTS_PER_PAGE,
        page * RESULTS_PER_PAGE
    ))

    data = cur.fetchall()

    conn.close()

    if not data:
        return None

    buttons = [
        [
            InlineKeyboardButton(
                name[:50],
                callback_data=f"file_{fid}"
            )
        ]
        for fid, name in data
    ]

    return InlineKeyboardMarkup(buttons)


@Client.on_message(
    filters.text
    & ~filters.command(["start"])
)
async def search(client, m):

    # 🚫 Anti Spam Cooldown
    if not check_cooldown(
        m.from_user.id
    ):
        return await m.reply(
            "⏳ Slow down..."
        )

    kb = build_results(
        m.text,
        0
    )

    if not kb:
        return await m.reply(
            "❌ No Results"
        )

    await m.reply(
        "🔎 Search Results",
        reply_markup=kb
    )
