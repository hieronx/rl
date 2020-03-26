import math
from functools import lru_cache

@lru_cache(maxsize=128)
def log_n(num_visits):
    """Calculates the log of the number of visits, this is cached"""
    return math.log(num_visits)

@lru_cache(maxsize=256)
def rave_score(c, rave_k, Cp, ln_N):
    beta = rave_beta(rave_k, c.num_visits)

    amaf_win_rate = amaf_score(c.amaf_reward, c.num_amaf_visits)
    win_rate = c.reward / c.num_visits
    
    return (
        (beta * amaf_win_rate + ((1 - beta) * win_rate)) # RAVE exploitation
        + Cp * math.sqrt((2 * ln_N / c.num_visits)) # UCT exploration
    )

@lru_cache(maxsize=256)
def alpha_amaf_score(c, alpha, Cp, ln_N):
    amaf = amaf_score(c.amaf_reward, c.num_amaf_visits)
    uct = uct_score(c.reward, c.num_visits, Cp, ln_N)
    return alpha * amaf + ((1 - alpha) * uct)

@lru_cache(maxsize=256)
def amaf_score(amaf_reward, num_amaf_visits):
    return amaf_reward / num_amaf_visits if amaf_reward > 0 and num_amaf_visits > 0 else 0.0

@lru_cache(maxsize=256)
def uct_score(reward, num_visits, Cp, ln_N):
    """Calculates the UCT value for the provided parameters"""
    return (reward / num_visits) + Cp * math.sqrt((2 * ln_N / num_visits))

@lru_cache(maxsize=256)
def rave_beta(rave_k, num_visits):
    return math.sqrt(rave_k / (rave_k + 3 * num_visits))