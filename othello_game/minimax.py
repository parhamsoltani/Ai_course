 
"""
Minimax algorithm with alpha-beta pruning for Othello AI
"""

import math
import random

class MinimaxAI:
    def __init__(self, depth=4):
        self.depth = depth
        self.nodes_evaluated = 0
        
    def evaluate_board(self, board, player):
        """
        Evaluate the board position for the given player
        Uses multiple heuristics: disc count, mobility, corners, and stability
        """
        opponent = 'B' if player == 'W' else 'W'
        
        # Disc count
        score = board.get_score()
        disc_score = score[player] - score[opponent]
        
        # Mobility (number of valid moves)
        player_moves = len(board.get_valid_moves(player))
        opponent_moves = len(board.get_valid_moves(opponent))
        mobility_score = player_moves - opponent_moves
        
        # Corner possession (corners are very valuable)
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        corner_score = 0
        for r, c in corners:
            if board.board[r][c] == player:
                corner_score += 25
            elif board.board[r][c] == opponent:
                corner_score -= 25
        
        # Edge possession
        edge_score = 0
        for i in range(8):
            # Top and bottom edges
            if board.board[0][i] == player:
                edge_score += 5
            elif board.board[0][i] == opponent:
                edge_score -= 5
            if board.board[7][i] == player:
                edge_score += 5
            elif board.board[7][i] == opponent:
                edge_score -= 5
            
            # Left and right edges
            if board.board[i][0] == player:
                edge_score += 5
            elif board.board[i][0] == opponent:
                edge_score -= 5
            if board.board[i][7] == player:
                edge_score += 5
            elif board.board[i][7] == opponent:
                edge_score -= 5
        
        # Danger squares (squares adjacent to corners - usually bad to play there)
        danger_squares = [(0, 1), (1, 0), (1, 1),  # Top-left corner
                         (0, 6), (1, 6), (1, 7),  # Top-right corner
                         (6, 0), (6, 1), (7, 1),  # Bottom-left corner
                         (6, 6), (6, 7), (7, 6)]  # Bottom-right corner
        
        danger_score = 0
        for r, c in danger_squares:
            if board.board[r][c] == player:
                danger_score -= 10
            elif board.board[r][c] == opponent:
                danger_score += 10
        
        # Game phase detection
        total_discs = score[player] + score[opponent]
        
        if total_discs < 20:  # Early game - focus on mobility and position
            total_score = (mobility_score * 10 + corner_score * 5 + 
                          edge_score * 2 + danger_score * 3 + disc_score)
        elif total_discs < 50:  # Mid game - balance all factors
            total_score = (disc_score * 2 + mobility_score * 5 + 
                          corner_score * 10 + edge_score * 3 + danger_score * 2)
        else:  # End game - focus on disc count
            total_score = (disc_score * 10 + corner_score * 5 + 
                          edge_score * 2 + mobility_score)
        
        return total_score
    
    def minimax(self, board, depth, alpha, beta, maximizing_player, player):
        """
        Minimax algorithm with alpha-beta pruning
        """
        self.nodes_evaluated += 1
        
        # Terminal node or depth reached
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board, player), None
        
        opponent = 'B' if player == 'W' else 'W'
        current_player = player if maximizing_player else opponent
        valid_moves = board.get_valid_moves(current_player)
        
        # No valid moves - pass turn
        if not valid_moves:
            return self.minimax(board, depth - 1, alpha, beta, 
                              not maximizing_player, player)
        
        best_move = None
        
        if maximizing_player:
            max_eval = -math.inf
            # Randomize move order for variety
            random.shuffle(valid_moves)
            
            for move in valid_moves:
                row, col = move
                new_board = board.copy()
                new_board.make_move(row, col, current_player)
                
                eval_score, _ = self.minimax(new_board, depth - 1, alpha, beta, 
                                            False, player)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            
            return max_eval, best_move
        
        else:
            min_eval = math.inf
            random.shuffle(valid_moves)
            
            for move in valid_moves:
                row, col = move
                new_board = board.copy()
                new_board.make_move(row, col, current_player)
                
                eval_score, _ = self.minimax(new_board, depth - 1, alpha, beta, 
                                            True, player)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            
            return min_eval, best_move
    
    def get_best_move(self, board, player):
        """
        Get the best move for the given player
        """
        self.nodes_evaluated = 0
        _, best_move = self.minimax(board, self.depth, -math.inf, math.inf, 
                                   True, player)
        return best_move