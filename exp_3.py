from schnapsen.game import SchnapsenGamePlayEngine, Bot, PlayerPerspective, Move, RegularMove
from schnapsen.bots import RandBot, RdeepBot, BullyBot, MiniMaxBot, AlphaBetaBot
import random
from statistics import mean
import math
from scipy.stats import ttest_ind
from SVBot import SVBot

engine = SchnapsenGamePlayEngine()


# Experiment 3: SV vs Rdeep (Swapped Starts)

from schnapsen.game import SchnapsenGamePlayEngine
from schnapsen.bots import RdeepBot
from scipy.stats import ttest_ind
from statistics import mean, stdev
import random

N = 5000
rng = random.Random(42)
engine = SchnapsenGamePlayEngine()

sv_bot = SVBot(rng, name="sv_bot")
rdeep_bot = RdeepBot(depth=4, num_samples=20, rand=rng, name="r_deep")

scores_start = []   # SV starts first
scores_second = []  # SV starts second
wins_start = 0
wins_second = 0

# starting first
for _ in range(N):
    winner, game_score, game_points = engine.play_game(sv_bot, rdeep_bot, rng)

    # SV's direct points this game (same pattern you used before)
    if winner is sv_bot:
        sv_points = game_points.direct_points
        wins_start += 1
    else:
        sv_points = 0

    scores_start.append(sv_points)

# starting second
for _ in range(N):
    winner, game_score, game_points = engine.play_game(rdeep_bot, sv_bot, rng)

    if winner is sv_bot:
        sv_points = game_points.direct_points
        wins_second += 1
    else:
        sv_points = 0

    scores_second.append(sv_points)
# printing results here 
print("\n=== Experiment 2: SV vs Rdeep (Swapped Starts) ===")

print("\nSV STARTS FIRST:")
print(f"Mean score: {mean(scores_start):.2f}")
print(f"Std dev:    {stdev(scores_start):.2f}")
print(f"Win rate:   {wins_start / N:.3f}")

print("\nSV STARTS SECOND:")
print(f"Mean score: {mean(scores_second):.2f}")
print(f"Std dev:    {stdev(scores_second):.2f}")
print(f"Win rate:   {wins_second / N:.3f}")

# t test
t, p = ttest_ind(scores_start, scores_second, equal_var=False)
print("\nWelch t-test (start first vs second):")
print(f"t = {t:.3f}")
print(f"p = {p:.5f}")
