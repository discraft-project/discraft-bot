from discord.ext import commands

class NotRegisteredUser(commands.CheckFailure):
    """DB에 등록되지 않은 사용자가 있을 때 발생"""
    pass
