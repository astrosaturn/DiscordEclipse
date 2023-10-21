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
        "INSERT INTO users (user_id, level, current_xp, credits, daily_cooldown, theft_cooldown, bank) VALUES (?, 1, 0, 0, 0, 0, 0)", (user_id,))
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

#Get the user's bank balance
def get_bank_bal(user_id: int):
    cur.execute(
        "SELECT bank FROM users WHERE user_id = ?", (user_id,)
    )
    balance = cur.fetchone()
    balance = ''.join(map(str,balance[0]))
    balance = int(balance)
    return balance

#Update a users bank balance
def update_bank_balance(amount: int, user_id: int):
    cur.exectue(
        "UPDATE users SET bank = ? WHERE user_id = ?", (amount, user_id,)
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
    id = ''.join(map(str,id[0]))        #WHAT THE FUCK DOES THIS EVEN MEAN??
    id = int(id)
    return id 

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
    if id == None:
        return
    else:
        id = ''.join(map(str,id[0]))
        id = int(id)
        return id
    
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

def create_action(user_id:int, guild_id:int, type:str, reason:str, moderator:int, username:str):
    case_num = generate_case_num()
    cur.execute(
        "INSERT INTO actions (user_id, guild_id, type, reason, moderator, casenum, username) VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, guild_id, type, reason, moderator, case_num, username)
    )
    conn.commit()

def get_case(case_num:int):
    cur.execute(
        "SELECT * FROM actions WHERE casenum = ?", (case_num,)
    )
    row = cur.fetchone()

    if row is not None:
        user_id, guild_id, type, reason, moderator, casenum, username = row
        return int(user_id), int(guild_id), type, reason, int(moderator), int(casenum), username
    
def get_case_num(user_id):
    cur.execute(
        "SELECT MAX(casenum) FROM actions WHERE user_id = ?", (user_id,)
    )
    case_num = cur.fetchone()
    case_num = int(case_num[0])
    return case_num