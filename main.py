import asyncio

from khl import Bot
import kookvoice

from plugins import (
    TOKEN,
    initCommands,
    initCrons,
    initEvents,
    addLog
)


bot = Bot(token=TOKEN)
kookvoice.set_ffmpeg('.\\ffmpeg\\ffmpeg.exe')
kookvoice.configure_logging(enabled=False)

@bot.on_startup
async def botInit(bot: Bot):
    addLog(f'[MAIN]Bot已开启')
    initCommands(bot)
    initCrons(bot)
    initEvents(bot)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(bot.start(), kookvoice.start()))
    loop.close()
