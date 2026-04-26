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

day_map = {"SUN":1, "MON":2, "TUE": 3, "WED": 4, "THU": 5, "FRI": 6, "SAT": 7}


########## HELPER FUNCTIONS ###########

#Parse the day string
#Input: day as a str
#Returns: day as a number or zero for invalid input
def parse_day(day: str):
    day = day.upper()
    day = day[:3]
    return day_map.get(day, 0)

#-------------------------------------------------------

def parse_time(time: str):
    time = time.lower();
    time = time.strip()

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

    

######### DISCORD FUNCTIONS ###########
#Add
@tree.command(
    name = "add_scheduled_ping",
    description = "format: <Mon/Tues/Wed/Thu/Fri/Sat/Sun>, <Time of day AM/PM>, <role>, <message>"
)
async def add_to_schedule(interaction: discord.Interaction, message: str) -> None:
    message.strip("")
    info = message.split(",")
    if (len(info) < 4):
        await interaction.response.send_message("invalid input")
        return

    #parse day
    day = info[0] #TODO condense later
    day = parse_day(day)
    if (day == 0):
        await interaction.response.send_message("invalid input")
        return
    else:
        info[0] = day
    
    #parse time
    time = parse_time(info[1])
    if (time[0] == -1):
        await interaction.response.send_message("invalid input")
        return
    
    role = info[2]

    mess = info[3]
    
    # schedule.append(info)
    
    await interaction.response.send_message("valid, thank you")
    print(schedule)


# #Print schedule
# @tree.command(
#     name = "print_schedule",
#     description = "whats the schedule?"
# )
# async def add_to_schedule(interaction: discord.Interaction) -> None:
#     await interaction.response.send_message("schedule")


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
