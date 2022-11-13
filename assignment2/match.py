import numpy as np
import random
import pprint
from typing import List, Tuple
from collections import deque


def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """
    pp = pprint.PrettyPrinter(indent=4)
    q = deque()
    N = len(gender_pref)
    count_list = list(range(N))
    random.shuffle(count_list)

    proposer_preferences = {}
    for i in range(0, N // 2):
        proposer_preferences[count_list[i]] = scores[count_list[i]]
    receiver_preferences = {}
    for i in range(N // 2, N):
        receiver_preferences[count_list[i]] = scores[count_list[i]]

    matched = [False] * len(gender_id)

    for proposer in proposer_preferences:
        q.append(proposer)

    # while some man is free - if our queue is not empty
    # hasn't proposed to every woman - we can set negative values for scores for people that they have already matched with

    # choose a man m - deq from deque
    # choose a woman --> score is not negative
    # if w is free --> if matched[w] == False
    # match them both --> matched[w] = True, matched[m] = True
    # elif comp score > than current comp score
    # match and free up

    matches = {}

    while q:
        proposer = q.pop()

        receiver = -1
        receiver_index = -1
        for i, receiver_score in enumerate(proposer_preferences[proposer]):
            if receiver_score == 0 or i not in receiver_preferences:
                continue
            elif i == "bisexual":
                

            receiver = receiver_score
            receiver_index = i

            break

        if receiver_index == -1:
            break

        if not matched[receiver_index]:
            matches[receiver_index] = proposer
            matched[proposer] = True
            matched[receiver_index] = True
            proposer_preferences[proposer][receiver_index] = 0
        else:
            matched_proposer = matches[receiver_index]

            if (receiver_preferences[receiver_index][proposer]
                > receiver_preferences[receiver_index][matched_proposer]):

                matches[receiver_index] = proposer
                proposer_preferences[proposer][receiver_index] = 0
                matched[matched_proposer] = False
                q.appendleft(matched_proposer)
            else:
                proposer_preferences[proposer][receiver_index] = 0
                q.appendleft(proposer)
                
    pp.pprint(matches)
    return matches


if __name__ == "__main__":
    raw_scores = np.loadtxt("raw_scores.txt").tolist()
    genders = []
    with open("genders.txt", "r") as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open("gender_preferences.txt", "r") as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
