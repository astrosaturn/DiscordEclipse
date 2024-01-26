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
        "INSERT INTO users (user_id, user_level, current_xp, credits, daily_cooldown, theft_cooldown, bank) VALUES (?, 1, 0, 0, 0, 0, 0)", (user_id,))
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
            "SELECT user_level FROM users WHERE user_id=?", (user_id,)
        )
    level = cur.fetchone()
    return level

#Let me try and see if i can lower the line limit a little bit LOL!
#Hopefully this will be able to be used to streamline the code
#And improve readability
def get_user_stat(stat_type: str, user_id: int):
    #If the user isnt in the database, add them.
    querey_user = check_db_for_user(user_id)
    if querey_user is None:
        initiate_user(user_id=user_id)
    
    cur.execute(f"SELECT {stat_type} FROM users WHERE user_id = ?", (user_id,))
    x = cur.fetchone()
    x = int(x[0])
    return x

def set_user_stat(stat_type: str, action: str, amount: int, user_id: int): # <--- This function is only used internally and by one command that is only useable by a developer.
    #First, check if the user is in the database.                                 It is also impossible to SQL inject into because of the checks it does so it wouldnt matter anyways.
    querey_user = check_db_for_user(user_id)
    if querey_user is None:
        initiate_user(user_id=user_id)
    
    match stat_type:
        case "current_xp":
            current_xp = get_user_stat("current_xp", user_id)
            if (action == "add"):
                new_stat_value = current_xp + amount
            elif (action == "remove"):
                new_stat_value = current_xp - amount
            else:
                new_stat_value = amount
        
        case "user_level":
            current_level = get_user_stat("user_level", user_id)
            if (action == "add"):
                new_stat_value = current_level + amount
            elif (action == "remove"):
                new_stat_value = current_level - amount
            else:
                new_stat_value = amount
        
        case "credits":
            current_balance = get_user_stat("credits", user_id)
            if (action == "add"):
                new_stat_value = current_balance + amount
            elif (action == "remove"):
                new_stat_value = current_balance - amount
            else:
                new_stat_value = amount
        
        case "bank":
            current_bank = get_user_stat("bank", user_id)
            if (action == "add"):
                new_stat_value = current_bank + amount
            elif (action == "remove"):
                new_stat_value = current_bank - amount
            else:
                new_stat_value = amount

    cur.execute(f'UPDATE users SET {stat_type} = ? WHERE user_id = ?', (new_stat_value, user_id,))
    conn.commit()  

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
        "SELECT user_id, user_level, credits FROM users ORDER BY credits DESC, user_level DESC LIMIT 10"
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
        "INSERT INTO guilds (guild_id, log_chan_id, scrape_chan_id, scraper_wh_id) VALUES (?, 0, 0, 0)", (guild_id,)
    )
    conn.commit()

#Check to see if a guild has been init into the database
def check_db_for_guild(guild_id: int):
    cur.execute(
        "SELECT guild_id FROM guilds WHERE guild_id = ?", (guild_id,)
    )
    guildid = cur.fetchone()
    if guildid is not None:
        guildid = int(guildid[0])
        return guildid
    else:
        return None



#Set a guild's log channel
def set_log_channel(channel_id: int, guild_id: int):
    #Check the DB for the guild
    querey_guild = check_db_for_guild(guild_id)
    #If it isnt in the DB, it should be!
    if querey_guild is None:
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
    try:
        id = ''.join(map(str,id[0]))        #WHAT THE FUCK DOES THIS EVEN MEAN??
        id = int(id)
        return id 
    except IndexError:
        return

#Set the scraper channel
def set_scrape_chan_id(channel_id:int, guild_id:int):
    #Check DB for the guild
    querey_guild = check_db_for_guild(guild_id)
    #If it isnt there, it should be!
    if querey_guild is None:
        init_guild(guild_id)
    
    cur.execute(
        "UPDATE guilds SET scrape_chan_id = ? WHERE guild_id = ?", (channel_id, guild_id,)
    )
    conn.commit()

#Get the scraper channel ID
def get_scrape_channel_id(guild_id: int):
    cur.execute(
        "SELECT scrape_chan_id FROM guilds WHERE guild_id = ?", (guild_id,)
    )
    id = cur.fetchall()
    #Handle the index being out of range for when the channel isnt assigned just so it doesnt clog my fucking terminal.
    try:
        id = ''.join(map(str,id[0]))
        id = int(id)
        return id
    except IndexError: 
        return
    
#Set the webhook ID
def set_webhook_id(webhook_id:int, guild_id:int):
    cur.execute(
        "UPDATE guilds SET scraper_wh_id = ? WHERE guild_id = ?", (webhook_id, guild_id,)
    )
    print(f"Scraper webhook id set to {webhook_id} in {guild_id}")
    conn.commit()

#Get the webhook ID
def get_webhook_id(guild_id:int):
    cur.execute(
        "SELECT scraper_wh_id FROM guilds WHERE guild_id = ?", (guild_id,)
    )
    id = cur.fetchall()
    id = ''.join(map(str,id[0]))
    id = int(id)
    return id

#ACTIONS TABLE
def generate_case_num():
    cur.execute(
        "SELECT MAX(casenum) FROM actions"
    )
    recent_case = cur.fetchone()
    if recent_case == None:
        recent_case = 0
    else:
        recent_case = int(recent_case[0])
    new_casenum = recent_case + 1
    return new_casenum

def create_action(user_id:int, guild_id:int, action_type:str, reason:str, moderator:int, username:str):
    case_num = generate_case_num()
    cur.execute(
        "INSERT INTO actions (user_id, guild_id, action_type, reason, moderator, casenum, username) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, guild_id, action_type, reason, moderator, case_num, username)
    )
    conn.commit()

def get_case(case_num:int):
    cur.execute(
        "SELECT * FROM actions WHERE casenum = ?", (case_num,)
    )
    row = cur.fetchone()

    if row is not None:
        user_id, guild_id, action_type, reason, moderator, casenum, username = row
        return int(user_id), int(guild_id), action_type, reason, int(moderator), int(casenum), username
    
def get_case_num(user_id):
    cur.execute(
        "SELECT MAX(casenum) FROM actions WHERE user_id = ?", (user_id,)
    )
    case_num = cur.fetchone()
    case_num = int(case_num[0])
    return case_num