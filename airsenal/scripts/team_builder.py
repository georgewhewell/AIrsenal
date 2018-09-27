#!/usr/bin/env python

import os
import sys


import random

from ..framework.utils import *
from ..framework.team import Team, TOTAL_PER_POSITION
from ..framework.player import CandidatePlayer


positions = ["FWD", "MID", "DEF", "GK"]  # front-to-back

num_iterations = 10

if __name__ == "__main__":
    best_score = 0.
    best_team = None
    for iteration in range(num_iterations):
        predicted_points = {}
        t = Team()
        # first iteration - fill up from the front
        for pos in positions:
            predicted_points[pos] = get_predicted_points(position=pos, method="EP")
            for pp in predicted_points[pos]:
                t.add_player(pp[0])
                if t.num_position[pos] == TOTAL_PER_POSITION[pos]:
                    break

        # presumably we didn't get a complete team now
        excluded_player_ids = []
        while not t.is_complete():
            # randomly swap out a player and replace with a cheaper one in the
            # same position
            player_to_remove = t.players[random.randint(0, len(t.players) - 1)]
            remove_cost = player_to_remove.current_price
            remove_position = player_to_remove.position
            t.remove_player(player_to_remove.player_id)
            excluded_player_ids.append(player_to_remove.player_id)
            for pp in predicted_points[player_to_remove.position]:
                if (
                    not pp[0] in excluded_player_ids
                ) or random.random() < 0.3:  # some chance to put player back
                    cp = CandidatePlayer(pp[0])
                    if cp.current_price >= remove_cost:
                        continue
                    else:
                        t.add_player(pp[0])
            # now try again to fill up the rest of the team
            num_missing_per_position = {}

            for pos in positions:
                num_missing = TOTAL_PER_POSITION[pos] - t.num_position[pos]
                if num_missing == 0:
                    continue
                for pp in predicted_points[pos]:
                    if pp[0] in excluded_player_ids:
                        continue
                    t.add_player(pp[0])
                    if t.num_position[pos] == TOTAL_PER_POSITION[pos]:
                        break
        # we have a complete team
        score = t.get_expected_points()
        if score > best_score:
            best_score = score
            best_team = t
        print(t)
        print("Score {}".format(score))
    print("====================================\n")
    print(best_team)
    print(best_score)