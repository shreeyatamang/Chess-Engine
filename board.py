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


# Check if a move is valid for a pawn including promotion
def is_valid_pawn_move(board, start_row, start_col, end_row, end_col, piece):
    direction = -1 if piece[0] == 'w' else 1  # White moves up (decreasing row), Black moves down
    start_rank = 6 if piece[0] == 'w' else 1  # Starting rank for pawns

    # Check if this is potentially a promotion move
    is_promotion_move = (piece[0] == 'w' and end_row == 0) or (piece[0] == 'b' and end_row == 7)

    # Move one square forward
    if start_col == end_col and board[end_row][end_col] == '--' and (end_row - start_row) == direction:
        return True, is_promotion_move

    # Double move from the starting position
    if start_col == end_col and board[end_row][end_col] == '--' and (end_row - start_row) == 2 * direction and start_row == start_rank:
        # Check that the path is clear
        intermediate_row = start_row + direction
        if board[intermediate_row][start_col] == '--':
            return True, False  # Double move cannot be a promotion

    # Diagonal capture
    if abs(start_col - end_col) == 1 and (end_row - start_row) == direction:
        # Check if there's an enemy piece to capture
        if board[end_row][end_col] != '--' and board[end_row][end_col][0] != piece[0]:
            return True, is_promotion_move

    return False, False

# Check if a move is valid for knight
def is_valid_knight_move(board, start_row, start_col, end_row, end_col, piece):
    # Knight moves in L-shape: 2 squares in one direction and 1 in the other
    if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or \
       (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
        # Check if target square is empty or has an enemy piece
        if board[end_row][end_col] == '--' or board[end_row][end_col][0] != piece[0]:
            return True
    return False

# Check if a move is valid for bishop
def is_valid_bishop_move(board, start_row, start_col, end_row, end_col, piece):
    if abs(start_row - end_row) == abs(start_col - end_col):  # Diagonal movement
        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1
        row, col = start_row + row_step, start_col + col_step

        # Check that path is clear
        while row != end_row and col != end_col:
            if board[row][col] != '--':  # Path is blocked
                return False
            row += row_step
            col += col_step

        # Check if target square is empty or has an enemy piece
        return board[end_row][end_col] == '--' or board[end_row][end_col][0] != piece[0]
    return False

# Check if a move is valid for rook
def is_valid_rook_move(board, start_row, start_col, end_row, end_col, piece):
    # Rook moves horizontally or vertically
    if start_row == end_row or start_col == end_col:
        # Check that path is clear
        if start_row == end_row:  # Horizontal move
            col_step = 1 if end_col > start_col else -1
            col = start_col + col_step
            while col != end_col:
                if board[start_row][col] != '--':  # Path is blocked
                    return False
                col += col_step
        else:  # Vertical move
            row_step = 1 if end_row > start_row else -1
            row = start_row + row_step
            while row != end_row:
                if board[row][start_col] != '--':  # Path is blocked
                    return False
                row += row_step

        # Check if target square is empty or has an enemy piece
        return board[end_row][end_col] == '--' or board[end_row][end_col][0] != piece[0]
    return False

# Check if a move is valid for queen
def is_valid_queen_move(board, start_row, start_col, end_row, end_col, piece):
    # Queen combines the movements of rook and bishop
    return is_valid_rook_move(board, start_row, start_col, end_row, end_col, piece) or \
           is_valid_bishop_move(board, start_row, start_col, end_row, end_col, piece)

# Check if a move is valid for king
def is_valid_king_move(board, start_row, start_col, end_row, end_col, piece):
    # King moves one square in any direction
    if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
        # Check if target square is empty or has an enemy piece
        if board[end_row][end_col] == '--' or board[end_row][end_col][0] != piece[0]:
            return True
    return False

# Check if a move is valid for any piece
def is_valid_move(board, start_row, start_col, end_row, end_col, piece):
    """
    Checks if a move is valid for a given piece.
    Returns a tuple (is_valid, is_promotion) where:
    - is_valid: True if the move is valid, False otherwise
    - is_promotion: True if the move is a pawn promotion, False otherwise
    """
    # If start and end positions are the same, it's not a valid move
    if start_row == end_row and start_col == end_col:
        return False, False
        
    # If the target square contains a piece of the same color, it's not a valid move
    if board[end_row][end_col] != '--' and board[end_row][end_col][0] == piece[0]:
        return False, False
        
    # Check validity based on piece type
    if piece[1] == 'P':  # Pawn
        return is_valid_pawn_move(board, start_row, start_col, end_row, end_col, piece)
    elif piece[1] == 'N':  # Knight
        return is_valid_knight_move(board, start_row, start_col, end_row, end_col, piece), False
    elif piece[1] == 'B':  # Bishop
        return is_valid_bishop_move(board, start_row, start_col, end_row, end_col, piece), False
    elif piece[1] == 'R':  # Rook
        return is_valid_rook_move(board, start_row, start_col, end_row, end_col, piece), False
    elif piece[1] == 'Q':  # Queen
        return is_valid_queen_move(board, start_row, start_col, end_row, end_col, piece), False
    elif piece[1] == 'K':  # King
        return is_valid_king_move(board, start_row, start_col, end_row, end_col, piece), False
    
    return False, False

# Handle pawn promotion
def handle_pawn_promotion(board, end_row, end_col, piece, promotion_piece='Q'):
    """
    Handles pawn promotion.
    Default promotion piece is Queen if not specified.
    Returns the new board after promotion.
    """
    # Create a copy of the board to avoid modifying the original
    new_board = [row[:] for row in board]
    
    # Replace the pawn with the promoted piece
    # Ensure we're using the correct color from the original pawn
    color = piece[0]  # Extract the color ('w' or 'b')
    new_board[end_row][end_col] = color + promotion_piece
    
    return new_board
# Make the move on the board if it's valid
def move_piece(board, start_row, start_col, end_row, end_col, piece, is_white_turn, promotion_piece=None):
    """
    Moves a piece on the board.
    Checks if the move is valid based on chess rules.
    Returns a tuple (new_board, success, is_promotion):
    - new_board: The board after the move (or original if move is invalid)
    - success: True if the move was successful, False otherwise
    - is_promotion: True if the move resulted in a pawn promotion
    """
    # Check if it's the correct turn
    if (piece[0] == 'w' and not is_white_turn) or (piece[0] == 'b' and is_white_turn):
        return board, False, False
    
    # Check if the move is valid
    is_valid, is_promotion = is_valid_move(board, start_row, start_col, end_row, end_col, piece)
    
    if is_valid:
        # Create a copy of the board
        new_board = [row[:] for row in board]
        
        # Move the piece
        new_board[end_row][end_col] = piece
        new_board[start_row][start_col] = '--'
        
        # Handle pawn promotion
        if is_promotion:
            if promotion_piece is None:
                promotion_piece = 'Q'  # Default to Queen if not specified
            new_board[end_row][end_col] = piece[0] + promotion_piece
            
        return new_board, True, is_promotion
    
    return board, False, False

# Check if a king is in check
def is_king_in_check(board, is_white):
    """
    Checks if the king of the specified color is in check.
    Returns True if the king is in check, False otherwise.
    """
    # Find the king's position
    king_row, king_col = None, None
    king_piece = 'wK' if is_white else 'bK'
    
    for row in range(8):
        for col in range(8):
            if board[row][col] == king_piece:
                king_row, king_col = row, col
                break
        if king_row is not None:
            break
    
    # Check if any opponent's piece can capture the king
    opponent_color = 'b' if is_white else 'w'
    
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '--' and piece[0] == opponent_color:
                if is_valid_move(board, row, col, king_row, king_col, piece)[0]:
                    return True
    
    return False

# Get all legal moves for a player
def get_legal_moves(board, is_white_turn):
    """
    Gets all legal moves for the current player.
    Returns a list of tuples (start_row, start_col, end_row, end_col).
    """
    legal_moves = []
    player_color = 'w' if is_white_turn else 'b'
    
    # Check all pieces of the current player
    for start_row in range(8):
        for start_col in range(8):
            piece = board[start_row][start_col]
            if piece != '--' and piece[0] == player_color:
                # Check all possible target squares
                for end_row in range(8):
                    for end_col in range(8):
                        if is_valid_move(board, start_row, start_col, end_row, end_col, piece)[0]:
                            # Make the move temporarily
                            temp_board = [row[:] for row in board]
                            temp_board[end_row][end_col] = piece
                            temp_board[start_row][start_col] = '--'
                            
                            # Check if the move would put the king in check
                            if not is_king_in_check(temp_board, is_white_turn):
                                legal_moves.append((start_row, start_col, end_row, end_col))
    
    return legal_moves

# Check if the game is over (checkmate or stalemate)
def is_game_over(board, is_white_turn):
    """
    Checks if the game is over (checkmate or stalemate).
    Returns a tuple (is_over, winner):
    - is_over: True if the game is over, False otherwise
    - winner: 'white', 'black', or 'draw' if the game is over, None otherwise
    """
    # Get all legal moves for the current player
    legal_moves = get_legal_moves(board, is_white_turn)
    
    # If there are no legal moves
    if not legal_moves:
        # Check if the king is in check (checkmate) or not (stalemate)
        if is_king_in_check(board, is_white_turn):
            # Checkmate - the opponent wins
            return True, 'black' if is_white_turn else 'white'
        else:
            # Stalemate - draw
            return True, 'draw'
    
    return False, None

# Handle the promotion UI interaction
def get_promotion_piece_choice(board, end_row, end_col, piece):
    """
    This function should be replaced with actual UI code to get the player's choice.
    Here we just return 'Q' for Queen as default.
    """
    # Default is Queen promotion
    return 'Q'



# Handle pawn promotion in the move function
def move_piece_with_promotion(board, start_row, start_col, end_row, end_col, is_white_turn):
    """
    Full move implementation with pawn promotion handling.
    Returns a tuple (new_board, success, message):
    - new_board: The board after the move
    - success: True if the move was successful
    - message: A message describing the result (e.g., "Promotion to Queen")
    """
    piece = board[start_row][start_col]
    
    # Check if it's a valid piece and the correct turn
    if piece == '--' or (piece[0] == 'w' and not is_white_turn) or (piece[0] == 'b' and is_white_turn):
        return board, False, "Invalid move"
    
    # Check if the move is valid
    is_valid, is_promotion = is_valid_move(board, start_row, start_col, end_row, end_col, piece)
    
    if not is_valid:
        return board, False, "Invalid move"
    
    # Create a new board with the move
    new_board = [row[:] for row in board]
    new_board[end_row][end_col] = piece
    new_board[start_row][start_col] = '--'
    
    # Check if the move would put the player's king in check
    if is_king_in_check(new_board, is_white_turn):
        return board, False, "Move would put your king in check"
    
    # Handle pawn promotion
    if is_promotion:
        # Get the promotion piece choice
        promotion_piece = get_promotion_piece_choice(board, end_row, end_col, piece)
        
        # Make sure the promoted piece has the same color as the original pawn
        piece_color = piece[0]  # This is either 'w' or 'b'
        new_board[end_row][end_col] = piece_color + promotion_piece
        
        return new_board, True, f"Promoted to {promotion_piece}"
    
    return new_board, True, "Move successful"