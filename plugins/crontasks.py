from khl import Bot

from .logger import addLog
from .lucky import lucky_list


def initCrons(bot: Bot) -> None:
    
    @bot.task.add_cron(timezone='Asia/Shanghai',
                       hour=23, minute=59, second=59)
    async def taskResetFortune():
        global lucky_list
        lucky_list.clear()
        addLog('[TASK]已重置今日人品')
