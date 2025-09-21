"""
GUI version of Othello game using tkinter
"""

import tkinter as tk
from tkinter import messagebox, ttk
from game_logic import OthelloBoard
from minimax import MinimaxAI
import threading
import time

class GUIGame:
    def __init__(self):
        self.board = OthelloBoard()
        self.ai = MinimaxAI(depth=4)
        self.human_player = 'B'
        self.ai_player = 'W'
        self.current_player = 'B'
        self.game_over = False
        self.ai_thinking = False
        self.consecutive_passes = 0  # Track consecutive passes

        # GUI setup
        self.root = tk.Tk()
        self.root.title("Othello Game")
        self.root.configure(bg='#2c3e50')

        # Set window size and center it
        self.setup_window()

        # Make window non-resizable
        self.root.resizable(False, False)

        self.setup_gui()

    def setup_window(self):
        """Setup window size and position"""
        # Set fixed window size
        window_width = 550
        window_height = 720

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate position to center window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set window size and position
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    def setup_gui(self):
        """Setup the GUI components"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50', padx=10, pady=10)
        main_frame.pack()

        # Title
        title_label = tk.Label(main_frame, text="OTHELLO",
                              font=('Arial', 20, 'bold'),
                              bg='#2c3e50', fg='white')
        title_label.pack(pady=(0, 5))

        # Info frame
        info_frame = tk.Frame(main_frame, bg='#2c3e50')
        info_frame.pack(pady=5)

        # Score and info labels
        score_frame = tk.Frame(info_frame, bg='#2c3e50')
        score_frame.pack()

        self.score_label = tk.Label(score_frame, text="",
                                   font=('Arial', 11),
                                   bg='#2c3e50', fg='white')
        self.score_label.pack()

        self.turn_label = tk.Label(score_frame, text="",
                                  font=('Arial', 11, 'bold'),
                                  bg='#2c3e50', fg='white')
        self.turn_label.pack()

        self.status_label = tk.Label(score_frame, text="",
                                    font=('Arial', 9),
                                    bg='#2c3e50', fg='#ecf0f1')
        self.status_label.pack()

        # Valid moves counter
        self.moves_label = tk.Label(score_frame, text="",
                                   font=('Arial', 9),
                                   bg='#2c3e50', fg='#95a5a6')
        self.moves_label.pack()

        # Board frame
        board_container = tk.Frame(main_frame, bg='#2c3e50')
        board_container.pack(pady=5)

        board_frame = tk.Frame(board_container, bg='#27ae60', relief=tk.RAISED, bd=2)
        board_frame.pack()

        # Create board buttons
        self.buttons = []
        for i in range(8):
            row_buttons = []
            for j in range(8):
                btn = tk.Button(board_frame, width=5, height=2,
                              bg='#27ae60', relief=tk.RAISED,
                              font=('Arial', 14),
                              command=lambda r=i, c=j: self.on_cell_click(r, c))
                btn.grid(row=i, column=j, padx=1, pady=1)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        # Control buttons frame
        control_frame = tk.Frame(main_frame, bg='#2c3e50')
        control_frame.pack(pady=5)

        # Player selection
        selection_frame = tk.Frame(control_frame, bg='#2c3e50')
        selection_frame.pack(pady=3)

        tk.Label(selection_frame, text="Play as:",
                font=('Arial', 9), bg='#2c3e50', fg='white').pack(side=tk.LEFT, padx=3)

        self.player_var = tk.StringVar(value='B')
        black_radio = tk.Radiobutton(selection_frame, text="Black (First)",
                                    variable=self.player_var, value='B',
                                    command=self.change_player_color,
                                    bg='#2c3e50', fg='white',
                                    font=('Arial', 9),
                                    selectcolor='#34495e',
                                    activebackground='#2c3e50')
        black_radio.pack(side=tk.LEFT, padx=3)

        white_radio = tk.Radiobutton(selection_frame, text="White (Second)",
                                    variable=self.player_var, value='W',
                                    command=self.change_player_color,
                                    bg='#2c3e50', fg='white',
                                    font=('Arial', 9),
                                    selectcolor='#34495e',
                                    activebackground='#2c3e50')
        white_radio.pack(side=tk.LEFT, padx=3)

        # Difficulty selection
        diff_frame = tk.Frame(control_frame, bg='#2c3e50')
        diff_frame.pack(pady=3)

        tk.Label(diff_frame, text="Difficulty:",
                font=('Arial', 9), bg='#2c3e50', fg='white').pack(side=tk.LEFT, padx=3)

        self.difficulty_var = tk.StringVar(value='4')

        # Style for combobox
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox', fieldbackground='#34495e', background='#34495e')

        difficulty_combo = ttk.Combobox(diff_frame, textvariable=self.difficulty_var,
                                      values=['2', '3', '4', '5', '6'],
                                      state='readonly', width=8,
                                      font=('Arial', 9))
        difficulty_combo.pack(side=tk.LEFT, padx=3)
        difficulty_combo.bind('<<ComboboxSelected>>', self.change_difficulty)

        # Action buttons
        button_frame = tk.Frame(control_frame, bg='#2c3e50')
        button_frame.pack(pady=5)

        new_game_btn = tk.Button(button_frame, text="New Game",
                                font=('Arial', 9, 'bold'),
                                bg='#3498db', fg='white',
                                command=self.new_game, width=10, height=1)
        new_game_btn.pack(side=tk.LEFT, padx=3)

        # Pass button (for when no moves available)
        self.pass_btn = tk.Button(button_frame, text="Pass Turn",
                                 font=('Arial', 9, 'bold'),
                                 bg='#f39c12', fg='white',
                                 command=self.pass_turn, width=10, height=1,
                                 state=tk.DISABLED)
        self.pass_btn.pack(side=tk.LEFT, padx=3)

        quit_btn = tk.Button(button_frame, text="Quit",
                           font=('Arial', 9, 'bold'),
                           bg='#e74c3c', fg='white',
                           command=self.root.quit, width=10, height=1)
        quit_btn.pack(side=tk.LEFT, padx=3)

        # Initialize display
        self.update_display()
        self.check_and_handle_no_moves()

        # Start AI if it plays first
        if self.ai_player == 'B':
            self.root.after(1000, self.ai_move)

    def change_player_color(self):
        """Change player color selection"""
        if not self.game_over and not self.ai_thinking:
            response = messagebox.askyesno("New Game",
                                          "Changing color will start a new game. Continue?")
            if response:
                self.human_player = self.player_var.get()
                self.ai_player = 'W' if self.human_player == 'B' else 'B'
                self.new_game()

    def change_difficulty(self, event=None):
        """Change AI difficulty"""
        self.ai.depth = int(self.difficulty_var.get())
        self.status_label.config(text=f"Difficulty: Level {self.difficulty_var.get()}")

    def new_game(self):
        """Start a new game"""
        self.board = OthelloBoard()
        self.current_player = 'B'
        self.game_over = False
        self.ai_thinking = False
        self.consecutive_passes = 0
        self.pass_btn.config(state=tk.DISABLED)
        self.update_display()
        self.check_and_handle_no_moves()

        # Start AI if it plays first
        if self.ai_player == 'B':
            self.root.after(500, self.ai_move)

    def pass_turn(self):
        """Pass the turn when no moves are available"""
        if self.current_player == self.human_player:
            self.consecutive_passes += 1
            self.status_label.config(text="Turn passed!")
            self.pass_btn.config(state=tk.DISABLED)

            # Switch to next player
            self.current_player = 'W' if self.current_player == 'B' else 'B'
            self.update_display()

            # Check if game should end
            if self.consecutive_passes >= 2:
                self.end_game()
            else:
                self.check_and_handle_no_moves()

    def check_and_handle_no_moves(self):
        """Check if current player has no moves and handle accordingly"""
        if self.game_over:
            return

        valid_moves = self.board.get_valid_moves(self.current_player)

        if not valid_moves:
            if self.current_player == self.human_player:
                # Enable pass button for human
                self.pass_btn.config(state=tk.NORMAL)
                self.status_label.config(text="No valid moves! You must pass.")
                messagebox.showinfo("No Moves", "You have no valid moves. You must pass your turn.")
            else:
                # AI passes automatically
                self.consecutive_passes += 1
                self.status_label.config(text="AI has no moves. Turn passed.")
                self.root.after(1500, self.switch_turn)
        else:
            self.consecutive_passes = 0
            self.pass_btn.config(state=tk.DISABLED)
            self.highlight_valid_moves()

            # If it's AI's turn, make AI move
            if self.current_player == self.ai_player:
                self.root.after(500, self.ai_move)

    def on_cell_click(self, row, col):
        """Handle cell click"""
        if self.game_over or self.ai_thinking:
            return

        if self.current_player != self.human_player:
            return

        if self.board.is_valid_move(row, col, self.current_player):
            self.board.make_move(row, col, self.current_player)
            self.consecutive_passes = 0
            self.update_display()
            self.switch_turn()
        else:
            self.status_label.config(text="Invalid move! Choose a highlighted cell.")

    def switch_turn(self):
        """Switch to the next player's turn"""
        # Check if game is over
        if self.board.is_game_over() or self.consecutive_passes >= 2:
            self.end_game()
            return

        # Switch player
        self.current_player = 'W' if self.current_player == 'B' else 'B'
        self.update_display()
        self.check_and_handle_no_moves()

    def ai_move(self):
        """Make AI move in a separate thread"""
        if self.game_over or self.ai_thinking:
            return

        self.ai_thinking = True
        self.status_label.config(text="AI thinking...")

        def make_move():
            valid_moves = self.board.get_valid_moves(self.ai_player)
            if valid_moves:
                move = self.ai.get_best_move(self.board, self.ai_player)
                if move:
                    row, col = move
                    self.board.make_move(row, col, self.ai_player)
                    self.consecutive_passes = 0

            # Update GUI in main thread
            self.root.after(0, self.ai_move_complete)

        # Run AI in separate thread to prevent GUI freezing
        thread = threading.Thread(target=make_move)
        thread.daemon = True
        thread.start()

    def ai_move_complete(self):
        """Complete AI move and update display"""
        self.ai_thinking = False
        self.update_display()
        self.switch_turn()

    def highlight_valid_moves(self):
        """Highlight valid moves for human player"""
        # Clear all highlights first
        for i in range(8):
            for j in range(8):
                if self.board.board[i][j] == ' ':
                    self.buttons[i][j].config(bg='#27ae60')

        # Highlight valid moves
        if self.current_player == self.human_player and not self.game_over:
            valid_moves = self.board.get_valid_moves(self.human_player)
            for row, col in valid_moves:
                self.buttons[row][col].config(bg='#f39c12')

    def update_display(self):
        """Update the board display"""
        for i in range(8):
            for j in range(8):
                cell = self.board.board[i][j]
                if cell == 'B':
                    self.buttons[i][j].config(text='⚫',
                                            bg='#27ae60', state=tk.NORMAL)
                elif cell == 'W':
                    self.buttons[i][j].config(text='⚪',
                                            bg='#27ae60', state=tk.NORMAL)
                else:
                    self.buttons[i][j].config(text='', bg='#27ae60', state=tk.NORMAL)

        # Update score
        score = self.board.get_score()
        self.score_label.config(text=f"Black: {score['B']}  |  White: {score['W']}")

        # Update valid moves count
        black_moves = len(self.board.get_valid_moves('B'))
        white_moves = len(self.board.get_valid_moves('W'))
        self.moves_label.config(text=f"Valid moves - Black: {black_moves}, White: {white_moves}")

        # Update turn indicator
        if not self.game_over:
            if self.current_player == 'B':
                current = "Black"
            else:
                current = "White"

            if self.current_player == self.human_player:
                self.turn_label.config(text=f"Your Turn ({current})")
                if len(self.board.get_valid_moves(self.human_player)) > 0:
                    self.status_label.config(text="Click a highlighted cell")
            else:
                self.turn_label.config(text=f"AI's Turn ({current})")
                if not self.ai_thinking:
                    self.status_label.config(text="")

        # Highlight valid moves
        self.highlight_valid_moves()

    def end_game(self):
        """Handle game end"""
        self.game_over = True
        self.pass_btn.config(state=tk.DISABLED)

        winner = self.board.get_winner()
        score = self.board.get_score()

        if winner == 'D':
            message = f"It's a DRAW!\nBoth: {score['B']} discs"
            title = "Game Over - Draw"
        elif winner == self.human_player:
            message = f"Congratulations! You WON!\n\nFinal Score:\nYou: {score[self.human_player]}\nAI: {score[self.ai_player]}"
            title = "Victory!"
        else:
            message = f"AI Wins!\n\nFinal Score:\nAI: {score[self.ai_player]}\nYou: {score[self.human_player]}"
            title = "Defeat"

        self.turn_label.config(text="Game Over!")
        self.status_label.config(text=f"Winner: {title.split(' - ')[0]}")

        # Show result after a short delay
        self.root.after(500, lambda: messagebox.showinfo(title, message))

    def run(self):
        """Run the GUI game"""
        # Set minimum window size
        self.root.minsize(500, 650)
        self.root.mainloop()