from itertools import product
import pickle
import random as _random
import matplotlib.pyplot as plt

EMPTY = ' '
ZERO = 'O'    # computer plays 'O'
CROSS = 'X'   # random agent plays 'X'
INITIAL_NO_OF_BEADS = 10 # initial number of beads for each available position
TRAINING_EPOCHS = 10000

class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

# two players
random = Player("Random", CROSS)
computer = Player("Computer", ZERO)

def get_empty_board():
    """returns an empty 3x3 tic-tac-toe board"""
    return tuple(tuple(EMPTY for _ in range(3)) for _ in range(3))

def print_board(board):
    """prints the tic-tac-toe board"""
    print("\n".join(["".join([f"[{item}]" for item in row]) for row in board]))

def is_valid_board(board):
    """checks if the board is in a valid state for the student to move"""
    zeros = sum(row.count(ZERO) for row in board)
    crosses = sum(row.count(CROSS) for row in board)
    return crosses == zeros + 1  # It's student's turn if 'X's are one more than 'O's

def is_game_over(board):
    """determine if the game has ended with a win"""
    # all Os or all Xs in at least one row
    if any(len(set(row)) == 1 and row[0] != EMPTY for row in board):
        return True
    # all Os or all Xs in at least one column
    if any(len(set(col)) == 1 and col[0] != EMPTY for col in zip(*board)):
        return True
    # all Os or all Xs along the diagonal
    if board[0][0] != EMPTY and len(set(board[i][i] for i in range(3))) == 1:
        return True
    # all Os or all Xs along the anti-diagonal
    if board[2][0] != EMPTY and len(set(board[2-i][i] for i in range(3))) == 1:
        return True
    return False

def is_draw(board):
    """determine if the game has ended with a draw"""
    return len(get_available_places(board)) == 0

def get_available_places(board):
    """return a list of empty positions on the board"""
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY]

def generate_all_board_states():
    """generates all possible incomplete board states with the computer's turn next"""
    all_states = tuple(
        product(
            product([EMPTY, ZERO, CROSS], repeat=3),
            repeat=3
        )
    )
    incomplete_states = filter(lambda b: not is_game_over(b), all_states)
    valid_states = filter(is_valid_board, incomplete_states)
    return tuple(valid_states)

# initialize MATCHBOXES with incomplete board states, 
# each containing INITIAL_NO_OF_BEADS beads for every available position
MATCHBOXES = {
    board: get_available_places(board) * INITIAL_NO_OF_BEADS 
    for board in generate_all_board_states()
}

def select_move(player, board):
    """randomly select a move for the given player on the given board"""
    if player == random:
        available_places = get_available_places(board)
    else:
        # re-initialize beads for the current board state if they're fully exhausted
        if len(MATCHBOXES[board]) == 0:
            MATCHBOXES[board] = get_available_places(board)
        # select from the beads available for the current board state
        available_places = MATCHBOXES[board]
    return _random.choice(available_places)

def make_move(board, position, symbol):
    """returns a new board state after making the move at the given position."""
    board_as_list = [list(row) for row in board]
    board_as_list[position[0]][position[1]] = symbol
    return tuple(tuple(row) for row in board_as_list)

def play_game():
    """represents a single game of tic-tac-toe."""
    current_player = random # random plays first with X
    board = get_empty_board()
    computer_moves = {}
    while True:
        print_board(board)
        selected_place = select_move(current_player, board)
        print(f"[{current_player.name}]: Enter move (1-9): {selected_place[0]*3 + selected_place[1] + 1}")
        if current_player == computer: #record computer's move
            computer_moves[board] = selected_place
        board = make_move(board, selected_place, current_player.symbol)
        if is_game_over(board):
            print(f"!! {current_player.name} won the game with '{current_player.symbol}'s !!")
            if current_player == computer:
                # computer wins: reinforce the choices made - add 2 beads for each winning move in the corresponding board state
                for move_board in computer_moves:
                    MATCHBOXES[move_board].extend([computer_moves[move_board]] * 2)
                return 1
            # computer loses: punish the choices made - remove 1 bead for each loosing move in the corresponding board state
            for move_board in computer_moves:
                if computer_moves[move_board] in MATCHBOXES[move_board]:
                    MATCHBOXES[move_board].remove(computer_moves[move_board])
            return -1
        if is_draw(board):
            print("!! The game ended in a draw !!")
            # Draw: slight reinforcement - add 1 bead for each winning move in the corresponding board state
            for move_board in computer_moves:
                MATCHBOXES[move_board].append(computer_moves[move_board])
            return 0
        # switch player
        current_player = random if current_player == computer else computer

def plot_performance(total_games, total_wins, total_draws, total_losses):
    fig = plt.figure(figsize=(10, 6))
    fig.canvas.manager.set_window_title('performance over time')
    plt.plot(total_games, total_wins, label='total wins', color='green')
    plt.plot(total_games, total_losses, label='total losses', color = 'red')
    plt.plot(total_games, total_draws, label='total draws', color='grey')

    plt.legend()
    plt.xlabel('total no. of games')
    plt.title('performance over time')
    plt.show()

def start_training(num_games):
    """plays a series of games and tracks the stats"""
    total_games, total_wins, total_draws, total_losses = [], [], [], []
    count, wins, draws, losses = 0, 0, 0, 0
    while True:
        if count % num_games == 0 and count > 0:
            print(f"[{count} games] Won: {wins} | Draw: {draws} | Lost: {losses}")
            total_games.append(count)
            total_wins.append(wins)
            total_draws.append(draws)
            total_losses.append(losses)
            wins, draws, losses = 0, 0, 0
            if input(f"Play another {num_games} games? (Y/N) ").strip().upper() != 'Y':
                break
        result = play_game()
        if result == 1:
            wins += 1
        elif result == 0:
            draws += 1
        else:
            losses += 1
        count += 1
    
    # Save the MATCHBOXES state for future runs on exit
    with open('data.pkl', 'wb') as file:
        pickle.dump(MATCHBOXES, file)

    plot_performance(total_games, total_wins, total_draws, total_losses)

    

if __name__ == "__main__":
    start_training(TRAINING_EPOCHS)
