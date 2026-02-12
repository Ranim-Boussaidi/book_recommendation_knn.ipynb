import random
from collections import defaultdict, Counter

opponent_moves = []
my_moves = []
strategy = None

def player(prev_play, opponent_history=[]):
    global opponent_moves, my_moves, strategy
    
    if prev_play == "":
        opponent_moves = []
        my_moves = []
        strategy = None
        return "R"
    
    opponent_moves.append(prev_play)
    
    if len(opponent_moves) == 1:
        my_move = "R"
    elif len(opponent_moves) == 2:
        my_move = "P"
    else:
        my_move = choose_counter_strategy()
    
    my_moves.append(my_move)
    return my_move

def choose_counter_strategy():
    global opponent_moves, my_moves, strategy
    
    if len(opponent_moves) >= 6:
        quincy_pattern = ["R", "P", "S", "R", "P", "S"]
        is_quincy = all(opponent_moves[i] == quincy_pattern[i] for i in range(6))
        if is_quincy:
            strategy = "quincy"
            return beat_quincy()
    
    if len(opponent_moves) >= 3 and my_moves:
        if opponent_moves[-1] == beat_move(my_moves[-1]):
            strategy = "kris"
            return beat_kris()
    
    if len(opponent_moves) >= 4 and len(my_moves) >= 10:
        recent = my_moves[-10:]
        freq = Counter(recent)
        most_common = freq.most_common(1)[0][0]
        if opponent_moves[-1] == beat_move(most_common):
            strategy = "mrugesh"
            return beat_mrugesh()
    
    strategy = "abbey"
    return beat_abbey()

def beat_move(move):
    beats = {"R": "P", "P": "S", "S": "R"}
    return beats[move]

def lose_move(move):
    loses = {"R": "S", "P": "R", "S": "P"}
    return loses[move]

def beat_quincy():
    global opponent_moves
    counters = ["P", "S", "R"]
    return counters[len(opponent_moves) % 3]

def beat_kris():
    global my_moves
    if not my_moves:
        return "R"
    return lose_move(my_moves[-1])

def beat_mrugesh():
    global my_moves
    recent = my_moves[-10:] if len(my_moves) >= 10 else my_moves
    if not recent:
        return "R"
    freq = Counter(recent)
    most_frequent = freq.most_common(1)[0][0]
    return lose_move(most_frequent)

def beat_abbey():
    global my_moves, opponent_moves
    
    if len(my_moves) < 2:
        return "P"
    
    transitions = defaultdict(lambda: defaultdict(int))
    
    for i in range(len(opponent_moves) - 2):
        key = (opponent_moves[i], opponent_moves[i + 1])
        next_move = opponent_moves[i + 2]
        transitions[key][next_move] += 1
    
    if len(opponent_moves) >= 2:
        last_key = (opponent_moves[-2], opponent_moves[-1])
        if last_key in transitions:
            predicted = max(transitions[last_key].items(), key=lambda x: x[1])[0]
            return beat_move(predicted)
    
    return "P"