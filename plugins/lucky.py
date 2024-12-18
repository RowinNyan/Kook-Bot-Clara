import random


lucky_list: dict[str, int] = dict()

def lucky(user: str) -> int:
    global lucky_list
    lucky_list[user] = lucky_list.get(user, random.randint(0, 100))
    return lucky_list[user]

def luckyText(num: int) -> str:
    text = f'你今天的人品值为：{num}'
    if num == 0:
        text += '？！'
    elif num <= 10:
        text += '……（是百分制哦）'
    elif num <= 50:
        text += '。'
    elif num < 100:
        text += '！'
    else:
        text += '！100！100！'
    return text
