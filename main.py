# HII DAVID WYATT - this is for you :)

import time
import datetime
from datetime import date
import discord
from discord import app_commands

#setting up discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

#hoping to put it in a list because it shouldnt be that long for my server purposes. Can move to a file
schedule = []

day_map = {"SUN":0, "MON":1, "TUE":2, "WED":3, "THU":4, "FRI":5, "SAT":6}


########## HELPER FUNCTIONS ###########

#Parse the day string
#Input: day as a str
#Returns: day as a number or -1 for invalid input
def parse_day(day: str):
    day = day.upper()
    day = day[:3]
    return day_map.get(day, -1)

#-------------------------------------------------------

#Parse the time string
#Input: time as a str
#Returns: hours and minutes as miltary time or -1 for invalid input
def parse_time(time: str):
    time = time.lower().strip()

    #get if its am or pm 
    afternoon = True #bias towards the afternoon
    if (time.find("am") >= 0):
        afternoon = False
    time = time.rstrip("apm")
    
    #if contains a : then separate hours from minutes
    info = time.split(":", 1)
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

    return hours, minutes

#-------------------------------------------------------

#86400 -> seconds in a day
def time_to_seconds(day, hour, minute):
    day_sec = (day * 86400) + (hour * 3600) + (minute * 60)
    return day_sec


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
    message.strip("")

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
    
    day_time = time_to_seconds(day, time[0], time[1])
    
    #add to schedule
    event = {day_time: (role, message)}
    schedule.append(event)
    schedule.sort()

    await interaction.response.send_message("scheduled") #sometimes does two @

    print(schedule)
    # await interaction.response.send_message(f"{role.mention} {message}")


##MAIN##
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await tree.sync()
    # run.start()


f = open("token.txt", "r")
token = f.readline().strip("\n");
client.run(token)
f.close()
