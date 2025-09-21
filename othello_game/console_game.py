 
"""
Console version of Othello game
"""

from game_logic import OthelloBoard
from minimax import MinimaxAI
import time

class ConsoleGame:
    def __init__(self):
        self.board = OthelloBoard()
        self.ai = MinimaxAI(depth=4)
        self.human_player = None
        self.ai_player = None
        
    def get_human_move(self):
        """Get move input from human player"""
        valid_moves = self.board.get_valid_moves(self.human_player)
        
        if not valid_moves:
            print(f"\nNo valid moves for {self.human_player}. Turn passed.")
            return None
        
        print(f"\nValid moves: {valid_moves}")
        
        while True:
            try:
                move_input = input("Enter your move (row col): ").strip()
                if move_input.lower() == 'quit':
                    return 'quit'
                
                row, col = map(int, move_input.split())
                
                if (row, col) in valid_moves:
                    return (row, col)
                else:
                    print("Invalid move! Please choose from valid moves.")
            except (ValueError, IndexError):
                print("Invalid input! Please enter row and column separated by space.")
    
    def play(self):
        """Main game loop for console version"""
        print("\n" + "=" * 50)
        print("OTHELLO GAME - Console Version")
        print("=" * 50)
        
        # Choose player color
        while True:
            choice = input("\nChoose your color (B for Black, W for White): ").upper()
            if choice in ['B', 'W']:
                self.human_player = choice
                self.ai_player = 'W' if choice == 'B' else 'B'
                break
            print("Invalid choice! Please enter B or W.")
        
        print(f"\nYou are playing as: {'Black' if self.human_player == 'B' else 'White'}")
        print(f"Computer is playing as: {'Black' if self.ai_player == 'B' else 'White'}")
        print("\nGame starting...")
        time.sleep(1)
        
        current_player = 'B'  # Black always starts
        
        while not self.board.is_game_over():
            self.board.display()
            
            if current_player == self.human_player:
                print(f"\nYour turn ({current_player})")
                move = self.get_human_move()
                
                if move == 'quit':
                    print("\nGame terminated by player.")
                    return
                elif move:
                    row, col = move
                    self.board.make_move(row, col, current_player)
                    print(f"You played: ({row}, {col})")
            else:
                print(f"\nComputer's turn ({current_player})")
                print("Thinking...")
                
                valid_moves = self.board.get_valid_moves(current_player)
                if valid_moves:
                    start_time = time.time()
                    move = self.ai.get_best_move(self.board, current_player)
                    elapsed_time = time.time() - start_time
                    
                    if move:
                        row, col = move
                        self.board.make_move(row, col, current_player)
                        print(f"Computer played: ({row}, {col})")
                        print(f"(Evaluated {self.ai.nodes_evaluated} positions in {elapsed_time:.2f}s)")
                else:
                    print("No valid moves for computer. Turn passed.")
            
            # Switch player
            current_player = 'W' if current_player == 'B' else 'B'
            time.sleep(0.5)
        
        # Game over
        print("\n" + "=" * 50)
        print("GAME OVER!")
        print("=" * 50)
        self.board.display()
        
        winner = self.board.get_winner()
        score = self.board.get_score()
        
        if winner == 'D':
            print(f"\nIt's a DRAW! Both players have {score['B']} discs.")
        elif winner == self.human_player:
            print(f"\nCongratulations! You WON!")
            print(f"Final score: You={score[self.human_player]}, Computer={score[self.ai_player]}")
        else:
            print(f"\nComputer WINS!")
            print(f"Final score: Computer={score[self.ai_player]}, You={score[self.human_player]}")