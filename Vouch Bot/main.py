import discord
from discord.ext import commands
from discord import app_commands
import json
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

try:
    with open('config.json') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    print("config.json file not found.")
    exit(1)


async def load_commands():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await bot.load_extension(f'commands.{filename[:-3]}')

@bot.event
async def on_ready():
    await load_commands()
    await bot.tree.sync()  
    print(f'{bot.user} has connected to Discord!')
    
bot.run(config['token'])