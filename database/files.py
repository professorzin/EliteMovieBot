from database.db import connect

def get_file(fid):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT chat_id,message_id,file_name
    FROM files
    WHERE id=?
    """, (fid,))

    r = cur.fetchone()

    conn.close()
    return r


def get_by_unique(unique_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT id,chat_id,message_id,file_name
    FROM files
    WHERE file_unique_id=?
    """, (unique_id,))

    r = cur.fetchone()

    conn.close()
    return r


def insert_file(chat_id, message_id, name, unique_id):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO files
    (chat_id,message_id,file_name,file_unique_id)
    VALUES (?,?,?,?)
    """, (chat_id, message_id, name, unique_id))

    conn.commit()
    conn.close()
