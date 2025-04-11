import tkinter as tk
from tkinter import messagebox
import chess
import os
from PIL import Image, ImageTk

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game with Timer")
        self.board = chess.Board()

        self.square_size = 64
        self.canvas = tk.Canvas(root, width=8*self.square_size, height=8*self.square_size)
        self.canvas.pack()

        self.turn = 'white'
        self.time_left_white = 60
        self.time_left_black = 60
        self.timer_running_white = False
        self.timer_running_black = False
        self.timer_label = tk.Label(root, text="White's Turn | Time: 60s", font=('Arial', 16))
        self.timer_label.pack()

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
                self.switch_turn()
            self.selected_square = None
            self.highlight_squares = []

        self.draw_board()

    def switch_turn(self):
        # Switch turn
        self.turn = 'black' if self.turn == 'white' else 'white'
        self.start_turn_timer()

    def start_turn_timer(self):
        # Set timer depending on the current player's turn
        if self.turn == 'white':
            self.timer_running_white = True
            self.timer_running_black = False
            self.time_left_white = 30  # Reset to 30 seconds for each turn
        else:
            self.timer_running_white = False
            self.timer_running_black = True
            self.time_left_black = 30

        self.update_timer()

    def update_timer(self):
        if self.timer_running_white:
            self.timer_label.config(text=f"White's Turn | Time: {self.time_left_white}s")
            if self.time_left_white <= 0:
                self.timer_running_white = False
                self.end_game("Black")
            else:
                self.time_left_white -= 1
                self.root.after(1000, self.update_timer)

        elif self.timer_running_black:
            self.timer_label.config(text=f"Black's Turn | Time: {self.time_left_black}s")
            if self.time_left_black <= 0:
                self.timer_running_black = False
                self.end_game("White")
            else:
                self.time_left_black -= 1
                self.root.after(1000, self.update_timer)

    def end_game(self, winner):
        # Handle game over due to time running out
        messagebox.showinfo("Game Over", f"{winner} wins due to time running out!")
        self.root.quit()


# To test this directly
if __name__ == "__main__":
    root = tk.Tk()
    gui = ChessGUI(root)
    root.mainloop()
