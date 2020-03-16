searches = {
    'cp-range': {
        'size': 5,
        'N': { 'min': 100, 'max': 100 },
        'Cp': { 'min': 0.01, 'max': 2.0 },
        'num-configs': 100,
        'plots': [
            {
                'xcol': 'Cp',
                'ycol': 'trueskill_mu',
                'xlabel': 'Cp',
                'ylabel': 'TrueSkill μ-value'
            }
        ]
    },
    'n-range': {
        'size': 5,
        'N': { 'min': 1, 'max': 10000 },
        'Cp': { 'min': 1.4, 'max': 1.4 },
        'num-configs': 50,
        'plots': [
            {
                'xcol': 'N',
                'ycol': 'trueskill_mu',
                'xlabel': 'N',
                'ylabel': 'TrueSkill μ-value'
            }
        ]
    },
    'n-vs-cp': {
        'size': 5,
        'N': { 'min': 1, 'max': 10000 },
        'Cp': { 'min': 0.5, 'max': 2.0 },
        'num-configs': 100,
        'plots': [
            {
                'xcol': 'N',
                'ycol': 'Cp',
                'xlabel': 'N',
                'ylabel': 'Cp'
            }
        ]
    }
}