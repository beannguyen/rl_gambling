from datetime import timedelta, datetime
from typing import List, Optional

from dateutil.parser import parse

from common.strategies.base_strategy import BaseStrategy
from common.formulations import calculate_hdp_result
from common.models.models import Match, Step, Bet
from common.utils import generate_env_state, combine_odds_array
from common.models.enums import Actions
from logger import init_logger


class SimpleStrategy(BaseStrategy):
    """

    Parameters:
    :param init_balance (double): Init account balance for each running session
    :param max_bets_per_session (int): The idea is after 'max_bets_per_session' bets, we will check the account balance
    to decide to stop loss or take profit or continue to bet.
    The risk probability will be distributed to 'max_bets_per_session' bets.
    :param tp_pct (float): percentage to take profit
    :param sl_pct (float): percentage to stop loss
    :return:
    """

    def __init__(self, agent, init_balance=1000000, max_bets_per_session=5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = init_logger(self.__class__.__name__, show_debug=kwargs.get('debug', True))
        self.agent = agent
        self.init_balance = init_balance
        self.balance = init_balance
        self.max_bets_per_session = max_bets_per_session
        self.pending_bet_count = 0
        self.pending_bets: List[Bet] = []
        # won't place bet until the last bet finished
        self.pending_bet_time: Optional[datetime] = None
        self.win_nb = 0
        self.draw_nb = 0
        self.total_bets = 0

        # take profit and stop loss
        self.tp_pct = kwargs.get('tp_pct', 0.2)
        self.sl_pct = kwargs.get('sl_pct', 0.03)
        self.restricted_odds = [0, .25]

    @staticmethod
    def _get_hdp_odds(odds_hdp, minute):
        for i, odd in enumerate(odds_hdp):
            if (i + 1 >= len(odds_hdp) - 1 and minute >= odds_hdp[i]['time']) or \
                    (i + 1 <= len(odds_hdp) - 1 and odds_hdp[i + 1]['time'] >= minute >= odds_hdp[i]['time']):
                return odd

    def _get_bet_status(self, profit):
        if profit > 0:
            status = 'Win'
            self.win_nb += 1
        elif profit == 0:
            status = 'Draw'
            self.draw_nb += 1
        else:
            status = 'Lose'
        return status

    def _log_bet(self, match, odd_hdp, action, stake, profit, status):
        self.logger.info('{} ${} on match {} vs {}'
                         .format(status,
                                 profit,
                                 match.home_team['name'],
                                 match.away_team['name']))

        self.logger.info(f'At {odd_hdp["time"]}m')
        self.logger.info('{} {} {}'.format(odd_hdp['ht'], odd_hdp['dec'], odd_hdp['at']))
        self.logger.info('Bet on {}, {} - {}'.format(action,
                                                     odd_hdp['home_goals'], odd_hdp['away_goals']))
        self.logger.info('Full time result {}-{}'.format(match.home_goals, match.away_goals))
        self.logger.info('Stake {}'.format(stake))
        self.logger.info('Account balance {}'.format(self.balance))
        self.logger.info('------------------------------------')

    def prenext(self):
        pass

    def _take_action(self, match: Match) -> Step:
        step = Step()
        odds_1x2, odds_hdp = match.odds_1x2, match.odds_hdp
        for odd_1x2 in odds_1x2:
            try:
                odd_hdp = self._get_hdp_odds(odds_hdp, odd_1x2['time'])
                if odd_hdp is None:
                    print('odd not found')
                    continue

                odd = combine_odds_array(odd_1x2, odd_hdp)
                if odd is None:
                    continue

                if 65 >= odd_hdp['time']:
                    continue

                if abs(odd_hdp['dec']) in self.restricted_odds:
                    continue

                state = generate_env_state(match.stats, odd)
                action = Actions(self.agent.predict(state))
                if action != Actions.NO_ACTION:
                    stake = self.balance * 0.01
                    _, profit, is_win = calculate_hdp_result(_cap=self.balance,
                                                             ft_htg=match.home_goals,
                                                             ft_atg=match.away_goals,
                                                             htg=odd_hdp['home_goals'],
                                                             atg=odd_hdp['away_goals'],
                                                             ht_hdp=odd_hdp['ht'],
                                                             odd_dec=odd_hdp['dec'],
                                                             at_hdp=odd_hdp['at'],
                                                             action=action,
                                                             _stake=stake)
                    # calc account balance
                    self.balance += profit

                    # print log
                    status = self._get_bet_status(profit)
                    self._log_bet(match, odd_hdp, action,
                                  stake, profit, status)

                    # init new bet
                    self.pending_bets.append(Bet(match=match,
                                                 odd_1x2=odd_1x2,
                                                 odd_hdp=odd_hdp,
                                                 action=action,
                                                 created_time=match.time + timedelta(
                                                     minutes=odd_hdp['time'])))

                    self.total_bets += 1
                    self.pending_bet_count += 1
                    step.action = action
                    step.profit = profit
                    step.status = status
                    break
            except Exception as e:
                self.logger.error(e)

        return step

    def next(self, match: Match) -> Step:
        if self.pending_bet_count < self.max_bets_per_session:
            return self._take_action(match)
        else:
            # if self.pending_bet_time is None:
            #     # set the pending time to 50m, usually we place a bet at 50', need 50' to finish
            #     # the last bet.
            #     if len(self.pending_bets) > 0:
            #         self.pending_bet_time = self.pending_bets[-1].match.time + timedelta(minutes=50)
            #
            # elif match.time >= self.pending_bet_time:
            #     if self.balance <= self.init_balance - (self.init_balance * self.sl_pct):
            #         self.logger.info('Stop loss executed')
            #         self.reset()
            #         return Step(is_stopped=True)
            #
            #     if self.balance >= self.init_balance + (self.init_balance * self.tp_pct):
            #         self.logger.info('Take profit executed')
            #         self.reset()
            #         return Step(is_stopped=True)
            #
            #     # assume all bet finished, we reset and start new session
            #     self.reset()
            #     self.next(match)
            self.reset()
            return Step(is_stopped=True)

    def reset(self):
        self.init_balance = self.balance
        self.pending_bet_count = 0
        self.pending_bets = []
        self.pending_bet_time = None
