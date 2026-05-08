from database.db import connect

def get_user(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT *
    FROM users
    WHERE user_id=?
    """, (user_id,))

    data = cur.fetchone()

    conn.close()

    return data
