from khl import Bot, Message
from khl.card import Card, CardMessage, Module, Element

from .logger import cmdLogger
from .exceptions import default_exc_handler


def help_command(bot: Bot) -> None:
    @bot.command(name='help',
                 aliases=['帮助', '机器人帮助'],
                 case_sensitive=False,
                 exc_handlers=default_exc_handler)
    @cmdLogger
    async def cmdHelp(msg: Message, *args: str):
        if not args:
            c = Card(Module.Header(Element.Text('Bot 指令帮助')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/help <指令名称或别名>`')),
                     Module.Section(Element.Text('别名：帮助、机器人帮助')),
                     Module.Section(Element.Text('查看 Bot 指令帮助，或查看关于某指令的详细帮助。')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/fortune`')),
                     Module.Section(Element.Text('别名：lucky、今日人品')),
                     Module.Section(Element.Text('查询今日人品。')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/music <歌曲名>`')),
                     Module.Section(Element.Text('别名：点歌')),
                     Module.Section(Element.Text('将指定歌曲加入播放列表中。')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/skip`')),
                     Module.Section(Element.Text('别名：跳过')),
                     Module.Section(Element.Text('跳过当前正在播放的歌曲。')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/setu <表达式>`')),
                     Module.Section(Element.Text('别名：随机涩图、随机色图、来点图图、来点色图、来点涩图')),
                     Module.Section(Element.Text('让 Bot 发送随机涩图，或通过表达式让 Bot 发送指定Tag的涩图。')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/dice [4|6|8|10|12|20|100]`')),
                     Module.Section(Element.Text('别名：扔骰子、掷骰子')),
                     Module.Section(Element.Text('扔出指定面数的骰子，默认掷出六面骰。')),
                     Module.Divider(),
                     Module.Section(Element.Text('`/about`')),
                     Module.Section(Element.Text('别名：关于')),
                     Module.Section(Element.Text('查看关于 Bot 的详细信息。')),
                     Module.Divider(),
                     color='#3498db')
        else:
            arg = ' '.join(args).lower()
            if arg in ['help', '帮助', '机器人帮助']:
                c = Card(Module.Header(Element.Text('指令：/help <指令名称或别名>')),
                         Module.Section(Element.Text('别名：帮助、机器人帮助')),
                         Module.Section(Element.Text('接受参数类型：`None|str`')),
                         Module.Section(Element.Text('查看 Bot 指令帮助，或查看关于某指令的详细帮助。')),
                         color='#3498db')
            elif arg in ['fortune', 'lucky', '今日人品']:
                c = Card(Module.Header(Element.Text('指令：/fortune')),
                         Module.Section(Element.Text('别名：lucky、今日人品')),
                         Module.Section(Element.Text('接受参数类型：`None`')),
                         Module.Section(Element.Text('查询今日人品，返回值为0-100的随机整数，当天某特定用户的数值不变。')),
                         color='#3498db')
            elif arg in ['music', '点歌']:
                c = Card(Module.Header(Element.Text('指令：/music <歌曲名>')),
                         Module.Section(Element.Text('别名：点歌')),
                         Module.Section(Element.Text('接受参数类型：`str|tuple`')),
                         Module.Section(Element.Text('示例：`/music 春日影`')),
                         Module.Section(Element.Text('将指定歌曲加入播放列表中。')),
                         color='#3498db')
            elif arg in ['skip', '跳过']:
                c = Card(Module.Header(Element.Text('指令：/skip')),
                         Module.Section(Element.Text('别名：跳过')),
                         Module.Section(Element.Text('接受参数类型：`None`')),
                         Module.Section(Element.Text('跳过当前正在播放的歌曲。')),
                         color='#3498db')
            elif arg in ['setu', '随机涩图', '随机色图', '来点图图', '来点色图', '来点涩图']:
                c = Card(Module.Header(Element.Text('指令：/setu <表达式>')),
                         Module.Section(Element.Text('别名：随机涩图、随机色图、来点图图、来点色图、来点涩图')),
                         Module.Section(Element.Text('接受参数类型：`None|str|tuple`')),
                         Module.Section(Element.Text('示例：`/setu 原神|明日方舟&白丝|黑丝`')),
                         Module.Section(Element.Text('注1：表达式中的**或运算**比**与运算**的优先级更高，且不支持使用小括号。')),
                         Module.Section(Element.Text('注2：支持的**或运算符**：`|、||、or`，支持的**与运算符**：`&、&&、and`')),
                         Module.Section(Element.Text('让 Bot 发送随机涩图，或通过表达式让 Bot 发送指定Tag的随机涩图。')),
                         Module.Section(Element.Text('此处使用`https://api.lolicon.app/setu/v2`这一api。')),
                         color='#3498db')
            elif arg in ['dice', '扔骰子', '掷骰子']:
                c = Card(Module.Header(Element.Text('指令：/dice [4|6|8|10|12|20|100]')),
                         Module.Section(Element.Text('别名：扔骰子、掷骰子')),
                         Module.Section(Element.Text('接受参数类型：`None|int`')),
                         Module.Section(Element.Text('扔出指定面数的骰子，默认掷出六面骰。')),
                         color='#3498db')
            elif arg in ['about', '关于']:
                c = Card(Module.Header(Element.Text('指令：/about')),
                         Module.Section(Element.Text('别名：关于')),
                         Module.Section(Element.Text('接受参数类型：`None`')),
                         Module.Section(Element.Text('查看关于 Bot 的详细信息。')),
                         color='#3498db')
            else:
                c = Card(Module.Section(Element.Text(f'不存在关于`{arg}`的指令帮助。')),
                         color='#3498db')
        await msg.reply(CardMessage(c), use_quote=False)
