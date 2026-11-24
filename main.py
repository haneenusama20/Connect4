import random
import time

from board import Board, EMPTY, HUMAN, AGENT
import agent
from tree_print import print_tree


RANDOM_DROPS_IN_EXPECTED = True


def ask_int(text, minimum):
    while True:
        answer = input(text)
        if answer.strip().isdigit() and int(answer) >= minimum:
            return int(answer)
        print("Please type a whole number, at least", minimum)


def print_board(board):
    symbols = {EMPTY: ".", HUMAN: "H", AGENT: "A"}
    print()
    for r in range(board.rows - 1, -1, -1):
        line = ""
        for c in range(board.cols):
            line = line + symbols[board.grid[r][c]] + " "
        print(line)
    numbers = ""
    for c in range(board.cols):
        numbers = numbers + str(c) + " "
    print(numbers)
    print()


def ask_human_column(board):

    valid = board.valid_columns()
    while True:
        col = ask_int("Your column " + str(valid) + ": ", 0)
        if col in valid:
            return col
        print("That column is not available.")


def real_drop(board, col, player, use_chance):
    
    landing = col
    if use_chance: #3shan el expiminimax
        options = agent.landing_options(board, col)
        columns = [c for c, p in options]
        probabilities = [p for c, p in options]
        landing = random.choices(columns, probabilities)[0]
        if landing != col:
            print("The disc slipped from column", col, "to column", landing)
    board.drop(landing, player)


def main():
    rows = ask_int("Rows (at least 6): ", 6)
    cols = ask_int("Columns (at least 7): ", 7)
    k = ask_int("K (search depth): ", 1)
    print("1) Minimax   2) Minimax with alpha-beta   3) Expected minimax")
    choice = ask_int("Algorithm: ", 1)
    while choice > 3 or choice < 1:
        choice = ask_int("Choose 1, 2 or 3: ", 1)

    if choice == 1:
        choose = agent.choose_move
    elif choice == 2:
        choose = agent.choose_move_alphabeta
    else:
        choose = agent.choose_move_expected
    use_chance = (choice == 3) and RANDOM_DROPS_IN_EXPECTED

    
    show_tree = ask_int("Print the tree each turn? (1 = yes, 0 = no): ", 0) == 1
    agent.set_tree_building(show_tree)

    board = Board(rows, cols)
    print_board(board)

    while not board.is_full():

        col = ask_human_column(board)
        real_drop(board, col, HUMAN, use_chance)
        print_board(board)
        if board.is_full():
            break

        start = time.perf_counter()  #mn hena dor el agent
        col = choose(board, k)
        seconds = time.perf_counter() - start
        if show_tree:
            print_tree(agent.get_tree())
        print("Agent plays column", col)
        print("Nodes expanded:", agent.get_nodes(), " Time:", round(seconds, 4), "s")
        real_drop(board, col, AGENT, use_chance)
        print_board(board)

    #Wooo khalasna
    human_score = board.scores[HUMAN]
    agent_score = board.scores[AGENT]
    print("Game over.  Human:", human_score, " Agent:", agent_score)
    if human_score > agent_score:
        print("Human wins!")
    elif agent_score > human_score:
        print("Agent wins!")
    else:
        print("Draw.")


if __name__ == "__main__":
    main()