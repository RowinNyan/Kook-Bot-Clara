from khl import Bot, Message, MessageTypes
from khl.card import Card, CardMessage, Module, Element, Types
import kookvoice

from .globals import NAME, DESCR, VER, DEV, TOKEN
from .exceptions import default_exc_handler, Errors, Warnings
from .logger import cmdLogger
from .lucky import lucky, luckyText
from .image import splitExpr, imgUpload, getImage
from .dice import newDice
from .music import getMusic, findUser, escape_markdown
from .help import help_command
from .debug import debug_command


def initCommands(bot: Bot) -> None:

    @bot.command(name='fortune',
                 aliases=['lucky', '今日人品'],
                 case_sensitive=False,
                 exc_handlers=default_exc_handler)
    @cmdLogger
    async def cmdFortune(msg: Message, *args: str):
        if args: raise Errors.ParameterError('None')
        d_lucky = lucky(msg.author_id)
        await msg.reply(luckyText(d_lucky), use_quote=False)

    @bot.command(name='music',
                 aliases=['点歌'],
                 case_sensitive=False,
                 exc_handlers=default_exc_handler)
    @cmdLogger
    async def cmdMusic(msg: Message, *args: str):
        music_name = ' '.join(args)
        if music_name:
            vid = await findUser(bot, msg.ctx.guild.id, msg.author_id)
            if not vid:
                await msg.reply('请先加入语音频道！', use_quote=False)
            else:
                music_info = await getMusic(bot, music_name)
                player = kookvoice.Player(msg.ctx.guild.id, vid, TOKEN)
                if music_info is None: raise Warnings.MusicSearchWarning(music_name)
                player.add_music(music=music_info.get('url'))
                i_url = await imgUpload(bot, music_info.get('cover'), music_info.get('music_id'))
                music = music_info.get('music_name')
                singer = escape_markdown(music_info.get('singer'))
                album = escape_markdown(music_info.get('album'))
                c = Card(Module.Header(Element.Text(f'已将歌曲 {music} 加入播放列表。')),
                         Module.Divider(),
                         Module.Section(Element.Text(f'**歌手：**{singer}\n**专辑：**{album}\n**时长：**{music_info.get("interval")}'),
                                        Element.Image(src=i_url)),
                         color='#3498db')
                await msg.reply(CardMessage(c), use_quote=False)
        else:
            await msg.reply('歌曲名不能为空！', use_quote=False)

    @bot.command(name='skip',
                 aliases=['跳过'],
                 case_sensitive=False,
                 exc_handlers=default_exc_handler)
    @cmdLogger
    async def cmdSkip(msg: Message, *args: str):
        if args: raise Errors.ParameterError('None')
        player = kookvoice.Player(msg.ctx.guild.id)
        player.skip()
        await msg.reply('歌曲已跳过。', use_quote=False)

    @bot.command(name='setu',
                 aliases=['随机涩图', '随机色图', '来点图图', '来点色图', '来点涩图'],
                 case_sensitive=False,
                 exc_handlers=default_exc_handler)
    @cmdLogger
    async def cmdSetu(msg: Message, *args: str):
        expr = ''.join(args)
        tags = splitExpr(expr)
        img_info = getImage(tags)
        img_intro = f'**图片Pid**：{img_info.get("pid")}\n**图片Tag**：\n{img_info.get("tags")}'
        img_url = await imgUpload(bot, img_info.get('url'), str(img_info.get("pid")))
        await msg.reply(img_url, type=MessageTypes.IMG, use_quote=False)
        await msg.reply(img_intro, use_quote=False)

    @bot.command(name='dice',
                 aliases=['扔骰子', '掷骰子'],
                 case_sensitive=False,
                 exc_handlers=default_exc_handler)
    @cmdLogger
    async def cmdDice(msg: Message, *args: str):
        t = newDice(*args)
        await msg.reply(t, use_quote=False)

    @bot.command(name='about',
                 aliases=['关于'],
                 case_sensitive=False,
                 exc_handlers=default_exc_handler)
    @cmdLogger
    async def cmdAbout(msg: Message, *args: str):
        if args: raise Errors.ParameterError('None')
        c = Card(Module.Header(Element.Text(f'关于 {NAME} Bot')),
                 Module.Divider(),
                 Module.Section(Element.Text(f'{DESCR}', type=Types.Text.PLAIN),
                                Element.Image(src='https://img.kookapp.cn/assets/2024-10/WlUkfIxnn50km0km.png')),
                 Module.Divider(),
                 Module.Section(Element.Text(f'**版本：**{VER}**\n制作：**{DEV}'),
                                Element.Image(src='https://img.kookapp.cn/attachments/2024-10/10/lXwQbUcYOe0dw0dw.jpeg')),
                 color='#3498db')
        await msg.reply(CardMessage(c), use_quote=False)

    help_command(bot)
    debug_command(bot)
