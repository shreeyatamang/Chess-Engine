# game.py
from board import create_board, move_piece
from gui import draw_board, load_images
import pygame

def start_game():
    board = create_board()
    turn = 'w'  # White starts
    game_over = False
    
    while not game_over:
        draw_board(pygame.display.get_surface(), board, load_images())
        # Add logic for detecting and handling player input, making moves, etc.
        
        # Switch turns after every valid move
        turn = 'b' if turn == 'w' else 'w'
    
    # Check for game over (checkmate, stalemate, etc.)
