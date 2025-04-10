import pygame

# Constants
WIDTH, HEIGHT = 512, 512
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
IMAGES = {}


def load_images():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK',
              'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        image = pygame.image.load(f'images/{piece}.png')  # Make sure the path and names are correct
        IMAGES[piece] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))




# Draw the chessboard and pieces
def draw_board(win, board):
    colors = [pygame.Color(240, 217, 181), pygame.Color(181, 136, 99)]  # Light and dark squares
    for r in range(ROWS):
        for c in range(COLS):
            color = colors[(r + c) % 2]
            pygame.draw.rect(win, color, pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = board[r][c]
            if piece != "--":  # If there is a piece, draw it
                win.blit(IMAGES[piece], pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def get_square_under_mouse(pos):
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return row, col

def is_valid_pawn_move(board, start_row, start_col, end_row, end_col, piece):
    direction = 1 if piece[0] == 'w' else -1  # White moves up (row decreases), black moves down (row increases)
    start_rank = 1 if piece[0] == 'w' else 6  # White pawns start at row 1, black pawns start at row 6

    # Move one square forward
    if start_col == end_col and board[end_row][end_col] == '--' and (end_row - start_row) == direction:
        return True

    # Double move from the starting position (first move)
    if start_col == end_col and board[end_row][end_col] == '--' and (end_row - start_row) == 2 * direction and start_row == start_rank:
        # Ensure the square in between is also empty
        if board[start_row + direction][start_col] == '--':
            return True

    # Diagonal capture
    if abs(start_col - end_col) == 1 and abs(start_row - end_row) == 1 and board[end_row][end_col] != '--' and board[end_row][end_col][0] != piece[0]:
        return True

    return False

def is_valid_knight_move(start_row, start_col, end_row, end_col):
    return (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2)

def is_valid_rook_move(board, start_row, start_col, end_row, end_col):
    if start_row == end_row:  # Same row
        step = 1 if start_col < end_col else -1
        for col in range(start_col + step, end_col, step):
            if board[start_row][col] != '--':  # Blocked by another piece
                return False
        return True
    if start_col == end_col:  # Same column
        step = 1 if start_row < end_row else -1
        for row in range(start_row + step, end_row, step):
            if board[row][start_col] != '--':  # Blocked by another piece
                return False
        return True
    return False

def is_valid_bishop_move(board, start_row, start_col, end_row, end_col):
    if abs(start_row - end_row) == abs(start_col - end_col):
        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1
        row, col = start_row + row_step, start_col + col_step
        while row != end_row and col != end_col:
            if board[row][col] != '--':  # Blocked by another piece
                return False
            row += row_step
            col += col_step
        return True
    return False

def is_valid_queen_move(board, start_row, start_col, end_row, end_col):
    return is_valid_rook_move(board, start_row, start_col, end_row, end_col) or is_valid_bishop_move(board, start_row, start_col, end_row, end_col)

def is_valid_king_move(start_row, start_col, end_row, end_col):
    return max(abs(start_row - end_row), abs(start_col - end_col)) == 1

def move_piece(board, start_row, start_col, end_row, end_col, piece, is_white_turn):
    if piece[0] == 'w' and not is_white_turn:
        return False  # White's turn only
    if piece[0] == 'b' and is_white_turn:
        return False  # Black's turn only

    # Handle pawn movement
    if piece[1] == 'P':  # Pawn
        return is_valid_pawn_move(board, start_row, start_col, end_row, end_col, piece)
    if piece[1] == 'N':  # Knight
        return is_valid_knight_move(start_row, start_col, end_row, end_col)
    if piece[1] == 'R':  # Rook
        return is_valid_rook_move(board, start_row, start_col, end_row, end_col)
    if piece[1] == 'B':  # Bishop
        return is_valid_bishop_move(board, start_row, start_col, end_row, end_col)
    if piece[1] == 'Q':  # Queen
        return is_valid_queen_move(board, start_row, start_col, end_row, end_col)
    if piece[1] == 'K':  # King
        return is_valid_king_move(start_row, start_col, end_row, end_col)
    return False

# Checkmate detection (simplified)
def is_king_in_check(board, king_row, king_col, is_white_turn):
    # For simplicity, this is a placeholder function.
    # You'll need to implement the logic to check if the king is under attack
    return False  # Update this with your check detection logic

def checkmate(board, is_white_turn):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != '--' and piece[0] == ('w' if is_white_turn else 'b'):
                # Check if any move of this piece can block check
                pass  # You should implement the logic to check all pieces and moves.
    return False  # Return True if checkmate
