import time

cooldowns = {}

def check_cooldown(user_id, seconds=5):

    now = time.time()

    if user_id in cooldowns:

        if now - cooldowns[user_id] < seconds:
            return False

    cooldowns[user_id] = now

    return True
