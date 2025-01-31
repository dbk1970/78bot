import logging
from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from bot_files.logic import list_team, add_member_team, delete_member_team, named_players, day_x, time_x, days_of_week
from bot_files.models import MyBotCls

logger = logging.getLogger(__name__)
router = Router()
bt = MyBotCls()
logger.info("go handlers")

def tread_handler(msg: Message):
    format_tread = (str(msg.chat.id)
                    + '|' + str(msg.from_user.id)
                    + '|' + msg.from_user.full_name
                    + '|' + msg.date.strftime("%M:%S.%f")
                    + '|' + datetime.now().strftime("%M:%S.%f")+'|')
    if msg.forward_date:
        format_tread += msg.forward_date.strftime("%d/%m, %H:%M:%S.%f") + '|'
    logger.info(format_tread)
    logger.info(msg.text)

@router.message(Command("start"))
async def start_handler(msg: Message):
    tread_handler(msg)
    await msg.answer(bt.dict_menu['welcoming'])


@router.message(F.text.startswith('+'))
async def add_handler(msg: Message):
    tread_handler(msg)
    name_player = named_players(msg.from_user.id, msg.from_user.full_name)
    if not day_x(bt) or not time_x(bt):
        return await msg.answer(days_of_week(bt))
    if msg.text.startswith('++'):
        name_player[2] = msg.text[2:]
        logger.info('add alien player')
    result = add_member_team(bt,name_player)
    if not result:
        logger.info('add player')
        if len(bt.voting_members) == bt.number_team_members:
            return await msg.answer(list_team(bt))
    else:
        await msg.answer(f"{name_player[1]}"+result)
        logger.info('NOT add player')

@router.message(F.text.startswith('—')) # здесь тире, а не два минуса!!!
@router.message(F.text.startswith('-')) # здесь минус!!!
async def del_handler(msg: Message):
    tread_handler(msg)
    name_player = named_players(msg.from_user.id, msg.from_user.full_name)
    n_p = name_player[1]
    if msg.text.startswith('—'): name_player[2] = n_p = msg.text[1:]  # здесь тире и два минуса тк два
    if msg.text.startswith('--'): name_player[2] = n_p = msg.text[2:]  # минуса преобразуется тире в тг
    bots_answer = delete_member_team(bt, name_player)
    await msg.answer(f"{n_p}" + bots_answer)


@router.message(F.text == '?')
async def list_team_handler(msg: Message):
    tread_handler(msg)
    list_players = list_team(bt)
    await msg.answer(list_players)

@router.message(Command("?"))
@router.message(F.text.lower() == 'help')
@router.message(F.text.lower() == 'помощь')
async def get_help(msg: Message):
    tread_handler(msg)
    await msg.answer(bt.dict_menu['brief_instructions'])

@router.message()
async def all_handler(msg: Message):
    tread_handler(msg)
