import requests
import json
import sys
from typing import Any

from plugins import TOKEN


API_BASE = 'https://www.kookapp.cn/api/v3/'
HEADERS = {'Authorization': f'Bot {TOKEN}',
           'Content-type': 'application/json;'}
GLOBAL = {}


def commands(cmd: str = 'NoneType',
             *args, **kwargs):

    """Main Function of Debug Panel."""

    def gdef(var_name: str,
             var_value: Any,
             *args, **kwargs):

        """Set Global Variables."""

        if not isinstance(var_name, str): raise Exception
        GLOBAL[var_name] = var_value

    def message(content: str = None,
                target: str = None,
                msg_type: int = 9,
                quote: str = None,
                nonce: str = None,
                temp: str = None,
                template: str = None,
                *args, **kwargs):

        """Send Messages."""

        data = {'target_id': target,
                'content': content.replace('_', ' ')}

        if target is None: data['target_id'] = GLOBAL.get('target_id')
        if msg_type != 9: data |= {'type': msg_type}
        if quote is not None : data |= {'quote': quote}
        if nonce is not None : data |= {'nonce': nonce}
        if temp is not None : data |= {'temp_target_id': temp}
        if template is not None : data |= {'template_id': template}

        if data.get('target_id') is None: raise Exception
        r = requests.post(url=f'{API_BASE}message/create',
                          data=json.dumps(data, ensure_ascii=False),
                          headers=HEADERS)
        content = json.loads(r.content)

        if content['code'] == 0: print('Message Was Sended Successfully.')
        else: print('Something Went Wrong. Code: %d.' % (content["code"]))

    def exit(*args, **kwargs):

        """Bot Offline."""

        r = requests.post(url=f'{API_BASE}user/offline',
                          headers=HEADERS)
        content = json.loads(r.content)

        if content['code'] == 0:
            print('Bot Offline Successfully.')
            sys.exit(0)
        else: print('Something Went Wrong. Code: %d.' % (content["code"]))

    def help(cmd_name: str = None,
             *args, **kwargs):

        """Get Help for Commands."""

    NoneType = lambda *args, **kwargs: None
    result = locals()[cmd](*args, **kwargs)
    return result


def translator(raw: str):

    """Command Translator."""

    splited = raw.split()
    cmd = splited.pop(0).lower()
    buffer = None
    args = []
    kwargs = {}
    for i in splited:
        if i[0] == '-':
            buffer = i[1:]
            continue
        if buffer is None:
            args.append(i)
        else:
            kwargs |= {buffer: i}
            buffer = None
    commands(cmd, *tuple(args), **kwargs)


if __name__ == '__main__':
    while True:
        raw = input()
        translator(raw)

