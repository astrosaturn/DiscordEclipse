import discord
from discord.ext import commands
import mariadb
import math
import time
import os 

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT")),
        database=os.getenv("DATABASE")
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")

cur = conn.cursor()

#Get a user's current XP
def get_user_xp(user_id: int):
    cur.execute(
            "SELECT current_xp FROM users WHERE user_id=?", (user_id,)
        )
    current_xp = cur.fetchone()
    current_xp = int(current_xp[0])    
    return current_xp

#Insert a user into the database
def initiate_user(user_id: int):
    cur.execute(
        "INSERT INTO users (user_id, level, current_xp, credits) VALUES (?, 1, 100, 0)", (user_id,))
    conn.commit()

#Check if a user ID currently exists in the database
def check_db_for_user(user_id: int):
    cur.execute(
            "SELECT user_id FROM users WHERE user_id=?", (user_id,)            
    )
    userid = cur.fetchone()
    
    if userid is not None:
        userid = int(userid[0])
        return userid
    else:
        return None

#Get the user's current level
def get_user_level(user_id: int):
    cur.execute(
            "SELECT level FROM users WHERE user_id=?", (user_id,)
        )
    level = cur.fetchone()
    level = int(level[0])
    return level

#Take the xp you want to add, and the user's id and add the XP to the user in the DB
def set_user_xp(xp_amount: int, user_id: int):
    cur.execute(
            "UPDATE users SET current_xp = ? WHERE user_id=?", (xp_amount, user_id,)
        )
    conn.commit()

#Change the level of the user to new_level
def level_set(new_level: int, user_id: int):
    cur.execute(
                "UPDATE users SET level=? WHERE user_id=?", (new_level, user_id,)                   
            )
    conn.commit()

#Add a user's xp together
def add_xp(xp_amount: int, user_id: int):
    cur_xp = get_user_xp(user_id=user_id)
    xp_to_give = cur_xp + xp_amount
    cur.execute(
        "UPDATE users SET current_xp = ? WHERE user_id=?", (xp_to_give, user_id,)
    )
    conn.commit()

