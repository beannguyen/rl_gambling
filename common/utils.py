import constants
import numpy as np

from common.models.enums import Actions


def str2action(action_str):
    if action_str == 'Actions.BET_A':
        return Actions.BET_A
    if action_str == 'Actions.BET_H':
        return Actions.BET_H
    if action_str == 'Actions.NO_ACTION':
        return Actions.NO_ACTION


def str2balance(s):
    s = s.replace('VND ', '')
    s = s.split('.')[0]
    if ',' in s:
        s = s.replace(',', '')
    return float(s)


def cal_dec_odds(odds_str):
    try:
        sep = '/'
        if sep in odds_str:
            arr = odds_str.split(sep)
            return (float(arr[0]) + float(arr[1])) / 2
        else:
            return float(odds_str)
    except Exception as e:
        raise e


def time_from_str(time_str):
    if '1H' in time_str:
        time_str = time_str.replace('1H', '')
    elif '2H' in time_str:
        time_str = time_str.replace('2H', '')
    elif time_str == 'HT':
        time_str = '45:00'

    time = time_str.split(':')[0]
    return int(time)


def combine_odds_array(odd_1x2, odd_hdp):
    match_progress = odd_hdp['time'] / 90
    diff_g = odd_hdp['home_goals'] - odd_hdp['away_goals']

    return [diff_g, 1 / odd_1x2['ht'], 1 / odd_1x2['draw'], 1 / odd_1x2['at'], 1 / (
            odd_hdp['ht'] + 1), odd_hdp['dec'], 1 / (1 + odd_hdp['at']), match_progress]


def generate_env_state(stats, odd, match_time=90):
    stats = [
        stats['corner']['home'] / match_time,
        stats['corner']['away'] / match_time,
        stats['yellow_card']['home'] / match_time,
        stats['yellow_card']['away'] / match_time,
        stats['red_card']['home'] / match_time,
        stats['red_card']['away'] / match_time,
        stats['shots']['home'] / match_time,
        stats['shots']['away'] / match_time,
        stats['shots_on_goals']['home'] / match_time,
        stats['shots_on_goals']['away'] / match_time,
        stats['attack']['home'] / match_time,
        stats['attack']['away'] / match_time,
        stats['dangerous_attack']['home'] / match_time,
        stats['dangerous_attack']['away'] / match_time,
        stats['possession']['home'],
        stats['possession']['away'],
    ]
    obs_shape = (1, constants.observation_size)
    state = np.concatenate((stats, odd), axis=0)
    return state.reshape(obs_shape)
