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


# #Add
# @tree.command(
#         name = "add_scheduled_ping",
#         description = "Add a time to ping everyone in format: <Mon/Tues/Wed/Thu/Fri/Sat/Sun>, <Time of day AM/PM>, <role>"
# )
# async def add_to_schedule(interaction: discord.Interaction, message: str):
#     message.strip("")
#     info = message.split(",")
#     day = info[0]
#     time = info[1]
#     role = info[2]
#     print(day + " " + time + " " + role)


# ##MAIN##
# @client.event
# async def on_ready():
#     print(f'We have logged in as {client.user}')
#     await tree.sync()
#     # run.start()

# This example requires the 'message_content' intent.

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')




f = open("token.txt", "r")
token = f.readline().strip("\n");
client.run(token)
