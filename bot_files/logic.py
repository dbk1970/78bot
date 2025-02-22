import logging
import os.path
from datetime import datetime, date


from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot_files.models import MyBotCls, new_groups
from bot_files.config import *


logger = logging.getLogger(__name__)
bot = Bot(token=AUTH_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
groups = new_groups(GROUP_CHAT_ID_DEFAULT, [ADMINS_IDS_DEFAULT_1, ADMINS_IDS_DEFAULT_2])

def timed_players(name_player)->list[str|None]:
    """ Функция формирования времени записи в команду в списке общих данных об игроке
    """
    name_player[3] = datetime.now().strftime('%H:%M:%S:%f')
    print(name_player)
    return name_player

def list_team(chat_id)->str:
    """ Функция формирования актуального списка команды """
    list_players = ''
    for n in range(len(groups[chat_id].voting_members)):
        player = groups[chat_id].voting_members[n][1]
        if groups[chat_id].voting_members[n][2]:
            player = (groups[chat_id].voting_members[n][2]+ ' от '
                      + groups[chat_id].voting_members[n][1])
        list_players += f'{n+1} - {player}\n'
        if n+1 == groups[chat_id].number_team_members: list_players += f'-----------------\n'
    if len(list_players) == 0: list_players = DICT_MENU['team_not_exist']
    logger.info('print list player')
    return list_players

def list_team_adm(chat_id)->str:
    return str(groups[chat_id].voting_members[1])+'--'+str(groups[chat_id].voting_members[3])

def repeat_member(chat_id: int, name_player: list)->int:
    """ Функция формирования проверки наличия игрока в команде и определение его номера в списке """
    r_t =None
    for i in range(len(groups[chat_id].voting_members)):
        if (groups[chat_id].voting_members[i][0] == name_player[0]
                and groups[chat_id].voting_members[i][2] == name_player[2]):
            r_t = i
    return r_t

def add_member_team(chat_id: int, name_plyer: list)-> str|None:
    """ Функция добавления игрока в список команды """
    result = DICT_MENU['team_member_already_exist']
    # При появлении первого игрока - добавляем VIPов в список команды
    if not groups[chat_id].voting_members: add_vip(chat_id)
    # Проверяем правильность ввода имени чужого игрока - должно быть минимум 2 знака
    if name_plyer[2] and len(name_plyer[2].replace(' ',''))<2:
        return DICT_MENU['wrong_command']
    # Проверяем на наличие игрока в команде, чтоб второй раз не записался
    if not repeat_member(chat_id, name_plyer):
        groups[chat_id].voting_members.append(name_plyer)
        result = None # В случае успешного добавления ничего не сообщаем
    return result

def add_vip(chat_id: int)-> None:
    """ Функция автоматического добавления VIP игроков в список команды """
    for i in range(len(groups[chat_id].vip_team_members)):
        groups[chat_id].vip_team_members[i] = timed_players([
            groups[chat_id].vip_team_members[i][0],
            groups[chat_id].vip_team_members[i][1],
            None,
            None])
    groups[chat_id].voting_members = groups[chat_id].vip_team_members[:]

def delete_member_team(chat_id: int, name_plyer: list|None, player_number=None) -> str:
    """ Функция удаления игрока из списка команды """
    if player_number: repeat_ = player_number
    else: repeat_ = repeat_member(chat_id, name_plyer)
    if repeat_:
        groups[chat_id].voting_members.pop(repeat_)
        return DICT_MENU['remove_from_team']
    else:
        return DICT_MENU['player_not_exist']

def its_time(chat_id: int)-> bool:
    """ Функция проверки времени начала голосования, для старта голосования """
    return datetime.now().strftime('%H:%M') == groups[chat_id].voting_time

def day_x(chat_id: int)-> bool:
    """ Функция проверки правильности дня недели для начала голосования """
    print(groups)
    return date.today().isoweekday() in groups[chat_id].day_of_the_week

def time_x(chat_id: int)-> bool:
    """ Функция проверки времени начала голосования, для последующего голосования """
    print(groups)
    return datetime.now().strftime('%H:%M:%S') >= groups[chat_id].voting_time


def days_of_week(chat_id: int)-> str:
    """ Функция реакции бота на неверные день недели или время начала голосования """
    if len(groups[chat_id].day_of_the_week) == 0 or len(groups[chat_id].voting_time) == 0:
        bot_answer = DICT_MENU['wrong_day']
    else:
        days = ''
        for day in [WEEK[n-1] for n in groups[chat_id].day_of_the_week]:
            print()
            days+=day+'; '
        bot_answer = (DICT_MENU['out_of_time']+ days[:-2] + ' в ' + groups[chat_id].voting_time)
    return bot_answer


async def send_msg(chat_id: int):
    """ Функция произведение старта голосования и включение клавиатуры для голосования """
    print('start in - ' + datetime.now().strftime('%H:%M:%S:%f'))
    if day_x(chat_id):
        btn_1 = KeyboardButton(text="+", callback_data="fgh")
        btn_2 = KeyboardButton(text="?", callback_data="?")
        btn_3 = KeyboardButton(text="-", callback_data="-")
        builder = ReplyKeyboardBuilder()
        builder.add(btn_1, btn_2, btn_3)
        builder.adjust(1,2)
        kb = builder.as_markup(resize_keyboard=True, one_time_keyboard=False)
        await bot.send_message(chat_id=chat_id,
                               text=DICT_MENU['start'],
                               reply_markup=kb,
                               reply_to_message_id=None)

