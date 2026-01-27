from schnapsen.game import SchnapsenGamePlayEngine, Bot, PlayerPerspective, Move, RegularMove
from schnapsen.bots import RandBot, RdeepBot, BullyBot, MiniMaxBot, AlphaBetaBot
import random
from statistics import mean
import math
from scipy.stats import ttest_ind
from SVBot import SVBot

engine = SchnapsenGamePlayEngine()

# Average points BullyBot vs RandBot (Experiment 1)


rand_bot = RandBot(random.Random(), name="randbot")
bully_bot = BullyBot(random.Random(), name="bullybot")

rand_points = []
bully_points = []

# Use a loop to run 100 games
for i in range(5001):
    # Run a game at each iteration of the loop and store the points 
    winner, game_score, game_points = engine.play_game(rand_bot, bully_bot, random.Random())
    if str(winner) == "randbot":
        rand_points.append(game_points.direct_points)
        bully_points.append(0)
    else:
        rand_points.append(0)
        bully_points.append(game_points.direct_points)

# This premade line will print the results if you completed the above code correctly
print(f"Rand has scored an average {mean(rand_points)}, while bullybot scored an average {mean(bully_points)}")






# Welch's t-test RandBot vs BullyBot

from scipy.stats import ttest_ind
# RandBot vs BullyBot
t_rand, p_rand = ttest_ind(
    bully_points,
    rand_points,
    equal_var=False  # Welch's t-test
)
print("BullyBot vs RandBot:")
print("t-statistic =", t_rand)
print("p-value =", p_rand)