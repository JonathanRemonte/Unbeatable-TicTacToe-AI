# Jonathan Andre V. Remonte
# TicTacToe Game w/ an Unbeatable AI implemented using MinMax Algorithm
# CMSC 170 X-1L

import tkinter as tk
import tkinter.messagebox
from tkinter import simpledialog
import copy
import random

# function for determining winning board configurations
def winner(board, player):
    # loop for checking winning rows and columns of the board
    for i in range(3):
        if all([board[i][j] == player for j in range(3)]) or all([board[j][i] == player for j in range(3)]):
            # print('all',True)
            return True
    # print(board)
    # conditional for checking winning diagonals of the board
    if board[0][0] == board[1][1] == board[2][2] == player or board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

# function for checking if the board is full
def fullBoard(board):
    return all(all(cell != '' for cell in row) for row in board)

# utility function for recognizing the winning player or a draw state
def utility(board):
    if winner(board, 'X'):
        return 1
    elif winner(board, 'O'):
        return -1
    return 0

# function that enumerates all of the next possible moves
def successors(board, player):
    branches = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                newBoard = copy.deepcopy(board)
                newBoard[i][j] = player
                branches.append(newBoard)
    return branches

# Provided pseudocde function that classifies every board configuration as terminal or non-terminal state
def value(board):
    # conditional statement that returns 1, 0, or -1 according to the terminal classification
    if isTerminal(board):
        return utility(board)
    # conditional statement that sets the player X as the maximizer
    if nextPlayer(board) == 'X':
        return maximizer(board)
    # conditional statement that sets the player O as the minimizer
    else:
        return minimizer(board)

# Provided pseudocode function for maximizer
def maximizer(board):
    m = -2
    for boardConfig in successors(board, 'X'):
        m = max(m, value(boardConfig))
    return m

# Provided pseudocode function for minimizer
def minimizer(board):
    m = 2
    for boardConfig in successors(board, 'O'):
        m = min(m, value(boardConfig))
    return m

# function checker for terminal board configs
def isTerminal(board):
    return winner(board, 'X') or winner(board, 'O') or fullBoard(board)

# function that determines the next player according to the number of moves performed
def nextPlayer(board):
    xCount = oCount = 0
    
    for row in board:
        for cell in row:
            match cell:
                case 'X': xCount += 1
                case 'O': oCount += 1

    if xCount == oCount:
        return 'X'
    return 'O'

# function responsible for getting the best move for every turn
def bestMove(board, currentPlayer):
    match currentPlayer:
        case 'O': bestScore = 2
        case 'X': bestScore = -2

    bestMove = None
    for i in range(3):
        for j in range(3):

            # performs simulation of every possible moves to empty cells
            if board[i][j] == '':
                board[i][j] = currentPlayer

                # saves the value of the move (either 1,0, or -1)
                score = value(board)

                # resets the cell
                board[i][j] = ''

                # sets the ideal score for X as 1 and -1 for O
                if currentPlayer == 'X' and score >= bestScore or currentPlayer == 'O' and score <= bestScore:
                    bestScore = score
                    bestMove = [i, j]
    # returns the index of the best move
    return bestMove

# Tkinter GUI Functions

# function responsible for overwriting the 2D board array, 
# making ai move for every after button click, and prompting a message box 
# if terminal state is reached
def buttonClick(row, col):
    global board, playerSymbol, aiSymbol
    if board[row][col] == '' and not isTerminal(board):
        board[row][col] = playerSymbol
        updateButtons()
        if not isTerminal(board):
            aiMove = bestMove(board, aiSymbol)
            board[aiMove[0]][aiMove[1]] = aiSymbol
            updateButtons()
        if isTerminal(board):
            if winner(board, aiSymbol):
                tkinter.messagebox.showinfo("Game Over", f"'{aiSymbol}' wins!")
            elif winner(board, playerSymbol):
                tkinter.messagebox.showinfo("Game Over", f"'{playerSymbol}' wins!")
            elif fullBoard(board):
                tkinter.messagebox.showinfo("Game Over", f"Draw!")
            
            resetGame()

# function responsible for updating the 2D button array
def updateButtons():
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=board[i][j])

# function for reseting the board and button arrays
def resetGame():
    global board
    board = [['', '', ''], ['', '', ''], ['', '', '']]
    updateButtons()
    if aiSymbol == 'X':
        aiFirstMove()

# function for asking the user what side to play
def playSide():
    global playerSymbol, aiSymbol
    choice = simpledialog.askstring("Choose Side", "Choose your side (X/O):").upper()
    while choice not in ['X', 'O']:
        choice = simpledialog.askstring("Choose Side", "Invalid choice. Choose your side (X/O):").upper()
    if choice == 'X':
        playerSymbol = 'X'
        aiSymbol = 'O'
    else:
        playerSymbol = 'O'
        aiSymbol = 'X'
    
    #conditional that lets ai make the first move as X
    if aiSymbol == 'X':
        aiFirstMove()
    
# function for randomizing the first move for ai
def aiFirstMove():
    global board, aiSymbol
    if aiSymbol == 'X':
        board[random.randint(0,2)][random.randint(0,2)] = aiSymbol
        updateButtons()

# Initialize the game board and Tkinter
root = tk.Tk()
root.title("Tic-Tac-Toe AI")
root.geometry("450x450+0+0")
root.configure(background='Cadet Blue')

# Separate 2D array for buttons and board values
board = [['', '', ''], ['', '', ''], ['', '', '']]
buttons = []
for i in range(3):
    buttons.append([])
    for j in range(3):
        buttons[i].append(None)
playerSymbol = ''
aiSymbol = ''

# Initialization of Tkinter buttons 
for i in range(3):
    for j in range(3):
        button = tk.Button(root, text='', font= ('Arial', 30), bg = "cadet blue", height=1, width=2,
                           command=lambda i=i, j=j: buttonClick(i, j))
        button.grid(row=i, column=j, sticky="nsew")
        buttons[i][j] = button

for i in range(3):
    root.grid_rowconfigure(i, weight=1)
for j in range(3):
    root.grid_columnconfigure(j, weight=1)

playSide()
root.mainloop()