from database.db import connect

def set_setting(key, value):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO settings
    (key,value)
    VALUES (?,?)
    """, (key, value))

    conn.commit()
    conn.close()


def get_setting(key):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT value
    FROM settings
    WHERE key=?
    """, (key,))

    data = cur.fetchone()

    conn.close()

    if not data:
        return None

    return data[0]
