# HII DAVID WYATT - this is for you :)

import time
import datetime
from datetime import date
import discord
from discord import app_commands

# CHANNEL = #add in channel here
# TOKEN = #add in here

#setting up discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
# client.tree = tree




#Add
@tree.command(
    name = "add_scheduled_ping",
    description = "Add a time to ping everyone in format: <Mon/Tues/Wed/Thu/Fri/Sat/Sun>, <Time of day AM/PM>, <role>"
)
async def add_to_schedule(interaction: discord.Interaction, message: str) -> None:
    message.strip("")
    info = message.split(",")
    day = info[0]
    time = info[1]
    role = info[2]
    f = open("schedule.txt", "a")
    f.write(message)
    f.write("\n")
    f.close()
    await interaction.response.send_message(message)
    print(day + " " + time + " " + role)



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
