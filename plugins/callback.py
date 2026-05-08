from pyrogram import Client, filters
from database.db import connect

@Client.on_callback_query(
    filters.regex("^del_")
)
async def delete_file(client, q):

    fid = int(
        q.data.split("_")[1]
    )

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    DELETE FROM files
    WHERE id=?
    """, (fid,))

    conn.commit()
    conn.close()

    await q.message.edit_text(
        "🗑 Deleted"
    )
