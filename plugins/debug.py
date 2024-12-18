import sys
from functools import wraps
from typing import Callable

from khl import Bot, Message, MessageTypes

from .globals import ADMIN, DEBUG
from .logger import debugLogger, logName, addLog
from .exceptions import default_exc_handler, Errors


def permission(lvl: list, description: str):
    def decorator(func: Callable):
        @wraps(func)
        async def wrappper(msg: Message, *args):
            if msg.author_id not in lvl: raise Errors.PermissionError(description)
            result = await func(msg, *args)
            return result
        return wrappper
    return decorator


def debug_command(bot: Bot) -> None:

    @bot.command(name='debug',
                 case_sensitive=False,
                 prefixes=['//'],
                 exc_handlers=default_exc_handler)
    @debugLogger
    @permission(ADMIN, '管理员')
    async def debugFunc(msg: Message, *args):
        msg.reply(' '.join(args), use_quote=False)

    @bot.command(name='log',
                 case_sensitive=False,
                 prefixes=['//'],
                 exc_handlers=default_exc_handler)
    @debugLogger
    @permission(ADMIN, '管理员')
    async def debugLog(msg: Message, *args):
        debug_channel = await bot.client.fetch_public_channel(DEBUG)
        log_url = await bot.client.create_asset(f'.\\log\\{logName()}.log')
        err_url = await bot.client.create_asset(f'.\\log\\error.txt')
        await debug_channel.send('已生成日志。')
        await debug_channel.send(log_url, type=MessageTypes.FILE)
        await debug_channel.send(err_url, type=MessageTypes.FILE)

    @bot.command(name='off',
                 case_sensitive=False,
                 prefixes=['//'],
                 exc_handlers=default_exc_handler)
    @debugLogger
    @permission(ADMIN, '管理员')
    async def debugOff(msg: Message, *args):
        debug_channel = await bot.client.fetch_public_channel(DEBUG)
        await debug_channel.send('Bot 已成功下线。')
        await bot.client.offline()
        addLog(f'[MAIN]Bot已关闭\n')
        sys.exit(0)

    @bot.command(name='error',
                 case_sensitive=False,
                 prefixes=['//'],
                 exc_handlers=default_exc_handler)
    @debugLogger
    @permission(ADMIN, '管理员')
    async def debugError(msg: Message, *args):
        raise Errors.DebugError(' '.join(args))

