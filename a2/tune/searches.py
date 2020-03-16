searches = {
    'sanity-check': {
        'baseline': { 'N': 100, 'Cp': 1.4 },
        'size': 6,
        'N': { 'min': 1, 'max': 5000 },
        'Cp': { 'min': 1.4, 'max': 1.4 },
        'num-configs': 0,
        'confidence-threshold': 1.0,
        'plots': [
            {
                'create': lambda df: df.plot(x='N', y='config_mu', kind='scatter', figsize=(8,5)),
                'xlabel': 'N',
                'ylabel': 'TrueSkill μ-value'
            }
        ]
    },
    'cp-range': {
        'baseline': { 'N': 500, 'Cp': 1.4 },
        'size': 5,
        'N': { 'min': 5000, 'max': 5000 },
        'Cp': { 'min': 0.5, 'max': 2.0 },
        'num-configs': 50,
        'confidence-threshold': 0.5,
        'plots': [
            {
                'create': lambda df: df.plot(x='Cp', y='config_mu', kind='scatter', figsize=(8,5)),
                'xlabel': 'Cp',
                'ylabel': 'TrueSkill μ-value'
            }
        ]
    },
    'n-range': {
        'baseline': { 'N': 100, 'Cp': 1.4 },
        'size': 5,
        'N': { 'min': 1, 'max': 10000 },
        'Cp': { 'min': 1.4, 'max': 1.4 },
        'num-configs': 50,
        'confidence-threshold': 0.5,
        'plots': [
            {
                'create': lambda df: df.plot(x='N', y='config_mu', kind='scatter', figsize=(8,5)),
                'xlabel': 'N',
                'ylabel': 'TrueSkill μ-value'
            }
        ]
    },
    'n-vs-cp': {
        'baseline': { 'N': 100, 'Cp': 1.4 },
        'size': 5,
        'N': { 'min': 1, 'max': 10000 },
        'Cp': { 'min': 0.5, 'max': 2.0 },
        'num-configs': 100,
        'confidence-threshold': 0.5,
        'plots': [
            {
                'create': lambda df: df.plot(x='N', y='Cp', kind='scatter', figsize=(8,5)),
                'xlabel': 'N',
                'ylabel': 'Cp'
            }
        ]
    }
}