# Matchbox Computer

## Overview

This project implements a simple machine learning approach using the Matchbox ([MENACE](https://en.wikipedia.org/wiki/Matchbox_Educable_Noughts_and_Crosses_Engine) - Machine Educable Noughts and Crosses Engine) concept to train a computer agent to play Tic-Tac-Toe. MENACE is an early form of machine learning applied to the game of Tic-Tac-Toe, where matchboxes and beads are used to simulate learning by reinforcing winning moves and punishing losing ones.. The program pits a random agent (playing as "X") against a computer agent (playing as "O"). The computer agent learns by reinforcing winning moves and punishing losing ones.

## Features

- Train a computer to play Tic-Tac-Toe against a random agent.
- Computer improves its performance over time by learning from wins, losses, and draws.
- Visualize performance trends using matplotlib plots.

## Prerequisites

Before running the code, ensure you have the following installed:

- Python 3.x
- Required libraries:
  - `itertools`
  - `random`
  - `pickle`
  - `matplotlib`

To install the necessary dependencies, run:

```bash
pip install matplotlib
```

## Running the Program

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Run the training:**
   To start the training process, execute the following command in your terminal:

   ```bash
   python <script_name>.py
   ```

   The script will simulate a series of Tic-Tac-Toe games between the random agent and the computer. After every `num_games` rounds, the script will display statistics about wins, draws, and losses. You will have the option to continue training after each batch.

3. **Save and Load Progress:**
   The state of the game and the computer's learned strategy is saved in a `data.pkl` file. This ensures that the computer continues to improve even after the program is restarted.

4. **Visualize Performance:**
   After the training session, a plot showing the total wins, losses, and draws over time will be displayed.
   ![alt text](https://github.com/saj3sh/matchbox-computer/blob/main/performance_over_time.png?raw=true)

## Explanation of Key Concepts

- **Matchboxes**: Each unique Tic-Tac-Toe board state is stored in a matchbox. The beads in each matchbox represent the available moves for the computer at that state.
- **Reinforcement Learning**: The computer is rewarded by adding beads for winning moves and penalized by removing beads for losing moves. This way, the computer learns which moves lead to better outcomes.
- **Training**: During training, the computer repeatedly plays games against a random opponent. After every batch of games, statistics are recorded, and the user is prompted to continue training or stop.

## Training Parameters

- `TRAINING_EPOCHS`: The number of games to play in one batch of training. Default is set to `10000`.
- `INITIAL_NO_OF_BEADS`: The number of initial beads for each move in an empty board.

## Customization

You can modify the `TRAINING_EPOCHS` and `INITIAL_NO_OF_BEADS` to adjust the length of training and initial randomness of the computer's moves.

## License

This project is open-source and available for use under the MIT License.
