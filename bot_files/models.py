import logging
from dataclasses import dataclass, field

from bot_files.config import *

# @dataclass
# class TeamMember:
#

@dataclass
class MyBotCls:
    day_of_the_week = DAY_OF_THE_WEEK_DEFAULT
    voting_time = VOTING_TIME_DEFAULT
    voting_members: list[list] = field(default_factory=list)
    number_team_members = NUMBERS_TEAM_MEMBERS
    vip_team_members = VIP_TEAM_MEMBERS
    end_countdown: bool = False
    dict_menu = DICT_MENU
    
