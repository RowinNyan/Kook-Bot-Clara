import json

from khl import Bot, Event, EventTypes


def events(name: str, *args):

    def debug():
        pass

    return locals().get(name, lambda *args: args)(*args)


def initEvents(bot: Bot):

    @bot.on_event(EventTypes.MESSAGE_BTN_CLICK)
    async def button_click_event(bot: Bot, e: Event):
        value: dict = json.loads(e.body.get('value', '{"event": "NoneType", "args": ()}'))
        NoneType = lambda *args, **kwargs: None
        # Code Here.
        ...
        # Code Here.

