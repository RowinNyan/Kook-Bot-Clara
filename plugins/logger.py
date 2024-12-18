import time
from functools import wraps
from typing import Callable, Any

from khl import Message, GuildUser


def cmdLogger(func: Callable[[Message, Any], Any]):
    @wraps(func)
    async def wrapper(msg: Message, *args) -> Any:
        author: GuildUser = msg.author
        addLog(f'[UCMD]{author.nickname}({author.id}): 调用函数{func.__name__}()，附加信息为\"{" ".join(args)}\"')
        try:
            result = await func(msg, *args)
            return result
        except Exception as e:
            raise e
    return wrapper

def debugLogger(func: Callable[[Message, Any], Any]):
    @wraps(func)
    async def wrapper(msg: Message, *args) -> Any:
        author: GuildUser = msg.author
        addLog(f'[DCMD]{author.nickname}({author.id}): 调用函数{func.__name__}()，附加信息为\"{" ".join(args)}\"')
        try:
            result = await func(msg, *args)
            return result
        except Exception as e:
            raise e
    return wrapper

def logName() -> str:
    return time.strftime(f"%Y-%m-%d", time.localtime())

def addLog(log: str) -> None:
    with open(f'.\\log\\{logName()}.log', 'a', encoding='utf-8') as f:
        n_time = time.strftime(f"%H:%M:%S", time.localtime())
        f.write(f'[{n_time}]{log}\n')
    print(f'[{n_time}]{log}')

