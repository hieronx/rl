import matplotlib.pyplot as plt
import pandas as pd


def plot(args):
    plot_max_game_score()
    plot_replay_buffer_comparison()
    plot_dropout_comparison()
    plot_update_frequency_comparison()
    plot_epsilon_schedule()

def plot_max_game_score():
    df = pd.read_csv('breakout/output/stats_dropout00_rb005.csv', index_col=None, header=0, delimiter=';')
    ax = df.plot.line(x='game_id', y='max_game_score')
    ax.set_xlabel('Episodes')
    ax.set_ylabel('Max game score')

    fn = 'breakout/output/plot_breakout_max-game-score.png'
    ax.get_figure().savefig(fn)
    print('Saved %s' % fn)

def plot_replay_buffer_comparison():
    files = [
        ('stats_dropout00_rb005', '0.5% replay bufffer'),
        ('stats_dropout00_rb025', '2.5% replay buffer'),
        ('stats_dropout00_rb10', '10% replay buffer'),
        ('stats_dropout00_rb25', '25% replay bufffer')
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

    fn = 'breakout/output/plot_breakout_replay-buffer.png'
    ax.get_figure().savefig(fn)
    print('Saved %s' % fn)

def plot_dropout_comparison():
    files = [
        ('stats_dropout02_rb10', '20% dropout'),
        ('stats_dropout00_rb10', 'No dropout')
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

    fn = 'breakout/output/plot_breakout_dropout.png'
    ax.get_figure().savefig(fn)
    print('Saved %s' % fn)

def plot_update_frequency_comparison():
    files = [
        ('stats_dropout00_rb005_uf1', 'Update frequency 1'),
        ('stats_dropout00_rb005', 'Update frequency 4')
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

    fn = 'breakout/output/plot_breakout_update-frequency.png'
    ax.get_figure().savefig(fn)
    print('Saved %s' % fn)

def plot_epsilon_schedule():
    df = pd.read_csv('breakout/output/stats_dropout02_rb10.csv', index_col=None, header=0, delimiter=';')
    ax = df.plot.line(x='game_id', y='epsilon')
    ax.set_xlabel('Episodes')
    ax.set_ylabel('Epsilon')

    fn = 'breakout/output/plot_breakout_epsilon-schedule.png'
    ax.get_figure().savefig(fn)
    print('Saved %s' % fn)
