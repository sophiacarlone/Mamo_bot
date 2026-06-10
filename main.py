# HII DAVID WYATT - this is for you :)

import time
import asyncio
import datetime
from datetime import date
import discord
from discord import app_commands
from discord.ext import tasks

#setting up discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


######### GLOBALS ###########
schedule = {} #schedule of events
time_index = 0
day_map = {"MO":0, "TU":1, "WE":2, "TH":3, "FR":4, "SA":5, "SU":6}
CHANNEL = 1179068545297043537


########## HELPER FUNCTIONS ###########

#Parse the day string
#Input: day as a str
#Returns: day as a number or -1 for invalid input
def parse_day(day: str):
    day = day.upper()
    day = day[:2]
    return day_map.get(day, -1)

#-------------------------------------------------------

#Parse the time string
#Input: time as a str
#Returns: hours and minutes as miltary time or -1 for invalid input
def parse_time(time: str):
    time = time.lower().strip()
    seconds = 0 #remove later
    #get if its am or pm 
    afternoon = True #bias towards the afternoon
    if (time.find("a") >= 0):
        afternoon = False
    time = time.rstrip("apmAPM")
    
    #if contains a : then separate hours from minutes
    info = time.split(":", -1)
    if(len(info) == 3):
        seconds = int(info[2])
        if seconds > 59 or seconds < 0:
            seconds = 0
    hours = int(info[0])
    minutes = 0
    if (len(info) == 2):
        minutes = int(info[1])
    if (hours > 12 or minutes > 59):
        return -1,-1
    
    #put into military time
    if not afternoon and hours == 12:
        hours = 0
    if (afternoon and hours != 12):
        hours = hours + 12

    return hours, minutes, seconds

#-------------------------------------------------------

#86400 -> seconds in a day
def time_to_seconds(day, hour, minute, seconds):
    day_sec = (day * 86400) + (hour * 3600) + (minute * 60) + seconds
    return day_sec

#-------------------------------------------------------

def seconds_to_time(seconds_format):
    #day
    day = ""
    d = int(seconds_format / 86400)
    for key, val in day_map.items():
        if val == d:
            day = key
            continue
    seconds_format = seconds_format % 86400

    #hour
    hour = int(seconds_format / 3600)
    seconds_format = seconds_format % 3600

    #minute
    minute = int(seconds_format / 60)

    #second
    second = seconds_format % 60

    return day, hour, minute, second

#-------------------------------------------------------

def find_closest_event(now):
    difference = 604800 #seconds in a week
    closest = 0
    for _, key in enumerate(schedule):
        temp = key - now
        if temp >= 0 and temp < difference:
            closest = key
            difference = temp
    #wrap around week
    if(closest == 0):
        closest = next(iter(schedule))
    return closest
    

######### DISCORD FUNCTIONS ###########
#Add
@tree.command(
    name = "add_scheduled_ping",
    description = "format: <Mon/Tues/Wed/Thu/Fri/Sat/Sun>, <Time of day AM/PM>, <role>, <message>"
)
@app_commands.describe(
    day="day of the week",
    time="time(default is afternoon)",
    role="whos your victim",
    message="message"
)
async def add_to_schedule(
    interaction: discord.Interaction, 
    day: str,
    time: str,
    role: discord.Role,
    message: str
) -> None:
    global schedule
    message.strip("")

    #parse day
    day = parse_day(day)
    if (day == -1):
        await interaction.response.send_message("invalid input day " + message)
        return
    
    #parse time
    time = parse_time(time)
    if (time[0] == -1):
        await interaction.response.send_message("invalid input time for event " + message)
        return
    
    day_time = time_to_seconds(day, time[0], time[1], time[2])
    
    #add to schedule
    schedule[day_time] = (role, message)
    schedule = dict(sorted(schedule.items(), key = lambda item: item[0]))

    await interaction.response.send_message("scheduled event " + message) #sometimes does two @

#-------------------------------------------------------

@tree.command(
name = "delete_scheduled_ping",
description = "format: <Mo/Tu/We/Th/Fr/Sa/Su>, <Time of day AM/PM>"
)
@app_commands.describe(
    day="day of the week",
    time="time(default is pm)",
)
async def delete_from_schedule(
    interaction: discord.Interaction, 
    day: str,
    time: str
) -> None:
    
    #parse day
    day = parse_day(day)
    if (day == -1):
        await interaction.response.send_message("invalid input day")
        return
    
    #parse time
    time = parse_time(time)
    if (time[0] == -1):
        await interaction.response.send_message("invalid input time")
        return
    day_time = time_to_seconds(day, time[0], time[1], time[2])

    #remove from schedule if its there
    if(schedule.pop(day_time, -1) == -1):
        await interaction.response.send_message("event not found") 
    else:
        await interaction.response.send_message("event removed") 

#-------------------------------------------------------

@tree.command(
name = "list_scheduled_pings"
)
async def list_schedule(
    interaction: discord.Interaction, 
) -> None:
    if len(schedule) == 0:
        await interaction.response.send_message("no scheduled events")
        return
    message = ""
    for key, val in schedule.items():
        day, hour, minute, second = seconds_to_time(key)
        message += (day + ", " + str(hour) + ":" + str(minute) + " " + val[1] + "\r\n")
    await interaction.response.send_message(message)
    
#-------------------------------------------------------

@tasks.loop()
async def pinger():
    channel = client.get_channel(CHANNEL)
    global schedule
    if(len(schedule) == 0):
        return
    
    #time now
    now = datetime.datetime.now()
    now_sec = time_to_seconds(now.today().weekday(), now.hour, now.minute, now.second) 
    
    # #time of next event
    next_event = find_closest_event(now_sec)
    # print("event")
    # print(seconds_to_time(next_event))
    # print("now")
    # print(seconds_to_time(now_sec))

    if(now_sec == next_event):
        role, message = schedule[next_event]
        await channel.send(f"{role.mention} {message}")
    
    await asyncio.sleep(1) #would turn to 60 later
    # #sleep till next event
    # if(now_sec > next_event): #wrapping around the week
    #     seconds_diff = (604800 - now_sec)+next_event
    #     # time.sleep(seconds_diff)
    #     await asyncio.sleep(seconds_diff)
    # else:
    #     # time.sleep(next_event-now_sec)
    #     await asyncio.sleep(next_event-now_sec)
    
    # #EVENT TIME!
    # role, message = schedule[next_event]
    # await channel.send(f"{role.mention} {message}")
    # # await asyncio.sleep(59) #dont repeat yourself


################### MAIN ######################
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await tree.sync()
    pinger.start()

f = open("token.txt", "r")
token = f.readline().strip("\n");
client.run(token)
f.close()
