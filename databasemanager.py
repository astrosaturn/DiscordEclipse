import discord
from discord.ext import commands
import mariadb
import math
import time
import os 
from datetime import datetime, timedelta

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

#Insert a user into the database
def initiate_user(user_id: int):
    cur.execute(
        "INSERT INTO users (user_id, level, current_xp, credits, daily_cooldown, theft_cooldown) VALUES (?, 1, 0, 0, 0, 0)", (user_id,))
    conn.commit()

#Get a user's current XP
def get_user_xp(user_id: int):
    querey_user = check_db_for_user(user_id)
    if querey_user is None:
        initiate_user(user_id=user_id) 

    cur.execute(
            "SELECT current_xp FROM users WHERE user_id=?", (user_id,)
        )
    current_xp = cur.fetchone()
    current_xp = int(current_xp[0])    
    return current_xp


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
    querey_user = check_db_for_user(user_id)
    if querey_user is None:
        initiate_user(user_id=user_id) 
 
    cur.execute(
            "SELECT level FROM users WHERE user_id=?", (user_id,)
        )
    level = cur.fetchone()
    return level

#Take the xp you want to add, and the user's id and add the XP to the user in the DB
def set_user_xp(xp_amount: int, user_id: int):    
    querey_user = check_db_for_user(user_id)
    if querey_user is None:
        initiate_user(user_id=user_id) 
                    
    cur.execute(
            "UPDATE users SET current_xp = ? WHERE user_id=?", (xp_amount, user_id,)
        )
    conn.commit()    

#Change the level of the user to new_level
def level_set(new_level: int, user_id: int):
    querey_user = check_db_for_user(user_id)
    if querey_user is None:
        initiate_user(user_id=user_id) 

    cur.execute(
            "UPDATE users SET level=? WHERE user_id=?", (new_level, user_id,)                   
        )
    conn.commit()

#Add a user's xp together
def add_xp(xp_amount: int, user_id: int):
    querey_user = check_db_for_user(user_id)
    if querey_user is None:
        initiate_user(user_id=user_id) 
    
    cur_xp = get_user_xp(user_id=user_id)
    xp_to_give = cur_xp + xp_amount
    cur.execute(
        "UPDATE users SET current_xp = ? WHERE user_id=?", (xp_to_give, user_id,)
    )
    conn.commit()

#Adds credits
def add_credits(credit_amount: int, user_id: int):
    querey_user = check_db_for_user(user_id)
    if querey_user is None:
        initiate_user(user_id=user_id) 

    #Get their credit amount first
    cur.execute(
        "SELECT credits FROM users WHERE user_id = ?", (user_id,)
    )
    current_credits = cur.fetchone()
    current_credits = int(current_credits[0])
        
    added_amount = current_credits + credit_amount
    cur.execute(
        "UPDATE users SET credits = ? WHERE user_id = ?", (added_amount, user_id,)
    )
    conn.commit()

#Removes credits
def remove_credits(credit_amount: int, user_id: int):
    querey_user = check_db_for_user(user_id)
    if querey_user is None:
        initiate_user(user_id=user_id) 
    #Get their credit amount first
    cur.execute(
        "SELECT credits FROM users WHERE user_id = ?", (user_id,)
    )
    current_credits = cur.fetchone()
    current_credits = int(current_credits[0])       #Fuck truples

    removed_amount = current_credits - credit_amount
        
    #aaaaand its gone
    cur.execute(
        "UPDATE users SET credits = ? WHERE user_id = ?", (removed_amount, user_id)
    )
    conn.commit

#Sets a user's credits to an amount
#This will exist for moderation purposes.
def set_credits(credit_amount: int, user_id: int):
    querey_user = check_db_for_user(user_id)
    if querey_user is None:
        initiate_user(user_id=user_id)  
    cur.execute(
        "UPDATE users SET credits = ? WHERE user_id = ?", (credit_amount, user_id,)
    )
    conn.commit()

#Get the user's current credit balance
def get_credits(user_id: int):
    querey_user = check_db_for_user(user_id)
    if querey_user is None:
        initiate_user(user_id=user_id) 
    cur.execute(
        "SELECT credits FROM users WHERE user_id = ?", (user_id,)
    )
    cur_cred = cur.fetchone()
    cur_cred = int(cur_cred[0])     #Fuck truples
    return cur_cred

#Create a day long cooldown
def init_cooldown(user_id: int):
    cooldown = int(datetime.now().timestamp()) + 86400
    cur.execute(
        "UPDATE users SET daily_cooldown = ? WHERE user_id = ?", (cooldown, user_id)
    )
    conn.commit()

#Check if the cooldown has passed
def cooldown_complete(user_id: int):
    cur.execute(
        "SELECT daily_cooldown FROM users WHERE user_id = ?", (user_id,)
    )        
    cooldown = cur.fetchone()
    if cooldown == None:
        init_cooldown(user_id)
    cooldown = int(cooldown[0])

    if int(datetime.now().timestamp()) > cooldown:
        return True
    else:
        return False
    
def cooldown_left(user_id: int):
    cur.execute(
        "SELECT daily_cooldown FROM users WHERE user_id = ?", (user_id,)
    )
    cd_left = cur.fetchone()
    cd_left = int(cd_left[0])
    return cd_left
    
#Shows the leaderboard
def get_leaderboard():
    cur.execute(
        "SELECT user_id, level, credits FROM users ORDER BY credits DESC, level DESC LIMIT 10"
    )
    results = cur.fetchall()
    return results

#Get the theft cooldown on a user
def get_theft_cooldown(user_id: int):
    cur.execute(
        "SELECT theft_cooldown FROM users WHERE user_id = ?", (user_id,)
    )
    cooldown = cur.fetchone()
    cooldown = int(cooldown[0])
    return cooldown

#Set the theft cooldown on a user
def set_theft_cooldown(amount: int, user_id: int):
    cur.execute(
        "UPDATE users SET theft_cooldown = ? WHERE user_id = ?", (amount, user_id,)
    )
    conn.commit()




#GUILD TABLE

#Initiate a guild into the DB
def init_guild(guild_id: int):
    cur.execute(
        "INSERT INTO guilds (guild_id, log_chan_id) VALUES (?, 0)", (guild_id,)
    )
    conn.commit()
        


#Set a guild's log channel
def set_log_channel(channel_id: int, guild_id: int):
    #See if the guild is in the db first.
    cur.execute(
        "SELECT guild_id = ? FROM guilds", (guild_id,)
    )
    gid = cur.fetchall()
    #If it isn't, it should be!
    if gid == None:
        init_guild(guild_id)
        
    cur.execute(
        "UPDATE guilds SET log_chan_id = ? WHERE guild_id = ?", (channel_id, guild_id,)
    )
    conn.commit()
    
    

#Get the guild's log channel
def get_log_channel(guild_id: int):
    cur.execute(
        "SELECT log_chan_id FROM guilds WHERE guild_id = ?", (guild_id,)
    )
    id = cur.fetchall()
    id = int(id[0])

    return id 