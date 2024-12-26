import discord
from discord.ext import commands

import logging
import asyncio
from pathlib import Path

from src.config import ENV
from src.classes.errors import NotRegisteredUser

# https://github.com/AlexFlipnote/discord_bot.py/blob/master/utils/data.py


class Bot(commands.Bot):
    """Discord 봇 클래스"""

    def __init__(self):
        self.logger = logging.getLogger(f"discord.classes.{self.__class__.__name__}")

        # Bot 권한 설정
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        # command.Bot 초기화
        super().__init__(
            command_prefix=commands.when_mentioned_or(ENV.DISCORD_BOT_PREFIX),
            intents=intents,
            help_command=commands.DefaultHelpCommand(),
        )

    async def setup_hook(self):
        # Cog 로드
        def task_finish_callback(task: asyncio.Task[None], name: str):
            try:
                task.result()
                self.logger.info(f"{name} loaded")
            except Exception as e:
               self.logger.error(f"Failed to load {name}: {e}")

        cogs_dir = Path("./src/cogs")
        try:
            async with asyncio.TaskGroup() as tg:
                for item in cogs_dir.iterdir():
                    if item.name.startswith("_"): # _로 시작하는 파일은 무시
                        self.logger.debug(f"Ignored file/directory: {item.name}")
                        continue

                    # 정상적인 Cog 파일인지 확인
                    if (
                        (item.is_dir() and (item / "__init__.py").exists())
                        or (item.is_file() and item.suffix == ".py")
                    ):
                        cog_fullname = f"src.cogs.{item.stem if item.is_file() else item.name}"
                        task = tg.create_task(self.load_extension(cog_fullname))
                        task.add_done_callback(lambda t, name=cog_fullname: task_finish_callback(t, name))
                    else:
                        self.logger.warning(f"Invalid Cog file/directory: {item}")

        except ExceptionGroup as eg:
            self.logger.error(f"Failed to load {len(eg.exceptions)} cogs", exc_info=True)

        # 앱 커맨드 동기화
        if ENV.DISCORD_GUILD_ID:
            GUILD_ID = discord.Object(id=ENV.DISCORD_GUILD_ID)
            self.tree.copy_global_to(guild=GUILD_ID)
            await self.tree.sync(guild=GUILD_ID)
        else:
            await self.tree.sync()

    async def on_ready(self):
        self.logger.info(f"{self.user} 봇 준비 완료")
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(ENV.DISCORD_BOT_ACTIVITY) if ENV.DISCORD_BOT_ACTIVITY else None,
        )

    async def on_message(self, message: discord.Message):
        if message.guild is None: # DM은 무시
            return

        await self.process_commands(message) # 명령어 처리

    async def on_command_error(self, ctx: commands.Context["Bot"], error: commands.CommandError):
        if isinstance(error, (
            commands.CommandNotFound, # 명령어가 없을 때
            commands.NotOwner         # 관리자 명령어를 호출했을 때
        )):
            return

        elif isinstance(error, NotRegisteredUser):
            await ctx.reply("사용자 등록을 먼저 해 주세요.")
            return

        elif isinstance(error, discord.DiscordServerError):
            await ctx.reply("오류가 발생했습니다.")
            self.logger.warning(error)
            return

        elif isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, discord.NotFound):
                await ctx.reply("오류가 발생했습니다.")
                self.logger.warning(error.original.args[0])
                return

        if ctx.command_failed:
            await ctx.reply("오류가 발생했습니다.")
            self.logger.error((
                f"Ignoring exception in command {ctx.command}: "
                f"User: {ctx.author} (ID: {ctx.author.id}) | "
                f"Content: {ctx.message.content}"
            ), exc_info=error)

    async def close(self):
        # if self.database is not None:
        #     await self.database.close()
        await super().close()


class Cog(commands.Cog):
    """명령어 카테고리 클래스"""

    # 명령어 도움말에 숨길지 여부
    hidden_help_command = False

    def __init__(self, bot: Bot):
        self.bot = bot
        self.logger = logging.getLogger(f"discord.cog.{self.__class__.__name__}")

        self.bot.logger.debug(f"Cog {self.__class__.__name__} loaded")

    # 명령어가 실행되기 전 실행되는 함수
    async def cog_before_invoke(self, ctx: commands.Context[Bot]):
        self.logger.debug(
            f"Command invoked | "
            f"User: {ctx.author} (ID: {ctx.author.id}) | "
            f"Command: {ctx.command} | "
            f"Content: {ctx.message.content}"
        )
