import time

from pyrogram import Client, filters

from database.db import connect
from config import ADMINS


# ---------------- FORCE SUB ---------------- #

@Client.on_message(
    filters.command("forceon")
    & filters.user(ADMINS)
)
async def force_on(client, m):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO settings
    (key,value)
    VALUES ('force','on')
    """)

    conn.commit()
    conn.close()

    await m.reply("✅ Force Subscribe Enabled")


@Client.on_message(
    filters.command("forceoff")
    & filters.user(ADMINS)
)
async def force_off(client, m):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO settings
    (key,value)
    VALUES ('force','off')
    """)

    conn.commit()
    conn.close()

    await m.reply("❌ Force Subscribe Disabled")


# ---------------- PREMIUM SYSTEM ---------------- #

@Client.on_message(
    filters.command("addpremium")
    & filters.user(ADMINS)
)
async def add_premium(client, m):

    try:
        user_id = int(m.command[1])
        plan = m.command[2].upper()
        days = int(m.command[3])

    except:
        return await m.reply(
            "Usage:\n"
            "/addpremium user_id plan days"
        )

    expiry = int(time.time()) + (days * 86400)

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO users
    (user_id,plan,expiry,used)
    VALUES (?,?,?,0)
    """, (
        user_id,
        plan,
        expiry
    ))

    conn.commit()
    conn.close()

    await m.reply(
        f"✅ {plan} added to {user_id}"
    )


@Client.on_message(
    filters.command("removepremium")
    & filters.user(ADMINS)
)
async def remove_premium(client, m):

    try:
        user_id = int(m.command[1])

    except:
        return await m.reply(
            "Usage:\n"
            "/removepremium user_id"
        )

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    DELETE FROM users
    WHERE user_id=?
    """, (user_id,))

    conn.commit()
    conn.close()

    await m.reply("❌ Premium Removed")


# ---------------- USER PLAN ---------------- #

@Client.on_message(
    filters.command("plan")
)
async def plan(client, m):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT plan,expiry
    FROM users
    WHERE user_id=?
    """, (m.from_user.id,))

    data = cur.fetchone()

    conn.close()

    if not data:
        return await m.reply(
            "🆓 FREE PLAN"
        )

    plan_name, expiry = data

    remain = expiry - int(time.time())

    days = remain // 86400

    await m.reply(
        f"💎 PLAN: {plan_name}\n"
        f"⏳ Remaining: {days} Days"
    )


# ---------------- STATS ---------------- #

@Client.on_message(
    filters.command("stats")
    & filters.user(ADMINS)
)
async def stats(client, m):

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM users"
    )

    users = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM files"
    )

    files = cur.fetchone()[0]

    conn.close()

    await m.reply(
        f"📊 BOT STATS\n\n"
        f"👤 Users: {users}\n"
        f"📂 Files: {files}"
    )


# ---------------- SYNC ---------------- #

@Client.on_message(
    filters.command("sync")
    & filters.user(ADMINS)
)
async def sync_channel(client, m):

    from services.indexer import index_file
    from config import CHANNEL_ID

    count = 0

    async for msg in client.get_chat_history(
        CHANNEL_ID,
        limit=500
    ):

        file = (
            msg.document
            or msg.video
            or msg.audio
        )

        if not file:
            continue

        result = await index_file(
            client,
            msg
        )

        if result[0] == "INDEXED_CHANNEL":
            count += 1

    await m.reply(
        f"✅ Synced {count} Files"
    )
