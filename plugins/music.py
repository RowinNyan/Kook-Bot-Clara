import requests
import json
import re
import os

from khl import Bot

from .exceptions import Errors


QQMUSIC_SEARCH_API = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p=1&w='
QQMUSIC_CLIENT_SONG_API = 'https://u.y.qq.com/cgi-bin/musicu.fcg'
QQMUSIC_SONG_BASICURL = 'http://dl.stream.qqmusic.qq.com/'
QQMUSIC_SONG_COVER = 'http://y.qq.com/music/photo_new/T002R300x300M000{id}.jpg'


def secToTime(second: int) -> str:
    min = second // 60
    sec = second % 60
    return '%02d:%02d' % (min, sec)

def escape_markdown(text):
    markdown_chars = r'[*_`\>\#\[\]\(\)\\|\!]'
    escaped_text = re.sub(markdown_chars, r'\\\g<0>', text)
    return escaped_text

async def searchMusic(music_name: str) -> list[dict[str, str]]:
    output = list()
    r = requests.get(url=f'{QQMUSIC_SEARCH_API}{music_name}')
    content: dict = json.loads(r.content.decode('utf-8')[9:-1])
    if content.get('code', -1) == 0:
        for m in content['data']['song']['list']:
            music_info: dict = m
            singer = str()
            for s in music_info.get('singer', [{'name': '未知歌手'}]):
                singer += s['name'] + '/'
            singer = singer[:-1]
            output.append({
                'music_name': music_info.get('songname', '未知歌曲'),
                'music_id': music_info.get('songmid', ''),
                'singer': singer,
                'interval': secToTime(music_info.get('interval', 0)),
                'album_name': music_info.get('albumname', '未知专辑'),
                'album_id': music_info.get('albummid', '')
            })
        return output
    else:
        raise Errors.ResponseError(content.get('code', -1))

async def getMusic(bot: Bot, music_name: str) -> dict[str, str]:
    music_list = await searchMusic(music_name)
    for music_info in music_list:
        data = {
            'vkey.GetVkeyServer': {
            'method': 'CgiGetVkey',
            'module': 'vkey.GetVkeyServer',
            'param': {
                    'guid': '0',
                    'songmid': [
                        music_info['music_id']
                    ],
                    'uin': '0'
                }
            }
        }
        cookies: str = ''
        if os.path.exists('.\\config\\qqmusic_cookie'):
            with open('.\\config\\qqmusic_cookie', 'r', encoding='utf-8') as file:
                cookies += ''.join([line.strip() for line in file])
        r = requests.post(url=QQMUSIC_CLIENT_SONG_API,
                          data=json.dumps(data, ensure_ascii=False),
                          headers={'Cookie': cookies})
        content: dict = json.loads(r.content)
        if content.get('code', -1) == 0:
            purl = content['vkey.GetVkeyServer']['data']['midurlinfo'][0]['purl']
            if purl:
                music_url = QQMUSIC_SONG_BASICURL + purl
                kwargs = {'id': music_info['album_id']}
                cover_url = QQMUSIC_SONG_COVER.format(**kwargs)
                return {
                    'music_name': music_info['music_name'],
                    'music_id': music_info['music_id'],
                    'singer': music_info['singer'],
                    'interval': music_info['interval'],
                    'album': music_info['album_name'],
                    'url': music_url,
                    'cover': cover_url
                }

async def findUser(bot: Bot, gid: str, aid: str) -> str:
    voice_channel_ = await bot.client.gate.request('GET', 'channel-user/get-joined-channel',
                                                   params={'guild_id': gid, 'user_id': aid})
    voice_channel = voice_channel_["items"]
    if voice_channel:
        vcid = voice_channel[0]['id']
        return vcid
