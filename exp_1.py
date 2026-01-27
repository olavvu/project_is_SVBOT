from schnapsen.game import SchnapsenGamePlayEngine, Bot, PlayerPerspective, Move, RegularMove
from schnapsen.bots import RandBot, RdeepBot, BullyBot, MiniMaxBot, AlphaBetaBot
import random
from statistics import mean
import math
from scipy.stats import ttest_ind
from SVBot import SVBot

engine = SchnapsenGamePlayEngine()

# Average points RandBot vs SVBot (Experiment 1)

from schnapsen.bots import RandBot

rand_bot = RandBot(random.Random(), name="randbot")
sv_bot = SVBot(random.Random(), name="sv_bot")

rand_points = []
sv_bot_points = []

# here it loops 5000 games
for i in range(5001):
    # loop and store points
    winner, game_score, game_points = engine.play_game(rand_bot, sv_bot, random.Random())
    if str(winner) == "randbot":
        rand_points.append(game_points.direct_points)
        sv_bot_points.append(0)
    else:
        rand_points.append(0)
        sv_bot_points.append(game_points.direct_points)

# printing results and finding mean of points 
print(f"Rand has scored an average {mean(rand_points)}, while sv_bot scored an average {mean(sv_bot_points)}")



# Welch's t-test RandBot vs SVBot


from scipy.stats import ttest_ind
# RandBot vs SVBot
t_rand, p_rand = ttest_ind(
    sv_bot_points,
    rand_points,
    equal_var=False  # Welch's t-test
)
print("SVBot vs RandBot:")
print("t-statistic =", t_rand)
print("p-value =", p_rand)






