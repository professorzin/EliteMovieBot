import time
from database.db import connect

PLANS = {
    "FREE": 3,
    "SILVER": 10,
    "GOLD": 50,
    "PREMIUM": 999999
}


def get_plan(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT plan, expiry, used
    FROM users
    WHERE user_id=?
    """, (user_id,))

    data = cur.fetchone()

    conn.close()

    if not data:
        return "FREE", 0, 0

    plan, expiry, used = data

    # Premium expired
    if expiry and expiry < int(time.time()):
        return "FREE", 0, used

    return plan, expiry, used


def can_use(user_id):

    plan, _, used = get_plan(user_id)

    limit = PLANS.get(plan, 3)

    return used < limit


def increase_usage(user_id):

    conn = connect()
    cur = conn.cursor()

    # Create FREE user if not exists
    cur.execute("""
    INSERT OR IGNORE INTO users
    (user_id, plan, expiry, used)
    VALUES (?, 'FREE', 0, 0)
    """, (user_id,))

    cur.execute("""
    UPDATE users
    SET used = used + 1
    WHERE user_id=?
    """, (user_id,))

    conn.commit()
    conn.close()


def reset_usage(user_id):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    UPDATE users
    SET used = 0
    WHERE user_id=?
    """, (user_id,))

    conn.commit()
    conn.close()









# import time
# from database.db import connect

# PLANS = {
#     "FREE": 3,
#     "SILVER": 10,
#     "GOLD": 50,
#     "PREMIUM": 999999
# }

# def get_plan(user_id):

#     conn = connect()
#     cur = conn.cursor()

#     cur.execute("""
#     SELECT plan,expiry,used
#     FROM users
#     WHERE user_id=?
#     """, (user_id,))

#     data = cur.fetchone()

#     conn.close()

#     if not data:
#         return "FREE", 0, 0

#     plan, expiry, used = data

#     if expiry and expiry < int(time.time()):
#         return "FREE", 0, 0

#     return plan, expiry, used


# def can_use(user_id):

#     plan, _, used = get_plan(user_id)

#     limit = PLANS.get(plan, 3)

#     return used < limit


# def increase_usage(user_id):

#     conn = connect()
#     cur = conn.cursor()

#     cur.execute("""
#     UPDATE users
#     SET used = used + 1
#     WHERE user_id=?
#     """, (user_id,))

#     conn.commit()
#     conn.close()
