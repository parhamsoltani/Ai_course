 
"""
Othello Game Implementation
Author: Parham Soltani

"""

import sys
from console_game import ConsoleGame
from gui_game import GUIGame

def main():
    print("=" * 50)
    print("Welcome to Othello Game!")
    print("=" * 50)
    print("\nSelect game mode:")
    print("1. Console Version")
    print("2. GUI Version (Graphical Interface)")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            print("\nStarting Console Version...")
            game = ConsoleGame()
            game.play()
            break
        elif choice == '2':
            print("\nStarting GUI Version...")
            game = GUIGame()
            game.run()
            break
        elif choice == '3':
            print("Thank you for playing!")
            sys.exit(0)
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()