import json
from datetime import datetime

from common.agents.a2c_agent import A2CAgent
from common.models.enums import Actions
from common.models.models import Match
from common.strategies.base_strategy import BaseStrategy
from common.strategies.simple_strategy import SimpleStrategy
from logger import init_logger


class BacktestRunner:
    def __init__(self, matches_by_date, strategy: BaseStrategy, **kwargs):
        self.matches_by_date = matches_by_date
        self.logger = init_logger(self.__class__.__name__, show_debug=kwargs.get('debug', True))
        self.strategy = strategy
        self.nb_win = 0
        self.nb_bets = 0

    def run(self):
        for date in self.matches_by_date:
            self.logger.info('--------------------------------------')
            self.logger.info(f'Start bet at {datetime.strptime(date, "%m%d%Y")}')

            for match in self.matches_by_date[date]:
                match = Match(json_data=match)
                step = self.strategy.next(match)
                if step.action != Actions.NO_ACTION:
                    self.nb_bets += 1
                    if step.status == 'Win':
                        self.nb_win += 1

                if step.is_stopped:
                    break
        if self.nb_bets > 0:
            self.logger.info(f'Win {self.nb_win * 100 / self.nb_bets} / {self.nb_bets}')


if __name__ == '__main__':
    agent = A2CAgent(saved_model='saved/A2C_fb-v0_0_test.pkl')
    with open('csv_files/backtest_11282019-12042019.json') as f:
        matches_by_date = json.load(f)
        strategy = SimpleStrategy(agent=agent, max_bets_per_session=15)
        runner = BacktestRunner(matches_by_date=matches_by_date, strategy=strategy)
        runner.run()
