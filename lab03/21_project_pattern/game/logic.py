import random

suits = ["clubs", "diamonds", "hearts", "spades"]
ranks = ['2','3','4','5','6','7','8','9','10','jack','queen','king','ace']

def create_deck():
    deck = [(r, s) for r in ranks for s in suits]
    random.shuffle(deck)
    return deck

def calculate_score(hand):
    total = 0
    aces = 0

    for rank, _ in hand:
        if rank in ['jack','queen','king']:
            total += 10
        elif rank == 'ace':
            aces += 1
        else:
            total += int(rank)

    scores = [total + aces]

    for i in range(1, aces + 1):
        scores.append(total + aces + i * 10)

    valid = [s for s in scores if s <= 21]
    return valid if valid else [min(scores)]