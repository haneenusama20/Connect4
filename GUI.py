import sys
import pygame
import numpy as np
import time
ROW = 6
COLUMN = 7 
WIN = 4 
BLUE = (65,105,225)
DARKERBLUE = (6,42,120)
YELLOW = (255,255,0)
RED = (255,0,0)
BLACK = (0,0,0)
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
        for opr,opc in [[dr,dc],[dr*-1,dc*-1]]: #3ks el direction
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
        return ROW,COLUMN
    if row > 20:
        print("cant be more than 10")
        return ROW,COLUMN
    col = int(input("col: "))
    if col<COLUMN:
        print("cant be less than 7")
        return ROW,COLUMN
    if col>15:
        print("cant be more than 10")
        return ROW,COLUMN

    return row, col
def draw_board(board):
    screen.fill(DARKERBLUE)
    for c in range(COLUMN):
        for r in range(ROW):
            pygame.draw.rect(screen, BLUE, (c*SQAURESSIZE +25, r*SQAURESSIZE +SQAURESSIZE,SQAURESSIZE , SQAURESSIZE))
            piece = board[ROW - 1 - r][c]
            color = BLACK if piece == 0 else RED if piece == 1 else YELLOW
            pygame.draw.circle(screen, color, (int(c*SQAURESSIZE + SQAURESSIZE/2 +25), int(r*SQAURESSIZE + SQAURESSIZE/2 +SQAURESSIZE)), SQAURESSIZE/2 - 5)

    pygame.draw.line(screen, BLACK, (COLUMN*SQAURESSIZE +25, ROW*SQAURESSIZE +SQAURESSIZE), (25, ROW*SQAURESSIZE +SQAURESSIZE), 7)
    pygame.draw.rect(screen, DARKERBLUE, (0, ROW*SQAURESSIZE +SQAURESSIZE, width, SQAURESSIZE))
def animate_drop_peice_gui(player,row,col,board):
    x = col*SQAURESSIZE + SQAURESSIZE/2 +25
    target_y = (ROW-row)*SQAURESSIZE + SQAURESSIZE/2 
    y = SQAURESSIZE//2
    speed = 0
    while y < target_y:
        y += speed
        speed += 0.5
        draw_board(board)
        pygame.draw.circle(screen, RED if player == 1 else YELLOW, (int(x), int(y)), SQAURESSIZE/2 - 5)
        pygame.display.update()
        pygame.time.delay(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def win_announcment(screen, player):
    pygame.display.get_surface().fill((0,0,0))
    pygame.display.update()
    font = pygame.font.SysFont("monospace", 90)
    text = font.render("Player " + str(player) + " wins!", 1, (255,255,255))
    textpos = text.get_rect(centerx=screen.get_width()/2)
    screen.blit(text, textpos)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
def get_data():
    font = pygame.font.SysFont("monospace", 20)
    text = font.render("Enter row: ", 1, (255,255,255))
    text2 =font.render("Enter column: ", 1, (255,255,255))
    textChooseminimax = font.render("choose ai type  ", 1, (255,255,255))
    alpha_betapruningText = font.render("Minimax with alpha-beta pruning", 1, (255,255,255))
    expectiminimaxText = font.render("Expected Minimax", 1, (255,255,255))
    minimaxnorm = font.render("Minimax without alpha-beta prunin", 1, (255,255,255))
    circleab = pygame.Rect(335, 160, 20, 20)
    circleem = pygame.Rect(335, 210, 20, 20)
    circlemn = pygame.Rect(335, 260, 20, 20)
    pygame.display.update()
    donebtn = pygame.Rect(690, 410, 140, 36)
    inputbox1  = pygame.Rect(180, 55, 100, 32)
    inputbox2 = pygame.Rect(195, 105, 100, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')

    chooseplayerText = font.render("Choose player type", 1, (255,255,255))
    circle1 = pygame.Rect(335, 315, 20, 20)
    circle2 = pygame.Rect(335, 370, 20, 20)
    circle1Text = font.render("RED", 1, RED)
    circle2Text = font.render("YELLOW", 1, YELLOW)
    active = False
    active2 = False
    textinput1 = ''
    textinput2 = ''
    done = False
    alpha = 0
    expectimax = 0
    player =1 
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if donebtn.collidepoint(event.pos):
                    done = True
                active = inputbox1.collidepoint(event.pos)
                active2 = inputbox2.collidepoint(event.pos)
                if circleab.collidepoint(event.pos):
                    alpha = 1
                    expectimax = 0
                if circleem.collidepoint(event.pos):
                    alpha = 0
                    expectimax = 1
                if circlemn.collidepoint(event.pos):
                    alpha = 0
                    expectimax = 0
                if circle1.collidepoint(event.pos):
                    player =1 
                if circle2.collidepoint(event.pos):
                    player = 2
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        textinput1 = textinput1[:-1]
                    elif event.unicode.isdigit():
                        textinput1 += event.unicode
                elif active2:
                    if event.key == pygame.K_BACKSPACE:
                        textinput2 = textinput2[:-1]
                    elif event.unicode.isdigit():
                        textinput2 += event.unicode

        screen.fill((30, 30, 30))
        screen.blit(text, (40, 60))
        screen.blit(text2, (40, 110))
        screen.blit(textChooseminimax, (40, 160))
        screen.blit(alpha_betapruningText, (370, 158))
        screen.blit(expectiminimaxText, (370, 208))
        screen.blit(minimaxnorm, (370, 258))
        screen.blit(chooseplayerText, (40, 290))
        screen.blit(circle1Text, (370, 313))
        screen.blit(circle2Text, (370, 368))
        pygame.draw.rect(screen, color_active if active else color_inactive, inputbox1, 2)
        pygame.draw.rect(screen, color_active if active2 else color_inactive, inputbox2, 2)
        screen.blit(font.render(textinput1, True, (255, 255, 255)), (inputbox1.x + 5, inputbox1.y + 5))
        screen.blit(font.render(textinput2, True, (255, 255, 255)), (inputbox2.x + 5, inputbox2.y + 5))
        pygame.draw.circle(screen, (255, 255, 255) if alpha else (0, 0, 0), circleab.center, 10)
        pygame.draw.circle(screen, (255, 255, 255) if expectimax else (0, 0, 0), circleem.center, 10)
        pygame.draw.circle(screen, (255, 255, 255) if not alpha and not expectimax else (0, 0, 0), circlemn.center, 10)
        pygame.draw.circle(screen, RED if player == 1 else (0, 0, 0), circle1.center, 10)
        pygame.draw.circle(screen, YELLOW if player == 2 else (0, 0, 0), circle2.center, 10)
        pygame.draw.rect(screen, color_inactive, donebtn)
        done_text = font.render("Done", True, (255, 255, 255))
        screen.blit(done_text, done_text.get_rect(center=donebtn.center))
        pygame.display.update()

    row = int(textinput1) if textinput1 else ROW
    col = int(textinput2) if textinput2 else COLUMN
    if not ROW <= row <= 20 or not COLUMN <= col <= 15:
        return ROW, COLUMN, alpha, player, expectimax
    return row, col,alpha,player,expectimax
        
pygame.init()
SQAURESSIZE = 100
screen = pygame.display.set_mode((850, 460))
ROW, COLUMN,alpha,Hplayer,expecti = get_data()
width = COLUMN * SQAURESSIZE + 50
height = (ROW + 1) * SQAURESSIZE + 50
screen = pygame.display.set_mode((width, height))
board = create_board()
game_over = False
turn = 0
draw_board(board)
pygame.display.update()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            game_over = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            

            if turn == 0 and Hplayer ==1:
                position = event.pos[0] #25dna x bas 
                select = (position - 25) // SQAURESSIZE 
            
                if 0 <= select < COLUMN and is_valid_location(board,select):
                    row = get_next_open_row(board,select)
                    animate_drop_peice_gui(1,row,select,board)
                    drop_piece(board,row,select,1)
                    draw_board(board)
                    pygame.display.update()
                    if winning(board,row,select):
                        game_over = True
                        win_announcment(screen,1)
                
                
            elif turn ==1 and Hplayer ==2:
                #player 2
                position = event.pos[0] #25dna x bas 
                select = (position - 25) // SQAURESSIZE 
                if 0 <= select < COLUMN and is_valid_location(board,select):
                    row = get_next_open_row(board,select)
                    animate_drop_peice_gui(2,row,select,board)
                    drop_piece(board,row,select,2)
                    draw_board(board)
                    pygame.display.update()
                    if winning(board,row,select):
                        game_over = True
                        win_announcment(screen,2)
            elif turn ==0 and Hplayer!=1:
                print("ai logic")
            elif turn ==1 and Hplayer!=2:
                print("ai logic")
            turn+=1 #le8ayet ba2a ma el ai yed5ol fl howar 
            turn = turn%2
            

