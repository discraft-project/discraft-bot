from discord.ext import commands

import logging

from src.classes.bot import Bot
from src.classes.errors import NotRegisteredUser

logger = logging.getLogger("discord.classes.Checks")


def is_registered():
    """DB에 사용자가 등록되어있는지 확인"""
    async def predicate(ctx: commands.Context[Bot]):
        if ctx.invoked_with == "help": # help 명령어 실행시 체크 안함.
            return False

        logger.debug(f"Checking if {ctx.author.id} is registered")
        raise NotImplementedError("DB 연동이 되지 않아 사용자 등록 체크를 할 수 없습니다.")
        # return True

    return commands.check(predicate)