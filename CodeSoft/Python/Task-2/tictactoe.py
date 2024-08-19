import tkinter as tk
from tkinter import messagebox
import random

def check_victory(grid, player_mark):
    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2] == player_mark:
            return True
        if grid[0][i] == grid[1][i] == grid[2][i] == player_mark:
            return True
    if grid[0][0] == grid[1][1] == grid[2][2] == player_mark or grid[0][2] == grid[1][1] == grid[2][0] == player_mark:
        return True
    return False

def is_board_full(grid):
    for row in grid:
        if " " in row:
            return False
    return True

def evaluate_position(grid, depth, maximize, alpha, beta):
    if check_victory(grid, "O"):
        return 1
    if check_victory(grid, "X"):
        return -1
    if is_board_full(grid):
        return 0

    if maximize:
        max_eval = -float('inf')
        for r in range(3):
            for c in range(3):
                if grid[r][c] == " ":
                    grid[r][c] = "O"
                    eval_score = evaluate_position(grid, depth + 1, False, alpha, beta)
                    grid[r][c] = " "
                    max_eval = max(eval_score, max_eval)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for r in range(3):
            for c in range(3):
                if grid[r][c] == " ":
                    grid[r][c] = "X"
                    eval_score = evaluate_position(grid, depth + 1, True, alpha, beta)
                    grid[r][c] = " "
                    min_eval = min(eval_score, min_eval)
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
        return min_eval

def determine_best_move(grid):
    best_eval = -float('inf')
    best_spot = None
    for r in range(3):
        for c in range(3):
            if grid[r][c] == " ":
                grid[r][c] = "O"
                eval_score = evaluate_position(grid, 0, False, -float('inf'), float('inf'))
                grid[r][c] = " "
                if eval_score > best_eval:
                    best_eval = eval_score
                    best_spot = (r, c)
    return best_spot

def handle_click(r, c):
    if cells[r][c]["text"] == " ":
        cells[r][c]["text"] = "X"
        game_board[r][c] = "X"
        if check_victory(game_board, "X"):
            messagebox.showinfo("Tic-Tac-Toe", "Congrats! You won!")
            reset_game()
        elif is_board_full(game_board):
            messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
            reset_game()
        else:
            computer_turn()

def computer_turn():
    move = determine_best_move(game_board)
    if move:
        r, c = move
        cells[r][c]["text"] = "O"
        game_board[r][c] = "O"
        if check_victory(game_board, "O"):
            messagebox.showinfo("Tic-Tac-Toe", "The computer wins!")
            reset_game()
        elif is_board_full(game_board):
            messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
            reset_game()

def reset_game():
    for r in range(3):
        for c in range(3):
            cells[r][c]["text"] = " "
            game_board[r][c] = " "

window = tk.Tk()
window.title("Tic-Tac-Toe")

game_board = [[" " for _ in range(3)] for _ in range(3)]

cells = [[None for _ in range(3)] for _ in range(3)]
for r in range(3):
    for c in range(3):
        cells[r][c] = tk.Button(window, text=" ", font=('Arial', 24), width=5, height=2,
                                command=lambda row=r, col=c: handle_click(row, col))
        cells[r][c].grid(row=r, column=c)

window.mainloop()
