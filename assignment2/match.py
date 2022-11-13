import numpy as np
from random import random
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

    N = len(scores)

    proposer_preferences, receiver_preferences = [], []
    shuffled = random.shuffle(scores)

    for i in range(0, 4):
        proposer_preferences[i] = shuffled[i]
    for i in range(5,9):
        receiver_preferences[i-5] = shuffled[i]

    # receiver is index
    is_matched = [False] * N
    matches = {}

    proposers = deque() 

    for proposer in proposer_preferences:
        proposers.append(proposer)

    # while some proposer is free and hasn't proposed to every receiver
    while proposers:

        prop = proposers.pop()
        # loop through possible receivers
        for i in range(N/2):
            # make sure preferences match
            if check_preferences(gender_pref[prop], gender_id[i]):

                # is receiver is not matched
                if not is_matched[i]:
                    matches[receiver_preferences[i]] = prop
                    is_matched[i] = True

                # if receiver prefers current proposer
                elif receiver_preferences[prop] > receiver_preferences[matches[i]]:
                    # get previous proposer and append to queue
                    prev_prop = matches[receiver_preferences[i]]
                    matches[prop] = receiver_preferences[i]
                    proposers.append(prev_prop)
                
                # else reject
                else:
                    break
            
    return matches


def check_preferences(pref, gender):
    if pref == "Bisexual":
        return True
    elif pref == "Men":
        if gender in ("Male", "Nonbinary"):
            return True
    elif pref == "Women":
        if gender in ("Female", "Nonbinary"):
            return True  
    return False

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)