from decimal import Decimal
from typing import Tuple

from common.models.enums import Actions


def _cal_reward(hdp_odd, diff_g, dec_odd, _stake):
    reward = 0
    _is_win = False

    if hdp_odd == 0:
        if diff_g == 0:  # stake refund
            reward = 0
            _is_win = False
        elif diff_g > 0:
            reward = _stake * dec_odd
            _is_win = True
        else:
            reward = -_stake
            _is_win = False

    elif hdp_odd == -0.25:
        if diff_g == 0:
            reward = -_stake / 2
            _is_win = False
        elif diff_g > 0:
            reward = _stake * dec_odd
            _is_win = True
        else:
            reward = -_stake
            _is_win = False
    elif hdp_odd == 0.25:
        if diff_g == 0:
            reward = (_stake * dec_odd) / 2  # haft win
            _is_win = True
        elif diff_g > 0:
            reward = _stake * dec_odd
            _is_win = True
        else:
            reward = -_stake
            _is_win = False
    elif hdp_odd == -0.5:
        if diff_g > 0:
            reward = _stake * dec_odd
            _is_win = True
        else:
            reward = -_stake
            _is_win = False
    elif hdp_odd == 0.5:
        if diff_g > 0 or diff_g == 0:
            reward = _stake * dec_odd
            _is_win = True
        else:
            reward = -_stake
            _is_win = False
    elif hdp_odd == -0.75:
        if diff_g == 1:  # win by 1
            reward = (_stake * dec_odd) / 2
            _is_win = True
        elif diff_g >= 2:  # win by +2
            reward = _stake * dec_odd
            _is_win = True
        else:
            reward = -_stake
            _is_win = False
    elif hdp_odd == 0.75:
        if diff_g > 0 or diff_g == 0:
            reward = _stake * dec_odd
            _is_win = True
        elif diff_g == -1:
            reward = -(_stake * dec_odd) / 2
            _is_win = False
        elif diff_g <= -2:
            reward = -_stake
            _is_win = False
    elif hdp_odd == -1:
        if diff_g == 1:
            reward = 0  # stake refund
            _is_win = False
        elif diff_g >= 2:
            reward = _stake * dec_odd
            _is_win = True
        else:
            reward = -_stake
            _is_win = False
    elif hdp_odd == 1:
        if diff_g >= 0:
            reward = _stake * dec_odd
            _is_win = True
        elif diff_g == -1:  # lose by 1
            reward = 0  # stake refund
            _is_win = False
        elif diff_g <= -2:  # lose by 2+
            reward = -_stake
            _is_win = False
    elif hdp_odd == -1.25:
        if diff_g == 1:
            reward = -_stake / 2
            _is_win = False
        elif diff_g >= 2:  # win by 2+
            reward = _stake * dec_odd
            _is_win = True
        else:
            reward = -_stake
            _is_win = False
    elif hdp_odd == 1.25:
        if diff_g >= 0:
            reward = (_stake * dec_odd)
            _is_win = True
        elif diff_g == -1:
            reward = (_stake * dec_odd) / 2
            _is_win = True
        else:
            reward = -_stake
            _is_win = False
    elif hdp_odd == -1.5:
        if diff_g >= 2:  # win by 2+
            reward = _stake * dec_odd
            _is_win = True
        else:
            reward = -_stake
            _is_win = False
    elif hdp_odd == 1.5:
        if diff_g >= 0 or diff_g == -1:  # win or draw or lose by 1
            reward = _stake * dec_odd
            _is_win = True
        else:
            reward = -_stake
            _is_win = False
    elif hdp_odd == -1.75:
        if diff_g == 2:  # win by 2
            reward = (_stake * dec_odd) / 2
            _is_win = True
        elif diff_g >= 3:  # win by 3+
            reward = _stake * dec_odd
            _is_win = True
        else:
            reward = -_stake
            _is_win = False
    elif hdp_odd == 1.75:
        if diff_g >= 0 or diff_g == -1:  # win or draw
            reward = (_stake * dec_odd)
            _is_win = True
        elif diff_g == -2:  # lose by 2
            reward = -_stake / 2
            _is_win = False
        elif diff_g <= -3:  # lose by 3+
            reward = -_stake
            _is_win = False
    elif hdp_odd == -2:
        if diff_g == 2:  # win by 2
            reward = 0  # stake refund
            _is_win = False
        elif diff_g >= 3:  # win by 3+
            reward = _stake * dec_odd
            _is_win = True
        else:
            reward = -_stake
            _is_win = False
    elif hdp_odd == 2:
        if diff_g >= 0 or diff_g == -1:  # win or lose by 1
            reward = _stake * dec_odd
            _is_win = True
        elif diff_g == -2:  # lose by 2
            reward = 0
            _is_win = False
        elif diff_g <= -3:
            reward = -_stake
            _is_win = False

    return reward, _is_win


def calculate_hdp_result(_cap, ft_htg, ft_atg, htg, atg,
                         ht_hdp, odd_dec, at_hdp, action, _stake) -> Tuple[Decimal, float, bool]:
    """

    :param _cap: capital
    :param ft_htg: full time home team goals
    :param ft_atg: full time away team goals
    :param htg: current ht goals
    :param atg: current at goals
    :param ht_hdp: ht decimal. Ex: 1.01
    :param odd_dec: odd decimal: +0.5
    :param at_hdp: at decimal. Ex: 0.8
    :param action: bet on
    :param _stake:
    :return:
    """
    ht_dec_odd = 0
    at_dec_odd = 0
    if odd_dec > 0:
        ht_dec_odd = -abs(odd_dec)
        at_dec_odd = abs(odd_dec)
    elif odd_dec < 0:
        ht_dec_odd = abs(odd_dec)
        at_dec_odd = -abs(odd_dec)

    htg_s = ft_htg - htg
    atg_s = ft_atg - atg
    if action == Actions.BET_H:
        diff_g = htg_s - atg_s
        hdp_odd = ht_dec_odd
        dec_odd = ht_hdp
    else:
        diff_g = atg_s - htg_s
        hdp_odd = at_dec_odd
        dec_odd = at_hdp

    reward, _is_win = _cal_reward(hdp_odd, diff_g, dec_odd, _stake)
    _cap += reward
    return _cap, reward, _is_win
