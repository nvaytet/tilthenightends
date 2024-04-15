# SPDX-License-Identifier: BSD-3-Clause

import os
from typing import Dict

from .player import Player


def read_scores(players: Dict[str, Player], test: bool) -> Dict[str, int]:
    scores = {p: 0 for p in players}
    fname = "scores.txt"
    if os.path.exists(fname) and (not test):
        with open(fname, "r") as f:
            contents = f.readlines()
        for line in contents:
            name, score = line.split(":")
            scores[name] = int(score.strip())
    return scores


def _write_scores(scores: Dict[str, int]):
    fname = "scores.txt"
    with open(fname, "w") as f:
        for name, score in scores.items():
            f.write(f"{name}: {score}\n")


def _print_scores(round_scores: Dict[str, int], final_scores: Dict[str, int]):
    all_scores = [
        (team, round_scores[team], final_scores[team]) for team in final_scores
    ]
    sorted_scores = sorted(all_scores, key=lambda tup: tup[2], reverse=True)
    print("\nScores:")
    for i, (name, score, total) in enumerate(sorted_scores):
        print(f"{i + 1}. {name}: {total} (this round: {score})")


def finalize_scores(players: Dict[str, Player], test: bool = False):
    scores = read_scores(players, test=test)
    round_scores = {k: p.score for k, p in players.items()}
    final_scores = {k: scores[k] + p.score for k, p in players.items()}
    _print_scores(round_scores=round_scores, final_scores=final_scores)
    _write_scores(final_scores)
