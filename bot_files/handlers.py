import asyncio
import logging
from datetime import datetime

import aioschedule as schedule
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from bot_files.config import DICT_MENU
from bot_files.logic import groups, send_msg, add_member_team, list_team, delete_member_team, list_team_adm
from bot_files.logic import timed_players, day_x, time_x, days_of_week
from bot_files.models import new_groups

logger = logging.getLogger(__name__)
logger_tread = logging.getLogger()
router = Router()
logger.info("go handlers")


def tread_handler(msg: Message)->None:
    """ Функция собирания в логгер всех сообщений в группе """
    format_tread = (str(msg.chat.id)
                    + '|' + str(msg.from_user.id)
                    + '|' + msg.from_user.full_name
                    + '|' + msg.date.strftime("%M:%S.%f")
                    + '|' + datetime.now().strftime("%M:%S.%f")+'|')
    if msg.forward_date:
        format_tread += msg.forward_date.strftime("%d/%m, %H:%M:%S.%f") + '|'
    # fmt = logging.Formatter(fmt='%(message)s', datefmt=None)
    # str_hdl =logging.StreamHandler()
    # str_hdl.setFormatter(fmt=fmt)
    logger_tread.info(format_tread+' | '+msg.text)
    # logger.info(msg.text)

async def run_scheduler_to_start(chat_id: int)->None:
    """ Функция создания задачи по отслеживанию времени начала голосования """
    logger.info('run schedule')
    job = lambda : send_msg(chat_id)
    schedule.every().day.at(groups[chat_id].voting_time).do(job)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

@router.message(Command("start"))
async def start_handler(msg: Message)->None:
    """ Роутер для приема команды на вывод общей информации о функциональности бота """
    tread_handler(msg)
    if msg.chat.id not in groups.keys():
        new_groups(msg.chat.id, [msg.from_user.id,])
        await msg.answer(DICT_MENU['first_start'])



@router.message(F.text.startswith('+'))
async def add_handler(msg: Message)-> Message|None:
    """ Роутер для приема команды на запись игрока в команду """
    tread_handler(msg)
    name_player = timed_players([msg.from_user.id, msg.from_user.full_name, None, None])
    if not day_x(msg.chat.id) or not time_x(msg.chat.id):
        return await msg.answer(days_of_week(msg.chat.id))
    if msg.text.startswith('++') and name_player[2]!='':
        name_player[2] = msg.text[2:]
        logger.info('add alien player')
    result = add_member_team(msg.chat.id, name_player)
    if not result:
        logger.info('add player')
        if len(groups[msg.chat.id].voting_members) == groups[msg.chat.id].number_team_members:
            return await msg.answer(list_team(msg.chat.id))
    else:
        await msg.answer(f"{name_player[1]}"+result)
        logger.info('NOT add player')

@router.message(F.text.startswith('—')) # здесь тире, а не два минуса!!!
@router.message(F.text.startswith('-')) # здесь минус!!!
async def del_handler(msg: Message)-> None:
    """ Роутер для приема команды вывода(удаления) игрока из формируемой команды """
    tread_handler(msg)
    name_player = timed_players([msg.from_user.id, msg.from_user.full_name,None, None])
    n_p = name_player[1]
    if msg.text.startswith('—'): name_player[2] = n_p = msg.text[1:]  # здесь тире и два минуса тк два
    if msg.text.startswith('--'): name_player[2] = n_p = msg.text[2:]  # минуса преобразуется тире в тг
    bots_answer = delete_member_team(msg.chat.id, name_player)
    await msg.answer(f"{n_p}" + bots_answer)


@router.message(F.text == '?')
async def list_team_handler(msg: Message)-> None:
    """ Роутер для приема команды для вывода актуального списка игроков команды """
    tread_handler(msg)
    list_players = list_team(msg.chat.id)
    await msg.answer(list_players)

@router.message(Command("?"))
@router.message(F.text.lower() == 'help')
@router.message(F.text.lower() == 'помощь')
async def get_help(msg: Message)-> None:
    """ Роутер для приема команды для вывода справочной информации по функционалу бота """
    tread_handler(msg)
    await msg.answer(DICT_MENU['brief_instructions'])

@router.message(F.text.startswith('@@'))
async def admins_handler(msg: Message)-> None:
    """ Роутер для приема админ.команды """
    tread_handler(msg)
    if len(msg.text) == 2: print(str(groups[msg.chat.id].voting_members)+ '\n'+DICT_MENU['admin_menu'])
    if msg.from_user.id in groups[msg.chat.id].admins_ids:
        command_string = msg.text[2:].split('@')
        print(command_string)
        match command_string[0]:
            case 'del': delete_member_team(msg.chat.id, None,int(command_string[1]))
            case 'add': add_member_team(msg.chat.id, [
                int(command_string[1]),
                command_string[2],
                (lambda a: None if len(a)<=3 else a[3])(command_string) ,
                datetime.now().strftime('%H:%M:%S:%f')
            ])
            case '+':
                name_player = timed_players([msg.from_user.id, msg.from_user.full_name, None, None])
                add_member_team(msg.chat.id, name_player)
            case '?': print(list_team_adm(msg.chat.id).replace('], ', '],\n'))
            case _: ...


@router.message()
async def all_handler(msg: Message)->None:
    """ Роутер который отлавливает все остальные сообщения """
    tread_handler(msg)
    if msg.chat.id not in groups and msg.chat.id != msg.from_user.id:
        # groups = new_groups(msg.chat.id, [msg.from_user.id,])
        # print(groups)
        await msg.answer(DICT_MENU['welcoming']+DICT_MENU['first_meting'])
    print("все сообщения")
