import tkinter as tk
from tkinter import messagebox, simpledialog
import chess
import os
from PIL import Image, ImageTk
from ai import find_best_move, find_random_move  # Import AI logic

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game with AI and Timer")
        self.root.configure(bg="#2c2c2c")  # Dark background for modern look
        
        # Main frame to contain all elements
        self.main_frame = tk.Frame(root, bg="#2c2c2c")
        self.main_frame.pack(padx=20, pady=20)
        
        self.board = chess.Board()

        self.square_size = 70  # Slightly larger squares for better visibility
        self.canvas = tk.Canvas(
            self.main_frame, 
            width=8*self.square_size, 
            height=8*self.square_size,
            bg="#2c2c2c",
            highlightthickness=2,
            highlightbackground="#555555"
        )
        self.canvas.pack(pady=10)

        # Game info frame
        self.info_frame = tk.Frame(self.main_frame, bg="#2c2c2c")
        self.info_frame.pack(fill=tk.X, pady=10)
        
        # Status frame for timers and current player
        self.status_frame = tk.Frame(self.info_frame, bg="#2c2c2c")
        self.status_frame.pack(side=tk.LEFT, padx=10)
        
        self.turn = 'white'
        self.difficulty = 'Intermediate'  # Default difficulty level
        self.time_left_white = 10 * 60  # 10 minutes in seconds
        self.time_left_black = 10 * 60  # 10 minutes in seconds
        self.timer_running = False
        
        # Current player indicator
        self.turn_indicator = tk.Label(
            self.status_frame, 
            text="Current Player: White", 
            font=('Arial', 14, 'bold'), 
            bg="#2c2c2c", 
            fg="#ffffff"
        )
        self.turn_indicator.pack(anchor=tk.W, pady=(0, 10))

        # Timer labels with improved styling
        timer_frame = tk.Frame(self.status_frame, bg="#2c2c2c")
        timer_frame.pack(anchor=tk.W)
        
        # White timer with icon
        white_timer_frame = tk.Frame(timer_frame, bg="#2c2c2c")
        white_timer_frame.pack(anchor=tk.W, fill=tk.X, pady=5)
        
        white_icon_label = tk.Label(white_timer_frame, text="♔", font=('Arial', 16), bg="#2c2c2c", fg="#ffffff")
        white_icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.white_timer_label = tk.Label(
            white_timer_frame, 
            text="White's Time: 10:00", 
            font=('Arial', 14), 
            bg="#2c2c2c", 
            fg="#ffffff"
        )
        self.white_timer_label.pack(side=tk.LEFT)
        
        # Black timer with icon
        black_timer_frame = tk.Frame(timer_frame, bg="#2c2c2c")
        black_timer_frame.pack(anchor=tk.W, fill=tk.X, pady=5)
        
        black_icon_label = tk.Label(black_timer_frame, text="♚", font=('Arial', 16), bg="#2c2c2c", fg="#ffffff")
        black_icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.black_timer_label = tk.Label(
            black_timer_frame, 
            text="Black's Time: 10:00", 
            font=('Arial', 14), 
            bg="#2c2c2c", 
            fg="#ffffff"
        )
        self.black_timer_label.pack(side=tk.LEFT)

        # Controls frame for buttons and difficulty selection
        self.controls_frame = tk.Frame(self.info_frame, bg="#2c2c2c")
        self.controls_frame.pack(side=tk.RIGHT, padx=10)
        
        # Difficulty selection with better styling
        difficulty_frame = tk.Frame(self.controls_frame, bg="#2c2c2c")
        difficulty_frame.pack(pady=10)
        
        difficulty_label = tk.Label(
            difficulty_frame, 
            text="Difficulty:", 
            font=('Arial', 14), 
            bg="#2c2c2c", 
            fg="#ffffff"
        )
        difficulty_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.difficulty_var = tk.StringVar(value="Intermediate")
        difficulty_menu = tk.OptionMenu(
            difficulty_frame, 
            self.difficulty_var, 
            "Basic", "Intermediate", "Hard", 
            command=self.set_difficulty
        )
        difficulty_menu.config(bg="#3c3c3c", fg="#ffffff", activebackground="#555555", activeforeground="#ffffff")
        difficulty_menu["menu"].config(bg="#3c3c3c", fg="#ffffff")
        difficulty_menu.pack(side=tk.LEFT)
        
        # Button frame
        button_frame = tk.Frame(self.controls_frame, bg="#2c2c2c")
        button_frame.pack(pady=10)
        
        # New game button
        new_game_button = tk.Button(
            button_frame, 
            text="New Game", 
            command=self.new_game,
            bg="#4CAF50", 
            fg="white", 
            font=('Arial', 12),
            padx=10, 
            pady=5,
            relief=tk.FLAT
        )
        new_game_button.pack(side=tk.LEFT, padx=5)
        
        # Undo move button
        undo_button = tk.Button(
            button_frame, 
            text="Undo Move", 
            command=self.undo_move,
            bg="#FF9800", 
            fg="white", 
            font=('Arial', 12),
            padx=10, 
            pady=5,
            relief=tk.FLAT
        )
        undo_button.pack(side=tk.LEFT, padx=5)

        self.selected_square = None
        self.highlight_squares = []  # stores squares to highlight
        self.piece_images = {}
        self.load_piece_images()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)

        # Track game state
        self.game_active = True
        self.promotion_in_progress = False
        
        # Start turn timer
        self.start_turn_timer()
        
        # Draw coordinates around the board
        self.draw_coordinates()

    def load_piece_images(self):
        piece_symbols = ['r', 'n', 'b', 'q', 'k', 'p']
        for color in ['w', 'b']:
            for piece in piece_symbols:
                name = color + piece
                path = f"pieces/{name}.png"
                if os.path.exists(path):
                    image = Image.open(path).resize((self.square_size - 10, self.square_size - 10))
                    self.piece_images[name] = ImageTk.PhotoImage(image)

    def draw_coordinates(self):
        # Add file coordinates (a-h) at the bottom
        for i in range(8):
            x = i * self.square_size + self.square_size / 2
            y = 8 * self.square_size + 15
            self.canvas.create_text(x, y, text=chr(97 + i), fill="#ffffff", font=('Arial', 12))
        
        # Add rank coordinates (1-8) on the right
        for i in range(8):
            x = 8 * self.square_size + 15
            y = (7 - i) * self.square_size + self.square_size / 2
            self.canvas.create_text(x, y, text=str(i + 1), fill="#ffffff", font=('Arial', 12))

    def draw_board(self):
        colors = ["#EEEED2", "#769656"]  # Light and dark square colors
        self.canvas.delete("all")

        # Draw the squares
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size

                square = chess.square(col, 7 - row)

                # Highlight selected square
                if square == self.selected_square:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#f7ec54", outline="")
                # Highlight valid moves
                elif square in self.highlight_squares:
                    # Use different highlight based on whether there's a piece to capture
                    if self.board.piece_at(square):
                        # Red circle for capture moves
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                        self.canvas.create_oval(x1+10, y1+10, x2-10, y2-10, fill="#ff6961", outline="")
                    else:
                        # Green circle for empty square moves
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                        self.canvas.create_oval(x1+20, y1+20, x2-20, y2-20, fill="#a7c7ac", outline="")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

                # Draw pieces
                piece = self.board.piece_at(square)
                if piece:
                    name = piece.symbol()
                    image_key = ('w' if name.isupper() else 'b') + name.lower()
                    if image_key in self.piece_images:
                        image_x = x1 + (self.square_size - self.piece_images[image_key].width()) / 2
                        image_y = y1 + (self.square_size - self.piece_images[image_key].height()) / 2
                        self.canvas.create_image(image_x, image_y, anchor="nw", image=self.piece_images[image_key])
        
        # Draw coordinates        
        self.draw_coordinates()
        
        # Check if king is in check
        if self.board.is_check():
            king_color = chess.WHITE if self.board.turn == chess.WHITE else chess.BLACK
            king_square = self.board.king(king_color)
            col = chess.square_file(king_square)
            row = 7 - chess.square_rank(king_square)
            x1 = col * self.square_size
            y1 = row * self.square_size
            x2 = x1 + self.square_size
            y2 = y1 + self.square_size
            
            # Draw red border around king in check
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="#ff0000", width=3)

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

    def handle_pawn_promotion(self, move):
        """
        Handle pawn promotion with a dialog to select the piece.
        """
        if not self.is_pawn_promotion(move):
            return move
            
        self.promotion_in_progress = True
        
        # Create promotion dialog
        promotion_window = tk.Toplevel(self.root)
        promotion_window.title("Pawn Promotion")
        promotion_window.geometry("400x150")
        promotion_window.configure(bg="#3c3c3c")
        promotion_window.transient(self.root)
        promotion_window.grab_set()
        
        # Prevent interactions with main window while dialog is open
        promotion_window.focus_set()
        
        # Center the window
        window_width = 400
        window_height = 150
        position_right = int(self.root.winfo_x() + (self.root.winfo_width() - window_width) / 2)
        position_down = int(self.root.winfo_y() + (self.root.winfo_height() - window_height) / 2)
        promotion_window.geometry("+{}+{}".format(position_right, position_down))
        
        # Add label
        label = tk.Label(
            promotion_window, 
            text="Choose a piece for pawn promotion:", 
            font=('Arial', 14),
            bg="#3c3c3c",
            fg="#ffffff",
            pady=10
        )
        label.pack()
        
        selected_piece = tk.StringVar()
        
        # Create frame for buttons
        button_frame = tk.Frame(promotion_window, bg="#3c3c3c")
        button_frame.pack(pady=10)
        
        # Create piece buttons
        pieces = [('Queen', chess.QUEEN), ('Rook', chess.ROOK), 
                  ('Bishop', chess.BISHOP), ('Knight', chess.KNIGHT)]
                  
        for piece_name, piece_type in pieces:
            button = tk.Button(
                button_frame,
                text=piece_name,
                width=8,
                height=1,
                bg="#555555",
                fg="#ffffff",
                font=('Arial', 12),
                relief=tk.FLAT,
                command=lambda p=piece_type: self.complete_promotion(move, p, promotion_window)
            )
            button.pack(side=tk.LEFT, padx=5)
            
        # Wait for the window to be destroyed
        self.root.wait_window(promotion_window)
        return move

    def complete_promotion(self, move, piece_type, window):
        """Complete the pawn promotion with the selected piece type."""
        from_square = move.from_square
        to_square = move.to_square
        
        # Create a new move with promotion
        move = chess.Move(from_square, to_square, promotion=piece_type)
        
        # Execute the move
        self.board.push(move)
        
        # Check game state after the move
        self.check_game_over()
        
        # Switch turn
        self.switch_turn()
        
        # AI's turn if it's black's turn
        if self.turn == 'black' and self.game_active:
            self.make_ai_move()
            
        # Close the promotion window
        window.destroy()
        self.promotion_in_progress = False
        
        # Update the board display
        self.draw_board()

    def is_pawn_promotion(self, move):
        """Check if a move is a pawn promotion."""
        piece = self.board.piece_at(move.from_square)
        
        # If not a pawn, it's not a promotion
        if piece is None or piece.piece_type != chess.PAWN:
            return False
            
        # Check if the pawn is moving to the last rank
        rank = chess.square_rank(move.to_square)
        return (piece.color == chess.WHITE and rank == 7) or (piece.color == chess.BLACK and rank == 0)

    def on_click(self, event):
        if not self.game_active or self.promotion_in_progress:
            return
            
        col = event.x // self.square_size
        row = 7 - (event.y // self.square_size)
        
        # Make sure the click is within the board
        if not (0 <= col < 8 and 0 <= row < 8):
            return
            
        square = chess.square(col, row)

        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and ((piece.color == chess.WHITE and self.turn == 'white') or 
                         (piece.color == chess.BLACK and self.turn == 'black')):
                self.selected_square = square
                
                # Highlight legal moves for selected piece
                self.highlight_squares = [move.to_square for move in self.board.legal_moves 
                                         if move.from_square == square]
        else:
            # Try to make a move
            move = chess.Move(self.selected_square, square)
            
            # Check if it's a promotion move
            if self.is_pawn_promotion(move):
                self.handle_pawn_promotion(move)
                self.selected_square = None
                self.highlight_squares = []
                return
                
            # Regular move
            if move in self.board.legal_moves:
                self.board.push(move)
                self.check_game_over()  # Check if the game is over after the player's move
                
                if self.game_active:
                    self.switch_turn()
                    
                    # AI's turn
                    if self.turn == 'black':  # Assuming AI plays as Black
                        self.make_ai_move()

            self.selected_square = None
            self.highlight_squares = []

        self.draw_board()

    def make_ai_move(self):
        """Make AI move and handle promotions automatically."""
        best_move = self.get_ai_move()
        if best_move:
            self.board.push(best_move)
            self.check_game_over()  # Check if the game is over after the AI's move
            if self.game_active:
                self.switch_turn()

    def switch_turn(self):
        """Switch turn and update UI."""
        # Switch turn
        self.turn = 'black' if self.turn == 'white' else 'white'
        
        # Update turn indicator
        self.turn_indicator.config(text=f"Current Player: {'Black' if self.turn == 'black' else 'White'}")
        
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
        if self.timer_running and self.game_active:
            if self.turn == 'white':
                self.time_left_white -= 1
                minutes, seconds = divmod(self.time_left_white, 60)
                self.white_timer_label.config(text=f"White's Time: {minutes}:{seconds:02d}")
                
                # Change color if time is running low
                if self.time_left_white < 60:  # Less than a minute
                    self.white_timer_label.config(fg="#ff6961")
                elif self.time_left_white < 300:  # Less than 5 minutes
                    self.white_timer_label.config(fg="#ffb347")
                else:
                    self.white_timer_label.config(fg="#ffffff")
            else:
                self.time_left_black -= 1
                minutes, seconds = divmod(self.time_left_black, 60)
                self.black_timer_label.config(text=f"Black's Time: {minutes}:{seconds:02d}")
                
                # Change color if time is running low
                if self.time_left_black < 60:  # Less than a minute
                    self.black_timer_label.config(fg="#ff6961")
                elif self.time_left_black < 300:  # Less than 5 minutes
                    self.black_timer_label.config(fg="#ffb347")
                else:
                    self.black_timer_label.config(fg="#ffffff")

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
            self.end_game(winner, "Checkmate")
        elif self.board.is_stalemate():
            self.end_game(None, "Stalemate")
        elif self.board.is_insufficient_material():
            self.end_game(None, "Insufficient Material")
        elif self.board.is_seventyfive_moves():
            self.end_game(None, "75-Move Rule")
        elif self.board.is_fivefold_repetition():
            self.end_game(None, "Fivefold Repetition")

    def end_game(self, winner, reason="Time"):
        """
        End the game and show a message.
        """
        self.game_active = False
        self.timer_running = False
        
        if winner:
            message = f"{winner} wins due to {reason}!"
        else:
            message = f"Game is drawn due to {reason}!"
            
        # Show game over dialog with options
        game_over_window = tk.Toplevel(self.root)
        game_over_window.title("Game Over")
        game_over_window.geometry("400x200")
        game_over_window.configure(bg="#3c3c3c")
        game_over_window.transient(self.root)
        game_over_window.grab_set()
        
        # Center the window
        window_width = 400
        window_height = 200
        position_right = int(self.root.winfo_x() + (self.root.winfo_width() - window_width) / 2)
        position_down = int(self.root.winfo_y() + (self.root.winfo_height() - window_height) / 2)
        game_over_window.geometry("+{}+{}".format(position_right, position_down))
        
        # Add message
        tk.Label(
            game_over_window, 
            text="Game Over", 
            font=('Arial', 18, 'bold'),
            bg="#3c3c3c",
            fg="#ffffff",
            pady=10
        ).pack()
        
        tk.Label(
            game_over_window, 
            text=message, 
            font=('Arial', 14),
            bg="#3c3c3c",
            fg="#ffffff",
            pady=10
        ).pack()
        
        # Button frame
        button_frame = tk.Frame(game_over_window, bg="#3c3c3c")
        button_frame.pack(pady=20)
        
        # New game button
        tk.Button(
            button_frame,
            text="New Game",
            width=10,
            height=1,
            bg="#4CAF50",
            fg="#ffffff",
            font=('Arial', 12),
            relief=tk.FLAT,
            command=lambda: [game_over_window.destroy(), self.new_game()]
        ).pack(side=tk.LEFT, padx=10)
        
        # Exit button
        tk.Button(
            button_frame,
            text="Exit",
            width=10,
            height=1,
            bg="#f44336",
            fg="#ffffff",
            font=('Arial', 12),
            relief=tk.FLAT,
            command=self.root.quit
        ).pack(side=tk.LEFT, padx=10)

    def new_game(self):
        """
        Start a new game.
        """
        self.board = chess.Board()
        self.time_left_white = 10 * 60
        self.time_left_black = 10 * 60
        self.turn = 'white'
        self.game_active = True
        self.selected_square = None
        self.highlight_squares = []
        
        # Update UI
        self.white_timer_label.config(text="White's Time: 10:00", fg="#ffffff")
        self.black_timer_label.config(text="Black's Time: 10:00", fg="#ffffff")
        self.turn_indicator.config(text="Current Player: White")
        
        # Draw the board
        self.draw_board()
        
        # Start the timer
        self.start_turn_timer()

    def undo_move(self):
        """
        Undo the last two moves (player and AI).
        """
        if not self.game_active:
            return
            
        # Undo player move and AI move
        if len(self.board.move_stack) >= 2:
            self.board.pop()  # Undo AI move
            self.board.pop()  # Undo player move
            self.draw_board()
        # If only one move has been made
        elif len(self.board.move_stack) == 1:
            self.board.pop()
            self.draw_board()
            self.turn = 'white'
            self.turn_indicator.config(text="Current Player: White")


# To test this directly
if __name__ == "__main__":
    root = tk.Tk()
    gui = ChessGUI(root)
    root.mainloop()