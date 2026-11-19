import sys
import pygame
import numpy as np
ROW = 6
COLUMN = 7 
WIN = 4 

def create_board():
    board = np.zeros((ROW,COLUMN))
    return board

def drop_piece(board,row ,col,piece):
    board [row][col] = piece

    

def is_valid_location(board, col):
    return board[ROW-1][col] == 0

def get_next_open_row(board,col):
    for r in range(ROW):
        if board[r][col] ==0:
            # awel heta fadya f col dah 
            return r
def print_board(board):
    print(np.flip(board,0))#flipppppp
def winning(board,lastmoveRow,lastmoveCol):
    piece = board[lastmoveRow][lastmoveCol]
    DIRECTIONS = [[0, 1], [1, 0], [1, 1], [1, -1]]
    for dr,dc in DIRECTIONS:
        count = 1
        for opr,opc in [[dr,dc],[dr*-1,dc*-1]]:
            r = lastmoveRow + opr
            c = lastmoveCol + opc
            while r>=0 and r<ROW and c>=0 and c<COLUMN and board[r][c] == piece:
                count += 1
                r += opr
                c += opc
        if count == WIN:
            return True
    return False
def inputBoardSize():
    row = int(input("row: "))
    if row < ROW :
        print("cant be less than 6")
    col = int(input("col: "))
    if col<COLUMN:
        print("cant be less than 7")
        
    return row, col

ROW, COLUMN = inputBoardSize()
board = create_board()
game_over=False
turn = 0 # 0 = player 1 1 = 2 
while not game_over:
    if turn == 0:
        select = int(input("player1 "))
        if is_valid_location(board,select):
            row = get_next_open_row(board,select)
            drop_piece(board,row,select,1)
            if winning(board,row,select):
                game_over = True
                print("player 1 wins")
        
        
    else:
        #player 2
        select = int(input("player2 "))
        if is_valid_location(board,select):
            row = get_next_open_row(board,select)
            drop_piece(board,row,select,2)
            if winning(board,row,select):
                game_over = True
                print("player 2 wins")
    turn+=1
    turn = turn%2
    print_board(board)

