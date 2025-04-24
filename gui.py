import tkinter as tk
from tkinter import messagebox
import chess
import os
from PIL import Image, ImageTk
from ai import find_best_move, find_random_move  # Import AI logic

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game with AI and Timer")
        self.board = chess.Board()

        self.square_size = 64
        self.canvas = tk.Canvas(root, width=8*self.square_size, height=8*self.square_size)
        self.canvas.pack()

        self.turn = 'white'
        self.difficulty = 'Intermediate'  # Default difficulty level
        self.time_left_white = 10 * 60  # 10 minutes in seconds
        self.time_left_black = 10 * 60  # 10 minutes in seconds
        self.timer_running = False

        # Timer labels for White and Black
        self.white_timer_label = tk.Label(root, text="White's Time: 10:00", font=('Arial', 16), fg="black")
        self.black_timer_label = tk.Label(root, text="Black's Time: 10:00", font=('Arial', 16), fg="black")
        self.white_timer_label.place(x=10, y=520)  # Position near the White side
        self.black_timer_label.place(x=10, y=10)   # Position near the Black side

        # Difficulty selection
        difficulty_label = tk.Label(root, text="Select Difficulty:", font=('Arial', 14))
        difficulty_label.pack()
        difficulty_menu = tk.OptionMenu(root, tk.StringVar(value="Intermediate"), "Basic", "Intermediate", "Hard", command=self.set_difficulty)
        difficulty_menu.pack()

        self.selected_square = None
        self.highlight_squares = []  # stores squares to highlight
        self.piece_images = {}
        self.load_piece_images()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)

        self.start_turn_timer()

    def load_piece_images(self):
        piece_symbols = ['r', 'n', 'b', 'q', 'k', 'p']
        for color in ['w', 'b']:
            for piece in piece_symbols:
                name = color + piece
                path = f"pieces/{name}.png"
                if os.path.exists(path):
                    image = Image.open(path).resize((self.square_size, self.square_size))
                    self.piece_images[name] = ImageTk.PhotoImage(image)

    def draw_board(self):
        colors = ["#EEEED2", "#769656"]
        self.canvas.delete("all")

        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size

                square = chess.square(col, 7 - row)

                if square == self.selected_square:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#f7ec54", outline="")
                elif square in self.highlight_squares:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#ff6961", outline="")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

                piece = self.board.piece_at(square)
                if piece:
                    name = piece.symbol()
                    image_key = ('w' if name.isupper() else 'b') + name.lower()
                    if image_key in self.piece_images:
                        self.canvas.create_image(x1, y1, anchor="nw", image=self.piece_images[image_key])

    def set_difficulty(self, difficulty):
        """
        Set the difficulty level for the AI.
        """
        self.difficulty = difficulty

    def get_ai_move(self):
        """
        Get the AI's move based on the selected difficulty level.
        """
        if self.difficulty == 'Basic':
            return find_random_move(self.board)
        elif self.difficulty == 'Intermediate':
            return find_best_move(self.board, depth=2)
        elif self.difficulty == 'Hard':
            return find_best_move(self.board, depth=4)

    def on_click(self, event):
        col = event.x // self.square_size
        row = 7 - (event.y // self.square_size)
        square = chess.square(col, row)

        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and ((piece.color and self.turn == 'white') or (not piece.color and self.turn == 'black')):
                self.selected_square = square
                self.highlight_squares = [move.to_square for move in self.board.legal_moves if move.from_square == square]
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.check_game_over()  # Check if the game is over after the player's move
                self.switch_turn()

                # AI's turn
                if self.turn == 'black':  # Assuming AI plays as Black
                    best_move = self.get_ai_move()
                    if best_move:
                        self.board.push(best_move)
                        self.check_game_over()  # Check if the game is over after the AI's move
                        self.switch_turn()

            self.selected_square = None
            self.highlight_squares = []

        self.draw_board()

    def switch_turn(self):
        # Switch turn
        self.turn = 'black' if self.turn == 'white' else 'white'
        self.start_turn_timer()

    def start_turn_timer(self):
        """
        Start the timer for the current player's turn.
        Ensure the timer is not restarted unnecessarily.
        """
        if not self.timer_running:  # Prevent multiple timers from running
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        """
        Update the timer every second for the active player.
        """
        if self.timer_running:
            if self.turn == 'white':
                self.time_left_white -= 1
                minutes, seconds = divmod(self.time_left_white, 60)
                self.white_timer_label.config(text=f"White's Time: {minutes}:{seconds:02d}")
            else:
                self.time_left_black -= 1
                minutes, seconds = divmod(self.time_left_black, 60)
                self.black_timer_label.config(text=f"Black's Time: {minutes}:{seconds:02d}")

            # Check if either timer has run out
            if self.time_left_white <= 0:
                self.timer_running = False
                self.end_game("Black")
            elif self.time_left_black <= 0:
                self.timer_running = False
                self.end_game("White")
            else:
                # Schedule the next timer update after 1 second
                self.root.after(1000, self.update_timer)

    def check_game_over(self):
        """
        Check if the game is over due to checkmate, stalemate, or other conditions.
        """
        if self.board.is_checkmate():
            winner = "White" if self.board.turn == chess.BLACK else "Black"
            messagebox.showinfo("Game Over", f"Checkmate! {winner} wins!")
            self.root.quit()
        elif self.board.is_stalemate():
            messagebox.showinfo("Game Over", "Stalemate! The game is a draw!")
            self.root.quit()
        elif self.board.is_insufficient_material():
            messagebox.showinfo("Game Over", "Draw due to insufficient material!")
            self.root.quit()
        elif self.board.is_seventyfive_moves():
            messagebox.showinfo("Game Over", "Draw due to 75-move rule!")
            self.root.quit()
        elif self.board.is_fivefold_repetition():
            messagebox.showinfo("Game Over", "Draw due to fivefold repetition!")
            self.root.quit()

    def end_game(self, winner):
        # Handle game over due to time running out
        messagebox.showinfo("Game Over", f"{winner} wins due to time running out!")
        self.root.quit()


# To test this directly
if __name__ == "__main__":
    root = tk.Tk()
    gui = ChessGUI(root)
    root.mainloop()