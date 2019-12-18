from datetime import datetime
from typing import List, Optional

import numpy as np
from dateutil.parser import parse

from common.models.enums import Actions


class Odd1x2(object):
    def __init__(self, ht: float,
                 draw: float,
                 at: float,
                 time: int,
                 home_goals: int,
                 away_goals: int):
        self.ht = ht
        self.draw = draw
        self.at = at
        self.time = time
        self.home_goals = home_goals
        self.away_goals = away_goals


class OddAsianHDP(object):
    def __init__(self, ht: float,
                 dec: float,
                 at: float,
                 time: int,
                 home_goals: int,
                 away_goals: int):
        self.ht = ht
        self.dec = dec
        self.at = at
        self.time = time
        self.home_goals = home_goals
        self.away_goals = away_goals


class Team(object):
    def __init__(self, t_id: int, name: str):
        self.t_id = t_id
        self.name = name


class MatchStats(object):
    def __init__(self,
                 corner=None,
                 yellow_card=None,
                 red_card=None,
                 shots=None,
                 shots_on_goals=None,
                 attack=None,
                 dangerous_attack=None,
                 possession=None,
                 json_data=None):
        if json_data is None:
            self.corner = corner
            self.yellow_card = yellow_card
            self.red_card = red_card
            self.shots = shots
            self.shots_on_goals = shots_on_goals
            self.attack = attack
            self.dangerous_attack = dangerous_attack
            self.possession = possession
        else:
            self.__dict__ = json_data


class Match(object):
    def __init__(self,
                 m_id: np.int64 = None,
                 league_id: int = None,
                 home_team: Team = None,
                 away_team: Team = None,
                 time: datetime = None,
                 state=None,
                 home_goals: int = None,
                 away_goals: int = None,
                 odd_3in1: bool = None,
                 session: str = None,
                 stats: MatchStats = None,
                 odds_1x2: List[Odd1x2] = None,
                 odds_hdp: List[OddAsianHDP] = None,
                 json_data: dict = None):
        if json_data is not None:
            self._serialize(json_data)
            self.time = parse(self.time)
        else:
            self.m_id = m_id
            self.league_id = league_id
            self.home_team = home_team
            self.away_team = away_team
            self.time = time
            self.state = state
            self.home_goals = home_goals
            self.away_goals = away_goals
            self.odd_3in1 = odd_3in1
            self.session = session
            self.stats = stats
            self.odds_1x2 = odds_1x2
            self.odds_hdp = odds_hdp

    def _serialize(self, data):
        self.__dict__ = data

    def to_dict(self):
        return {
            'm_id': self.m_id,
            'league_id': self.league_id,
            'home_team': self.home_team.__dict__,
            'away_team': self.away_team.__dict__,
            'time': self.time,
            'state': self.state,
            'home_goals': self.home_goals,
            'away_goals': self.away_goals,
            'odd_3in1': self.odd_3in1,
            'session': self.session,
            'stats': self.stats.__dict__ if self.stats is not None else None,
            'odds_1x2': [odd.__dict__ for odd in self.odds_1x2] if self.odds_1x2 is not None else [],
            'odds_hdp': [odd.__dict__ for odd in self.odds_hdp] if self.odds_hdp is not None else []
        }


class MatchLogRecord(object):
    def __init__(self,
                 m_id: np.int64 = None,
                 league_id: int = None,
                 home_team: Team = None,
                 away_team: Team = None,
                 time: datetime = None,
                 state=None,
                 home_goals: int = None,
                 away_goals: int = None,
                 odd_3in1: bool = None,
                 session: str = None,
                 stats: MatchStats = None,
                 odds_1x2: List[Odd1x2] = None,
                 odds_hdp: List[OddAsianHDP] = None,
                 minutes: int = None,
                 created_at: Optional[datetime] = None,
                 json_data: dict = None):
        if json_data is not None:
            self._serialize(json_data)
        else:
            self.m_id = m_id
            self.league_id = league_id
            self.home_team = home_team
            self.away_team = away_team
            self.time = time
            self.state = state
            self.home_goals = home_goals
            self.away_goals = away_goals
            self.odd_3in1 = odd_3in1
            self.session = session
            self.stats = stats
            self.odds_1x2 = odds_1x2
            self.odds_hdp = odds_hdp
            self.minutes = minutes
            self.created_at = created_at

    def _serialize(self, data):
        self.__dict__ = data

    def to_dict(self):
        return {
            'm_id': self.m_id,
            'league_id': self.league_id,
            'home_team': self.home_team.__dict__,
            'away_team': self.away_team.__dict__,
            'time': self.time,
            'state': self.state,
            'home_goals': self.home_goals,
            'away_goals': self.away_goals,
            '3in1': self.odd_3in1,
            'session': self.session,
            'stats': self.stats.__dict__ if self.stats is not None else None,
            'odds_1x2': [odd.__dict__ for odd in self.odds_1x2] if self.odds_1x2 is not None else [],
            'odds_hdp': [odd.__dict__ for odd in self.odds_hdp] if self.odds_hdp is not None else [],
            'minute': self.minutes,
            'created_at': self.created_at
        }


class Bet(object):
    def __init__(self,
                 match,
                 odd_1x2: Odd1x2,
                 odd_hdp: OddAsianHDP,
                 action: Actions,
                 created_time: datetime):
        self.match = match
        self.odd_1x2 = odd_1x2
        self.odd_hdp = odd_hdp
        self.action = action
        self.created_time = created_time


class Step(object):
    action: Actions
    match_id: int
    profit: float
    status: str
    is_stopped: bool
    bet_data: dict

    def __init__(self, action: Actions = Actions.NO_ACTION,
                 profit: float = 0,
                 match_id: int = None,
                 status: str = None,
                 bet_data: dict = None,
                 is_stopped: bool = False):
        self.action = action
        self.profit = profit
        self.status = status
        self.match_id = match_id
        self.bet_data = bet_data
        self.is_stopped = is_stopped
