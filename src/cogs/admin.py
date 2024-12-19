import discord
from discord.ext import commands

from src.classes.bot import Bot, Cog


class AdminCommands(Cog):
    """관리자 전용 명령어"""

    hidden_help = True # 도움말에 표시하지 않음


    @commands.command(
        name="ping",
        help="pong!",
    )
    @commands.is_owner()
    async def ping(self, ctx: commands.Context[Bot]):
        await ctx.reply(f"pong! latency: {round(self.bot.latency * 1000)}ms")


async def setup(bot: Bot):
    await bot.add_cog(AdminCommands(bot))
