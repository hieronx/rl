searches = {
    # Time: around 1h
    'cp-range': {
        'size': 5,
        'N': { 'min': 100, 'max': 100 },
        'Cp': { 'min': 0.01, 'max': 2.0 },
        'num-configs': 200,
        'plots': [
            {
                'xcol': 'Cp',
                'ycol': 'trueskill_mu',
                'xlabel': 'Cp',
                'ylabel': 'TrueSkill μ-value',
                'linear-regression': False
            }
        ]
    },
    # Time: around 4h (num-configs=50), around 15m (num-configs=25)
    'n-range': {
        'size': 6,
        'N': { 'min': 1, 'max': 5000 },
        'Cp': { 'min': 0.4, 'max': 0.4 },
        'num-configs': 20,
        'plots': [
            {
                'xcol': 'N',
                'ycol': 'trueskill_mu',
                'xlabel': 'N',
                'ylabel': 'TrueSkill μ-value',
                'linear-regression': True
            }
        ]
    },
    'cp-range-6': {
        'size': 6,
        'N': { 'min': 100, 'max': 100 },
        'Cp': { 'min': 0.01, 'max': 2.0 },
        'num-configs': 200,
        'plots': [
            {
                'xcol': 'Cp',
                'ycol': 'trueskill_mu',
                'xlabel': 'Cp',
                'ylabel': 'TrueSkill μ-value',
                'linear-regression': False
            }
        ]
    },
    'cp-range-7': {
        'size': 7,
        'N': { 'min': 100, 'max': 100 },
        'Cp': { 'min': 0.01, 'max': 2.0 },
        'num-configs': 200,
        'plots': [
            {
                'xcol': 'Cp',
                'ycol': 'trueskill_mu',
                'xlabel': 'Cp',
                'ylabel': 'TrueSkill μ-value',
                'linear-regression': False
            }
        ]
    },
    'cp-range-8': {
        'size': 8,
        'N': { 'min': 100, 'max': 100 },
        'Cp': { 'min': 0.01, 'max': 2.0 },
        'num-configs': 200,
        'plots': [
            {
                'xcol': 'Cp',
                'ycol': 'trueskill_mu',
                'xlabel': 'Cp',
                'ylabel': 'TrueSkill μ-value',
                'linear-regression': False
            }
        ]
    },
}