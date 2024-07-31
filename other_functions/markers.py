import datetime
import re

month_to_num: dict[str, str] = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06', 'июля': '07', 'августа': '08', 'сентября': '09',
    'октября': '10', 'ноября': '11', 'декабря': '12'}

def normalize_message(text: str) -> dict[str, str]:
    info: dict = {}
    message_splited = text.split()
    info['year'] = str(datetime.datetime.now().year)
    info['number'] = message_splited[0]
    if int(info['number']) > 31:
        return None
    for elem in message_splited:
        if elem in month_to_num:
            info['month'] = month_to_num[elem]
            info['month_name'] = elem
    info['time'] = ''.join(re.findall(r'\d{2}:\d{2}', text))
    hours, minutes = info['time'].split(':')
    if int(hours) > 23 or int(minutes) > 59:
        return None
    info['text'] = ' '.join(message_splited[4:])
    return info






