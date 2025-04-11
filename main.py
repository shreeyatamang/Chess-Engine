import pygame
from tkinter import Tk
import sys
from board import create_initial_board  
from board import move_piece
from gui import ChessGUI


# Constants
WIDTH, HEIGHT = 512, 512
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
IMAGES = {}

#  images for pieces
def load_images():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK',
              'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        image = pygame.image.load(f'images/{piece}.png')  # Ensure the images exist in the 'images' folder
        IMAGES[piece] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

# Drawing the chessboard and pieces
def draw_board(win, board):
    colors = [pygame.Color(240, 217, 181), pygame.Color(181, 136, 99)]
    for r in range(ROWS):
        for c in range(COLS):
            color = colors[(r + c) % 2]
            pygame.draw.rect(win, color, pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = board[r][c]
            if piece != "--":
                win.blit(IMAGES[piece], pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def get_square_under_mouse(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return row, col

# Main game loop
def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")
    clock = pygame.time.Clock()
    board = create_initial_board()
    load_images()

    selected_square = None
    is_white_turn = True  
    running = True

    while running:
        draw_board(win, board)
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_square_under_mouse(pos)

                if selected_square is None:
                    selected_square = (row, col)
                else:
                    start_row, start_col = selected_square
                    end_row, end_col = row, col

                    piece = board[start_row][start_col]

                    # Check if the move is valid
                    if move_piece(board, start_row, start_col, end_row, end_col, piece, is_white_turn):
                        # Perform the move if valid
                        board[start_row][start_col] = '--'
                        board[end_row][end_col] = piece

                        # Switch turn after a valid move
                        is_white_turn = not is_white_turn

                    selected_square = None  # Reset after move

    pygame.quit()
    sys.exit()
    


def run_chess_game():
    root = tk.Tk()
    gui = ChessGUI(root)  # Initialize the ChessGUI
    root.mainloop()




if __name__ == "__main__":
    root = Tk()
    gui = ChessGUI(root)
    root.mainloop()

