import discord
from discord.ext import commands

from src.config import ENV
from src.classes.bot import Bot


bot = Bot()
bot.run(ENV.DISCORD_BOT_TOKEN)
