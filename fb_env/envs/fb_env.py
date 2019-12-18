import json
import random
from datetime import datetime
from typing import List, Optional

import gym
from gym import spaces
from gym.utils import seeding

import constants
from common import utils
from common.formulations import calculate_hdp_result
from common.models.enums import Actions
from common.models.models import Match, Bet, OddAsianHDP, Odd1x2, MatchLogRecord
from logger import init_logger


class BookmakerEnv(gym.Env):
    metadata = {'render.modes': ['human', 'system', 'none']}

    def __init__(self, **kwargs):
        self.logger = init_logger(__name__, show_debug=True)
        self.n = kwargs.get('action_size', constants.action_size)
        self.action_space = spaces.Discrete(self.n)
        self.obs_shape = (1, kwargs.get('observation', constants.observation_size))
        self.observation_space = spaces.Box(low=0, high=100, shape=self.obs_shape, dtype='float16')
        self.data_path = kwargs.get('data_path', 'csv_files/train.csv')
        self.matches: List[MatchLogRecord] = []
        self.activate_matches: List[MatchLogRecord] = []

        self.balance = kwargs.get('default_balance', 100)
        self.init_balance = kwargs.get('default_balance', 100)
        self.default_stake = kwargs.get('default_stake', 1)
        self.balance_history = []

        self.in_play_match: Optional[MatchLogRecord] = None
        self.odd_hdp: Optional[OddAsianHDP] = None
        self.odd_1x2: Optional[Odd1x2] = None

        self.current_step = 0
        self.step_left = 0
        self.window_index = 0
        self._init_matches()
        self.seed(kwargs.get('seed', 1))

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action)
        reward = 0
        is_done = False
        action_type = Actions(action)
        stake = self.default_stake
        info_debug = {}

        if action_type == Actions.BET_A or \
                action_type == Actions.BET_H:
            info_debug['bet'] = Bet(match=self.in_play_match,
                                    odd_hdp=self.odd_hdp,
                                    odd_1x2=self.odd_1x2,
                                    action=action_type,
                                    created_time=datetime.now())

            _, reward, is_win = calculate_hdp_result(_cap=self.balance,
                                                     ft_htg=self.in_play_match.home_goals,
                                                     ft_atg=self.in_play_match.away_goals,
                                                     htg=self.odd_hdp['home_goals'],
                                                     atg=self.odd_hdp['away_goals'],
                                                     ht_hdp=self.odd_hdp['ht'],
                                                     odd_dec=self.odd_hdp['dec'],
                                                     at_hdp=self.odd_hdp['at'],
                                                     action=action_type,
                                                     _stake=stake)
            self.balance += reward
            self.balance_history.append({
                'balance': self.balance,
                'profit': reward
            })

        self.current_step += 1
        self.step_left -= 1
        next_state = self._generate_next_state()

        if self.balance <= 0.1 * self.init_balance or self.step_left == 0:
            is_done = True

        return next_state, reward, is_done, info_debug

    def reset(self):
        self.balance = self.init_balance
        self.balance_history = []

        self.in_play_match = None
        self.odd_hdp = None
        self.odd_1x2 = None

        self.current_step = 0

        self.step_left = 100
        if self.window_index >= len(self.matches) - self.step_left - 1:
            self.window_index = 0
        else:
            self.window_index += 1

        self.activate_matches = self.matches[self.window_index: self.window_index + self.step_left]
        return self._generate_next_state()

    def _init_matches(self):
        with open(self.data_path) as f:
            matches = json.load(f)
            for match in matches:
                match = MatchLogRecord(json_data=match)
                if match.home_goals is None or match.away_goals is None:
                    continue
                self.matches.append(match)

            random.shuffle(self.matches)
            print('Loaded {} matches'.format(len(self.matches)))

    def _generate_next_state(self):
        self._pick_match()
        odd_arr = utils.combine_odds_array(self.odd_1x2, self.odd_hdp)
        return utils.generate_env_state(stats=self.in_play_match.stats,
                                        odd=odd_arr, match_time=self.odd_hdp['time'])

    @staticmethod
    def _validate_odd(odd_1x2, odd_hdp):
        if odd_1x2['ht'] == 0 or odd_1x2['draw'] == 0 or odd_1x2['at'] == 0 \
                or odd_hdp['ht'] == 0 or odd_hdp['at'] == 0:
            return False
        return True

    def _pick_match(self):
        try:
            while True:
                match = self.activate_matches.pop()
                if len(match.odds_1x2) == 0 and len(match.odds_hdp) == 0:
                    self.step_left -= 1
                    continue

                if match.odds_hdp[0]['time'] > 0:
                    self.in_play_match = match
                    odd_1x2 = self.in_play_match.odds_1x2[0]
                    odd_hdp = self.in_play_match.odds_hdp[0]
                    if self._validate_odd(odd_1x2, odd_hdp):
                        self.odd_1x2, self.odd_hdp = odd_1x2, odd_hdp
                        break
                    else:
                        self.step_left -= 1
                else:
                    self.activate_matches.pop()
                    self.step_left -= 1
        except:
            return False

    def render(self, mode='human'):
        pass
