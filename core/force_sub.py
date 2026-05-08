from config import FORCE_SUB_CHANNELS
from database.db import connect

def force_enabled():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT value
    FROM settings
    WHERE key='force'
    """)

    r = cur.fetchone()

    conn.close()

    return r and r[0] == "on"


async def check_sub(client, user_id):

    if not force_enabled():
        return True

    for ch in FORCE_SUB_CHANNELS:

        try:
            member = await client.get_chat_member(
                ch,
                user_id
            )

            if member.status in ["left", "kicked"]:
                return False

        except:
            return False

    return True
