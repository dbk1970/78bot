import datetime
import logging

from bot_files.models import MyBotCls
from bot_files.config import WEEK

logger = logging.getLogger(__name__)

def named_players(id_player, full_name_player):
    id_player = id_player
    full_name = full_name_player
    alien_name = None
    player_vote_time = datetime.datetime.now().strftime('%H:%M:%S:%f')
    return [id_player, full_name, alien_name, player_vote_time]

def list_team(bt:MyBotCls):
    list_players = ''
    for n in range(len(bt.voting_members)):
        player = bt.voting_members[n][1]
        if bt.voting_members[n][2]:
            player = bt.voting_members[n][2]+ ' от ' + bt.voting_members[n][1]
        list_players += f'{n+1} - {player}\n'
        if n+1 == bt.number_team_members: list_players += f'-----------------\n'
    if len(list_players) == 0: list_players = bt.dict_menu['team_not_exist']
    logger.info('print list player')
    return list_players

def repeat_member(bt: MyBotCls, name_player: list):
    r_t =None
    for i in range(len(bt.voting_members)):
        if (bt.voting_members[i][0] == name_player[0]
                and bt.voting_members[i][2] == name_player[2]):
            r_t = i
    return r_t

def add_member_team(bt: MyBotCls, name_plyer: list):
    result = bt.dict_menu['team_member_already_exist']
    if not bt.voting_members: add_vip(bt)
    if name_plyer[2] and len(name_plyer[2].replace(' ',''))<2:
        return bt.dict_menu['wrong_command']
    if not repeat_member(bt, name_plyer):
        bt.voting_members.append(name_plyer)
        result = None # в случае успешного добавления ничего не сообщаем
    return result

def add_vip(bt: MyBotCls):
    for i in range(len(bt.vip_team_members)):
        bt.vip_team_members[i] = named_players(bt.vip_team_members[i][0], bt.vip_team_members[i][1])
    bt.voting_members = bt.vip_team_members

def delete_member_team(bt: MyBotCls, name_plyer: list):
    repeat = repeat_member(bt,name_plyer)
    if repeat:
        bt.voting_members.pop(repeat)
        return bt.dict_menu['remove_from_team']
    else:
        return bt.dict_menu['player_not_exist']





def its_time(bt: MyBotCls):
    return datetime.datetime.now().strftime('%H:%M') == bt.voting_time

def day_x(bt: MyBotCls)-> bool:
    return datetime.datetime.isoweekday(datetime.datetime.today()) in bt.day_of_the_week

def time_x(bt: MyBotCls)-> bool:
    print (datetime.datetime.now().strftime('%H:%M:%S')+' | '+bt.voting_time)
    return datetime.datetime.now().strftime('%H:%M:%S') >= bt.voting_time


def days_of_week(bt:MyBotCls)-> str:
     if len(bt.day_of_the_week) == 0 or len(bt.voting_time) == 0:
            answer_not_time = bt.dict_menu['wrong_day']
     else:
         days = ''
         for i in [WEEK[i-1] for i in bt.day_of_the_week]: days+=i+'; '
         answer_not_time = (bt.dict_menu['out_of_time']
                 + days[:-2] + ' в ' + bt.voting_time[:5])
     return answer_not_time

