from schnapsen.game import SchnapsenGamePlayEngine, Bot, PlayerPerspective, Move, RegularMove
from schnapsen.bots import RandBot, RdeepBot, BullyBot, MiniMaxBot, AlphaBetaBot
import random
from statistics import mean
import math
from scipy.stats import ttest_ind
from SVBot import SVBot

engine = SchnapsenGamePlayEngine()

# Average points RdeepBot vs SVBot (Experiment 2)

rdeep_bot = RdeepBot(depth = 4, num_samples = 45, rand = random.Random(), name="r_deep")
sv_bot = SVBot(random.Random(), name="sv_bot")

rdeep_points = []
sv_bot_points = []

# Use a loop to run 5000 games
for i in range(5001):
    # Run a game at each iteration of the loop and store the points 
    winner, game_score, game_points = engine.play_game(rdeep_bot, sv_bot, random.Random())
    if str(winner) == "r_deep":
        rdeep_points.append(game_points.direct_points)
        sv_bot_points.append(0)
    else:
        rdeep_points.append(0)
        sv_bot_points.append(game_points.direct_points)

# print results
print(f"RDeep has scored an average {mean(rdeep_points)}, while sv_bot scored an average {mean(sv_bot_points)}")






# Welch's t-test Rdeep vs SVBot


from scipy.stats import ttest_ind
# RdeepBot vs SVBot
t_rand, p_rand = ttest_ind(
    sv_bot_points,
    rdeep_points,
    equal_var=False  # Welch's t-test
)
print("SVBot vs RdeepBot:")
print("t-statistic =", t_rand)
print("p-value =", p_rand)
