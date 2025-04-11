
def create_initial_board():
    """
    Creates the initial chessboard setup.
    White pieces are represented by 'w', and black pieces by 'b'.
    The pieces are represented as follows:
    P - Pawn
    R - Rook
    N - Knight
    B - Bishop
    Q - Queen
    K - King
    """
    # Creating an 8x8 grid
    board = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    ]
    return board


# Check if a move is valid for a pawn
def is_valid_pawn_move(board, start_row, start_col, end_row, end_col, piece):
    direction = 1 if piece[0] == 'w' else -1
    start_rank = 1 if piece[0] == 'w' else 6

    # Move one square forward
    if start_col == end_col and board[end_row][end_col] == '--' and (end_row - start_row) == direction:
        return True

    # Double move from the starting position
    if start_col == end_col and board[end_row][end_col] == '--' and (end_row - start_row) == 2 * direction and start_row == start_rank:
        if board[start_row + direction][start_col] == '--':
            return True

    # Diagonal capture
    if abs(start_col - end_col) == 1 and abs(start_row - end_row) == 1 and board[end_row][end_col] != '--' and board[end_row][end_col][0] != piece[0]:
        return True

    return False

# Check if a move is valid for other pieces
def is_valid_move(board, start_row, start_col, end_row, end_col, piece):
    if piece[1] == 'P':  # Pawn
        return is_valid_pawn_move(board, start_row, start_col, end_row, end_col, piece)
    # Add other piece validations like Knight, Rook, Bishop, Queen, King
    return False

# Make the move on the board if it's valid
def move_piece(board, start_row, start_col, end_row, end_col, piece):
    if is_valid_move(board, start_row, start_col, end_row, end_col, piece):
        board[end_row][end_col] = piece
        board[start_row][start_col] = '--'
        return True
    return False

def move_piece(board, start_row, start_col, end_row, end_col, piece, is_white_turn):
    """
    Moves a piece on the board.
    Checks if the move is valid based on basic chess rules.
    """
    # Helper function to check if the target square is empty or occupied by an opponent's piece
    def is_valid_target(row, col):
        if board[row][col] == '--':  # The square is empty
            return True
        elif board[row][col][0] != piece[0]:  # The square is occupied by an opponent's piece
            return True
        return False

    # Pawn movement
    if piece[1] == 'P':  # If the piece is a Pawn
        direction = 1 if piece[0] == 'w' else -1  # White moves up, Black moves down

        # Normal pawn move (1 square forward)
        if start_col == end_col and start_row + direction == end_row and board[end_row][end_col] == '--':
            board[end_row][end_col] = piece
            board[start_row][start_col] = '--'
            return True

        # Pawn first move (2 squares forward from the starting position)
        if piece[0] == 'w' and start_row == 6 and start_col == end_col and start_row - 2 == end_row and board[end_row][end_col] == '--':
            board[end_row][end_col] = piece
            board[start_row][start_col] = '--'
            return True
        if piece[0] == 'b' and start_row == 1 and start_col == end_col and start_row + 2 == end_row and board[end_row][end_col] == '--':
            board[end_row][end_col] = piece
            board[start_row][start_col] = '--'
            return True

        # Pawn capture (1 square diagonally)
        if abs(start_col - end_col) == 1 and start_row + direction == end_row and board[end_row][end_col] != '--':
            board[end_row][end_col] = piece
            board[start_row][start_col] = '--'
            return True

    # Knight movement (L-shape: 2 squares in one direction, 1 in the other)
    elif piece[1] == 'N':
        if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or \
           (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
            if is_valid_target(end_row, end_col):
                board[end_row][end_col] = piece
                board[start_row][start_col] = '--'
                return True

    # Bishop movement (diagonal any number of squares)
    elif piece[1] == 'B':
        if abs(start_row - end_row) == abs(start_col - end_col):  # Diagonal movement
            row_step = 1 if end_row > start_row else -1
            col_step = 1 if end_col > start_col else -1
            row, col = start_row + row_step, start_col + col_step

            while row != end_row and col != end_col:
                if board[row][col] != '--':  # Blocked path
                    return False
                row += row_step
                col += col_step

            if is_valid_target(end_row, end_col):
                board[end_row][end_col] = piece
                board[start_row][start_col] = '--'
                return True

    # Rook movement (horizontal or vertical any number of squares)
    elif piece[1] == 'R':
        if start_row == end_row:  # Horizontal move
            col_step = 1 if end_col > start_col else -1
            for col in range(start_col + col_step, end_col, col_step):
                if board[start_row][col] != '--':  # Blocked path
                    return False
            if is_valid_target(end_row, end_col):
                board[end_row][end_col] = piece
                board[start_row][start_col] = '--'
                return True
        elif start_col == end_col:  # Vertical move
            row_step = 1 if end_row > start_row else -1
            for row in range(start_row + row_step, end_row, row_step):
                if board[row][start_col] != '--':  # Blocked path
                    return False
            if is_valid_target(end_row, end_col):
                board[end_row][end_col] = piece
                board[start_row][start_col] = '--'
                return True

    # Queen movement (combines rook and bishop movement)
    elif piece[1] == 'Q':
        # Handle rook-like moves (horizontal or vertical)
        if start_row == end_row:  # Horizontal move
            col_step = 1 if end_col > start_col else -1
            for col in range(start_col + col_step, end_col, col_step):
                if board[start_row][col] != '--':  # Blocked path
                    return False
            if is_valid_target(end_row, end_col):
                board[end_row][end_col] = piece
                board[start_row][start_col] = '--'
                return True
        elif start_col == end_col:  # Vertical move
            row_step = 1 if end_row > start_row else -1
            for row in range(start_row + row_step, end_row, row_step):
                if board[row][start_col] != '--':  # Blocked path
                    return False
            if is_valid_target(end_row, end_col):
                board[end_row][end_col] = piece
                board[start_row][start_col] = '--'
                return True
        # Handle bishop-like moves (diagonal)
        elif abs(start_row - end_row) == abs(start_col - end_col):
            row_step = 1 if end_row > start_row else -1
            col_step = 1 if end_col > start_col else -1
            row, col = start_row + row_step, start_col + col_step

            while row != end_row and col != end_col:
                if board[row][col] != '--':  # Blocked path
                    return False
                row += row_step
                col += col_step

            if is_valid_target(end_row, end_col):
                board[end_row][end_col] = piece
                board[start_row][start_col] = '--'
                return True

    # King movement (1 square in any direction)
    elif piece[1] == 'K':
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
            if is_valid_target(end_row, end_col):
                board[end_row][end_col] = piece
                board[start_row][start_col] = '--'
                return True

    return False  
