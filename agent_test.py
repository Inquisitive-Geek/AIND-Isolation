"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import itertools
import random
import warnings

from collections import namedtuple

from isolation import Board
from sample_players import (RandomPlayer, open_move_score,
                            improved_score, center_score)
from game_agent import (MinimaxPlayer, AlphaBetaPlayer, custom_score,
                        custom_score_2, custom_score_3)

NUM_MATCHES = 1  # number of matches against each opponent
TIME_LIMIT = 150  # number of milliseconds before timeout

DESCRIPTION = """
This script evaluates the performance of the custom_score evaluation function
against the `ID_Improved` agent baseline. `ID_CustomScore` is an agent using
Iterative Deepening and the custom_score function defined in game_agent.py.
"""

Agent = namedtuple("Agent", ["player", "name"])

def play_round(cpu_agent, test_agents, win_counts, num_matches):
    """Compare the test agents to the cpu agent in "fair" matches.

    "Fair" matches use random starting locations and force the agents to
    play as both first and second player to control for advantages resulting
    from choosing better opening moves or having first initiative to move.
    """
    timeout_count = 0
    forfeit_count = 0
    for _ in range(num_matches):

        games = sum([[Board(cpu_agent.player, agent.player),
                      Board(agent.player, cpu_agent.player)]
                    for agent in test_agents], [])

        # initialize all games with a random move and response
        for _ in range(2):
            move = random.choice(games[0].get_legal_moves())
            for game in games:
                game.apply_move(move)

        # play all games and tally the results
        for game in games:
            winner, _, termination = game.play(time_limit=TIME_LIMIT)
            win_counts[winner] += 1

        if termination == "timeout":
            timeout_count += 1
        elif winner not in test_agents and termination == "forfeit":
            forfeit_count += 1

    return timeout_count, forfeit_count


def main():

    # Define two agents to compare -- these agents will play from the same
    # starting position against the same adversaries in the tournament
    test_agents = [
        Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved") # ,
        # Agent(AlphaBetaPlayer(score_fn=custom_score), "AB_Custom"),
        # Agent(AlphaBetaPlayer(score_fn=custom_score_2), "AB_Custom_2"),
        # Agent(AlphaBetaPlayer(score_fn=custom_score_3), "AB_Custom_3")
     ]

    # Define a collection of agents to compete against the test agents
    cpu_agents = [
        Agent(RandomPlayer(), "Random") #,
        # Agent(MinimaxPlayer(score_fn=open_move_score), "MM_Open"),
        # Agent(MinimaxPlayer(score_fn=center_score), "MM_Center"),
        # Agent(MinimaxPlayer(score_fn=improved_score), "MM_Improved"),
        # Agent(AlphaBetaPlayer(score_fn=open_move_score), "AB_Open"),
        # Agent(AlphaBetaPlayer(score_fn=center_score), "AB_Center"),
        # Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved")
    ]

    print(DESCRIPTION)
    print("{:^74}".format("*************************"))
    print("{:^74}".format("Playing Matches"))
    print("{:^74}".format("*************************"))
    wins = {test_agents[0].player: 0,
            cpu_agents[0].player: 0}
    counts = play_round(cpu_agents[0], test_agents[0], wins, NUM_MATCHES)
    # total_timeouts += counts[0]
    # total_forfeits += counts[1]
    # counts = play_round(agent, test_agents, wins, num_matches)
    # total_timeouts += counts[0]
    # total_forfeits += counts[1]



if __name__ == "__main__":
    main()