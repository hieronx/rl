import matplotlib.pyplot as plt
import pandas as pd

from mountaincar.train import train

num_trials = 10

def plot(args):
    args.num_threads = 10
    args.num_games_eval = 100
    args.steps_per_game_eval = 200
    args.num_games_train = 100000
    args.steps_per_game_train = 200
    args.score_requirement = -198

    plot_dropout_effect(args)
    # plot_random_sample_size(args)

def plot_dropout_effect(args):
    args.num_games_train = 100000
    args.overwrite_training_data = False

    args.dropout_pct = 0.0
    scores_wo_dropout = []
    for _ in range(num_trials):
        score = train(args)
        scores_wo_dropout.append(score)

    args.dropout_pct = 0.2
    scores_with_dropout = []
    for _ in range(num_trials):
        score = train(args)
        scores_with_dropout.append(score)

    print('Scores without dropout: %s' % str(scores_wo_dropout))
    print('Scores with dropout: %s' % str(scores_with_dropout))

    df = pd.DataFrame({ 'Without dropout': scores_with_dropout, 'With dropout': scores_wo_dropout })
    ax = df.plot.hist(bins=12, alpha=0.5)

    fn = 'breakout/output/plot_mountaincar_dropout-effect-100k.png'
    ax.get_figure().savefig(fn)
    print('Saved %s' % fn)


# def plot_random_sample_size(args):
#     args.overwrite_training_data = True

#     args.num_games_train = 10000
#     scores_wo_dropout = []
#     for _ in range(num_trials):
#         score = train(args)
#         scores_wo_dropout.append(score)

#     args.num_games_train = 100000
#     scores_with_dropout = []
#     for _ in range(num_trials):
#         score = train(args)
#         scores_with_dropout.append(score)

#     print('Scores without dropout: %s' % str(scores_wo_dropout))
#     print('Scores with dropout: %s' % str(scores_with_dropout))

#     df = pd.DataFrame({ 'Without dropout': scores_with_dropout, 'With dropout': scores_wo_dropout })
#     ax = df.plot.hist(bins=12, alpha=0.5)

#     fn = 'breakout/output/plot_mountaincar_random_sample_size.png'
#     ax.get_figure().savefig(fn)
#     print('Saved %s' % fn)
