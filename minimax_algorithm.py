import random as r


def update_state(curr, r, c, v):
    curr[r * 3 + c] = get_symbol(v)
    return not v


def get_symbol(v):
    return 'X' if v else 'O'


def gen_moves(curr, v):
    s = get_symbol(v)
    poss_moves = []
    for i, x in enumerate(curr):
        if x == -1:
            poss_moves.append(curr[:])
            poss_moves[-1][i] = s
    r.shuffle(poss_moves)
    return poss_moves


def is_won(curr: list):
    for i in range(3):
        if curr[3 * i + 0] == curr[3 * i + 1] == curr[3 * i + 2] != -1: return True
        if curr[0 + i] == curr[3 + i] == curr[6 + i] != -1: return True
    return curr[0] == curr[4] == curr[8] != -1 or curr[2] == curr[4] == curr[6] != -1


def is_draw(curr: list):
    return -1 not in curr


def final_score(curr):
    res = 0
    for x in curr:
        if x == -1: res += 1
    return res


def find_best_move(curr, is_ai, v):
    if is_won(curr): return curr, 1 + final_score(curr) if not is_ai else -final_score(curr) - 1  # invert the flag
    if is_draw(curr): return curr, 0
    poss_moves = gen_moves(curr, v)
    b = -10 if is_ai else 10
    next_move = None
    for move in poss_moves:
        _, score = find_best_move(move, not is_ai, not v)
        if (score > b and is_ai) or (score < b and not is_ai):
            next_move, b = move, score
    return next_move, b
