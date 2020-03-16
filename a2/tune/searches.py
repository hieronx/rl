searches = {
    'sanity-check': {
        'size': 6,
        'N': { 'min': 1, 'max': 5000 },
        'Cp': { 'min': 1.4, 'max': 1.4 },
        'num-configs': 0,
        'plots': [
            {
                'xcol': 'N',
                'ycol': 'trueskill_mu',
                'xlabel': 'N',
                'ylabel': 'TrueSkill μ-value',
            }
        ]
    },
    'cp-range': {
        'size': 5,
        'N': { 'min': 150, 'max': 150 },
        'Cp': { 'min': 0.01, 'max': 1.0 },
        'num-configs': 50,
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