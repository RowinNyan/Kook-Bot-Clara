import time
import traceback
from functools import wraps
from typing import Callable

from khl import Message, command
from khl.card import Card, CardMessage, Module, Element
import khl.command.exception

from .logger import addLog


class Errors:

    class BaseError(Exception):
        def __init__(self, *args):
            super().__init__(*args)

    class DebugError(BaseError):
        def __init__(self, *args):
            super().__init__(*args)

    class ParameterError(BaseError):
        def __init__(self, *args):
            super().__init__(*args)

    class PermissionError(BaseError):
        def __init__(self, *args):
            super().__init__(*args)

    class ResponseError(BaseError):
        def __init__(self, *args):
            super().__init__(*args)

    class TerminalError(BaseError):
        def __init__(self, *args):
            super().__init__(*args)


class Warnings:

    class BaseWarning(Exception):
        def __init__(self, *args):
            super().__init__(*args)

    class MusicSearchWarning(BaseWarning):
        def __init__(self, *args):
            super().__init__(*args)


def errorLog(func: Callable[[command.Command, Exception, Message], bool]) -> None:
    @wraps(func)
    async def wrapper(cmd: command.Command,
                      exc: Exception,
                      msg: Message) -> bool:
        if isinstance(exc, khl.command.exception.Exceptions.Lexer.NotMatched): return
        result: bool = await func(cmd, exc, msg)
        if result:
            tb_str = ''.join(traceback.format_tb(exc.__traceback__))
            with open(f'.\\log\\error.txt', 'a', encoding='utf-8') as f:
                n_time = time.strftime(f"%Y-%m-%d %H:%M:%S", time.localtime())
                f.write(f'[{n_time}][EXC]Raised {str(type(exc))[8:-2]} when executing command "{cmd.name}".\n')
                f.write('Traceback (most recent call last):\n')
                f.write(f'{tb_str}')
                f.write(f'{str(type(exc))[8:-2]}: {exc}\n\n')
        return result
    return wrapper


@errorLog
async def catchException(cmd: command.Command,
                         exc: Exception,
                         msg: Message):

    if isinstance(exc, Errors.BaseError):
        if isinstance(exc, Errors.DebugError): 
            c = Card(Module.Header(Element.Text('【错误】调试错误')),
                     Module.Divider(),
                     Module.Section(Element.Text(f'错误信息：`{exc}`。')),
                     color='#dd3333')
        elif isinstance(exc, Errors.ParameterError):
            c = Card(Module.Header(Element.Text('【错误】命令传参格式错误')),
                     Module.Divider(),
                     Module.Section(Element.Text(f'命令传参格式错误，应当传入参数的类型为：`{exc}`。')),
                     Module.Section(Element.Text('由于命令传参格式错误，刚才的命令未能正确执行，请更换参数后重试。')),
                     color='#dd3333')
        elif isinstance(exc, Errors.PermissionError):
            c = Card(Module.Header(Element.Text('【错误】用户权限错误')),
                     Module.Divider(),
                     Module.Section(Element.Text('用户权限不足。')),
                     Module.Section(Element.Text(f'命令`{cmd.name}`需要{exc}权限才能调用。')),
                     color='#dd3333')
        elif isinstance(exc, Errors.ResponseError):
            c = Card(Module.Header(Element.Text('【错误】发生网络错误')),
                     Module.Divider(),
                     Module.Section(Element.Text(f'发生网络错误，错误码：`{exc}`。')),
                     Module.Section(Element.Text('由于发生网络错误，刚才的命令未能成功执行，请重试。')),
                     color='#dd3333')
        elif isinstance(exc, Errors.TerminalError):
            c = Card(Module.Header(Element.Text('【错误】终端指令执行错误')),
                     Module.Divider(),
                     Module.Section(Element.Text(f'终端指令执行错误，错误信息：`{exc}`。')),
                     Module.Section(Element.Text('由于终端指令执行错误，刚才的命令未能执行，请重试。')),
                     color='#dd3333')

    elif isinstance(exc, Warnings.BaseWarning):
        if isinstance(exc, Warnings.MusicSearchWarning):
            c = Card(Module.Header(Element.Text('【警告】未能成功搜索到歌曲')),
                     Module.Divider(),
                     Module.Section(Element.Text(f'未能搜索到歌曲 **{exc}**。')),
                     Module.Section(Element.Text(f'请确认歌曲名是否输入正确。')),
                     Module.Section(Element.Text(f'当然，不排除是网络问题，如果您已确认歌名输入无误则请重试。')),
                     color='#ff7700')

    else:
        c = Card(Module.Header(Element.Text('【异常】发生了一个未知异常')),
                 Module.Divider(),
                 Module.Section(Element.Text(f'发生了一个未知异常：`{str(type(exc))[8:-2]}`。')),
                 Module.Section(Element.Text(f'异常信息：{exc}')),
                 Module.Section(Element.Text('请重试。如果无法自行解决，请联系开发者。')),
                 color='#dd3333')

    addLog(f'[EXCP]执行命令 {cmd.name} 时发生错误：{str(type(exc))[8:-2]}，错误信息为：{exc}')
    await msg.reply(CardMessage(c), use_quote=False)


default_exc_handler = {Exception: catchException}

