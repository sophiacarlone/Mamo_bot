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

day_map = {"SUN":1, "MON":2, "TUE": 3, "WEN": 4, "THU": 5, "FRI": 6, "SAT": 7}


########## HELPER FUNCTIONS ###########

#Parse the day string
#Input: day as a str
#Returns: day as a number or zero for invalid input
def parse_day(day: str):
    day = day.upper()
    day = day[:3]
    print(day)
    return day_map.get(day, 0)
    

######### DISCORD FUNCTIONS ###########
#Add
@tree.command(
    name = "add_scheduled_ping",
    description = "Add a time to ping everyone in format: <Mon/Tues/Wed/Thu/Fri/Sat/Sun>, <Time of day AM/PM>, <role>"
)
async def add_to_schedule(interaction: discord.Interaction, message: str) -> None:
    message.strip("")
    info = message.split(",")

    day = info[0] #TODO condense later
    day = parse_day(day)
    if (day == 0):
        await interaction.response.send_message("invalid input")
        return
    else:
        info[0] = day
    
    time = info[1]
    
    role = info[2]
    
    schedule.append(info)
    
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
