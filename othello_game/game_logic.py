
"""
Core game logic for Othello
"""

import copy

class OthelloBoard:
    def __init__(self):
        self.size = 8
        self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = 'B'  # Black starts first
        self.initialize_board()

    def initialize_board(self):
        """Set up the initial board configuration"""
        mid = self.size // 2
        self.board[mid-1][mid-1] = 'W'
        self.board[mid-1][mid] = 'B'
        self.board[mid][mid-1] = 'B'
        self.board[mid][mid] = 'W'

    def is_valid_position(self, row, col):
        """Check if position is within board boundaries"""
        return 0 <= row < self.size and 0 <= col < self.size

    def get_opponent(self, player):
        """Get the opponent's symbol"""
        return 'W' if player == 'B' else 'B'

    def check_direction(self, row, col, dr, dc, player):
        """Check if placing a disc at (row, col) would flip discs in direction (dr, dc)"""
        opponent = self.get_opponent(player)
        r, c = row + dr, col + dc
        discs_to_flip = []

        # Must have at least one opponent disc in this direction
        if not self.is_valid_position(r, c) or self.board[r][c] != opponent:
            return []

        discs_to_flip.append((r, c))
        r, c = r + dr, c + dc

        # Continue in this direction until we find our disc or empty space
        while self.is_valid_position(r, c):
            if self.board[r][c] == player:
                return discs_to_flip
            elif self.board[r][c] == opponent:
                discs_to_flip.append((r, c))
                r, c = r + dr, c + dc
            else:  # Empty space
                return []

        return []

    def is_valid_move(self, row, col, player):
        """Check if a move is valid for the given player"""
        # Cell must be empty
        if self.board[row][col] != ' ':
            return False

        # Check all 8 directions
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if self.check_direction(row, col, dr, dc, player):
                    return True

        return False

    def get_valid_moves(self, player):
        """Get all valid moves for the given player"""
        valid_moves = []

        for row in range(self.size):
            for col in range(self.size):
                if self.is_valid_move(row, col, player):
                    valid_moves.append((row, col))

        return valid_moves

    def make_move(self, row, col, player):
        """Make a move and flip the appropriate discs"""
        if not self.is_valid_move(row, col, player):
            return False

        all_flips = []
        # Check all 8 directions
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                flips = self.check_direction(row, col, dr, dc, player)
                all_flips.extend(flips)

        # Place the disc and flip all affected discs
        self.board[row][col] = player
        for r, c in all_flips:
            self.board[r][c] = player

        return True

    def get_score(self):
        """Get the current score for both players"""
        black_count = sum(row.count('B') for row in self.board)
        white_count = sum(row.count('W') for row in self.board)
        return {'B': black_count, 'W': white_count}

    def is_game_over(self):
        """Check if the game is over"""
        black_moves = self.get_valid_moves('B')
        white_moves = self.get_valid_moves('W')
        return len(black_moves) == 0 and len(white_moves) == 0

    def is_board_full(self):
        """Check if the board is completely filled"""
        for row in self.board:
            if ' ' in row:
                return False
        return True

    def get_winner(self):
        """Determine the winner of the game"""
        score = self.get_score()
        if score['B'] > score['W']:
            return 'B'
        elif score['W'] > score['B']:
            return 'W'
        else:
            return 'D'  # Draw

    def copy(self):
        """Create a deep copy of the board"""
        new_board = OthelloBoard()
        new_board.board = copy.deepcopy(self.board)
        new_board.current_player = self.current_player
        return new_board

    def display(self):
        """Display the board in console"""
        print("\n  ", end="")
        for i in range(self.size):
            print(f" {i}", end="")
        print("\n  " + "-" * (self.size * 2 + 1))

        for i in range(self.size):
            print(f"{i} |", end="")
            for j in range(self.size):
                if self.board[i][j] == ' ':
                    # Show valid moves with *
                    if self.is_valid_move(i, j, self.current_player):
                        print(" *", end="")
                    else:
                        print(" .", end="")
                else:
                    print(f" {self.board[i][j]}", end="")
            print(" |")

        print("  " + "-" * (self.size * 2 + 1))

        score = self.get_score()
        print(f"\nScore: Black={score['B']}, White={score['W']}")

        # Show valid moves count
        black_moves = len(self.get_valid_moves('B'))
        white_moves = len(self.get_valid_moves('W'))
        print(f"Valid moves: Black={black_moves}, White={white_moves}")
