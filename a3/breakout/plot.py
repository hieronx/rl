import matplotlib.pyplot as plt
import pandas as pd


def plot(args):
    plot_max_game_score()
    plot_avg_game_score_by_rb_size()
    plot_epsilon_schedule()

def plot_max_game_score():
    df = pd.read_csv('breakout/output/stats_dropout00_rb005.csv', index_col=None, header=0, delimiter=';')
    ax = df.plot.line(x='game_id', y='max_game_score')
    ax.set_xlabel('Episodes')
    ax.set_ylabel('Max game score')

    fn = 'breakout/output/plot_breakout_max-game-score.png'
    ax.get_figure().savefig(fn)
    print('Saved %s' % fn)

def plot_avg_game_score_by_rb_size():
    files = [
        ('stats_dropout00_rb005', '0.5% replay bufffer, no dropout'),
        ('stats_dropout00_rb25-400k', '25% replay bufffer, no dropout'),
        ('stats_dropout02_rb10', '10% replay bufffer, 20% dropout'),
        ('stats_dropout00_rb10-180k', '10% replay buffer, no dropout')
    ]

    combined_data = []

    for filename, label in files:
        df = pd.read_csv('breakout/output/%s.csv' % filename, index_col=None, header=0, delimiter=';')
        df['dataset'] = label
        combined_data.append(df)

    df = pd.concat(combined_data, axis=0)
    fig, ax = plt.subplots()

    for key, grp in df.groupby(['dataset']):
        ax = grp.plot(ax=ax, kind='line', x='game_id', y='avg_game_score', label=key)

    ax.set_xlabel('Episodes')
    ax.set_ylabel('Average game score')

    fn = 'breakout/output/plot_breakout_avg-game-score.png'
    ax.get_figure().savefig(fn)
    print('Saved %s' % fn)

def plot_epsilon_schedule():
    df = pd.read_csv('breakout/output/stats_dropout00_rb005.csv', index_col=None, header=0, delimiter=';')
    ax = df.plot.line(x='game_id', y='epsilon')
    ax.set_xlabel('Episodes')
    ax.set_ylabel('Epsilon')

    fn = 'breakout/output/plot_breakout_epsilon-schedule.png'
    ax.get_figure().savefig(fn)
    print('Saved %s' % fn)
