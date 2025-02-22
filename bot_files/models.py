from dataclasses import dataclass, field
import yaml

from bot_files.config import (DAY_OF_THE_WEEK_DEFAULT, VOTING_TIME_DEFAULT,
                              NUMBERS_TEAM_MEMBERS_DEFAULT, VIP_TEAM_MEMBERS_DEFAULT, PATH_YAML)


@dataclass
class MyBotCls:
    day_of_the_week: list[int]= field(default_factory=list)
    voting_time: str = ''
    voting_members: list[list]= field(default_factory=list)
    number_team_members: int = 12
    vip_team_members: list[list[int | str | None]]|None = field(default_factory=list)
    admins_ids: list[int] = field(default_factory=list)

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"day_of_the_week={self.day_of_the_week}, "
                f"voting_time={self.voting_time}, "
                f"voting_members={self.voting_members},"
                f"number_team_members={self.number_team_members}, "
                f"vip_team_members={self.vip_team_members}, "
                f"admins_ids={self.admins_ids})")


def new_groups(id_groups: int,admins_ids: list[int])-> dict[int, MyBotCls]:
    return {id_groups: MyBotCls(day_of_the_week=DAY_OF_THE_WEEK_DEFAULT,
                                              voting_time=VOTING_TIME_DEFAULT,
                                              voting_members=[],
                                              number_team_members=NUMBERS_TEAM_MEMBERS_DEFAULT,
                                              vip_team_members=VIP_TEAM_MEMBERS_DEFAULT,
                                              admins_ids=admins_ids)}

def write_groups(group: dict[int,MyBotCls]) -> None:
    with open(PATH_YAML, 'w+', encoding='utf-8') as write_groups_file:
        write_groups_file.write(yaml.dump(group, allow_unicode=True))

def read_groups()-> dict[int,MyBotCls]:
    with open(PATH_YAML, 'r+', encoding='utf-8') as read_groups_file:
        group = yaml.load(read_groups_file, Loader=yaml.Loader)
    return group
