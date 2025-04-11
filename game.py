# game.py

from chess_timer_game import ChessTimer

class ChessGame:
    def __init__(self):
        self.current_turn = 'white'
        self.timer = ChessTimer(60)
        self.timer.start(callback=self.handle_timeout)

    def handle_timeout(self):
        print(f"{self.current_turn.capitalize()} ran out of time. Game over.")
        # Display result, disable moves, etc.

    def make_move(self, move):
        # When a player makes a valid move
        self.timer.stop()

        # update board, switch turns
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

        # Start new timer for next player
        self.timer.start(callback=self.handle_timeout)
