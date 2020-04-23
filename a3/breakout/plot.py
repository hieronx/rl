import pandas as pd


def plot(args):
    df = pd.read_csv('breakout/output/stats_600k.csv', index_col=None, header=0, delimiter=';')
    plot_max_game_score(df)
    plot_avg_game_score(df)
    plot_scores_per_game(df)
    plot_epsilon_schedule(df)

def plot_max_game_score(df):
    ax = df.plot.line(x='game_id', y='max_game_score')
    ax.set_xlabel('Episodes')
    ax.set_ylabel('Max game score')

    fn = 'breakout/output/max-game-score.png'
    ax.get_figure().savefig(fn)
    print('Saved %s' % fn)

def plot_avg_game_score(df):
    ax = df.plot.line(x='game_id', y='avg_game_score')
    ax.set_xlabel('Episodes')
    ax.set_ylabel('Average game score')

    fn = 'breakout/output/avg-game-score.png'
    ax.get_figure().savefig(fn)
    print('Saved %s' % fn)

def plot_scores_per_game(df):
    ax = df.plot.scatter(x='game_id', y='score')
    ax.set_xlabel('Episodes')
    ax.set_ylabel('Score per game')

    fn = 'breakout/output/scores_per_game.png'
    ax.get_figure().savefig(fn)
    print('Saved %s' % fn)

def plot_epsilon_schedule(df):
    ax = df.plot.line(x='game_id', y='epsilon')
    ax.set_xlabel('Episodes')
    ax.set_ylabel('Epsilon')

    fn = 'breakout/output/epsilon-schedule.png'
    ax.get_figure().savefig(fn)
    print('Saved %s' % fn)
