import sys
import pygame
import numpy as np
import time
import random
import agent
from board import Board, HUMAN, AGENT
from tree_print import print_tree
from GUI_Tree import GIU_TREE

RANDOM_DROPS_IN_EXPECTED = True #in case mesh 3yzyn, nghyrha

class GIU_GAME:
    def __init__(self):

        self.ROW = 6
        self.COLUMN = 7 
        self.WIN = 4 
        self.BLUE = (65,105,225)
        self.DARKERBLUE = (6,42,120)
        self.YELLOW = (255,255,0)
        self.RED = (255,0,0)
        self.BLACK = (0,0,0)
        self.SQAURESSIZE = 100
        
        pygame.init()
        self.screen = pygame.display.set_mode((850, 460))
        self.start()
    def create_board(self):
        board = np.zeros((self.ROW,self.COLUMN))
        return board

    def drop_piece(self,board,row ,col,piece):
        board [row][col] = piece

        

    def is_valid_location(self,board, col):
        return board[self.ROW-1][col] == 0

    def get_next_open_row(self,board,col):
        for r in range(self.ROW):
            if board[r][col] ==0:
                # awel heta fadya f col dah 
                return r
    def print_board(self,board):
        print(np.flip(board,0))#flipppppp
    def winning(self,board,lastmoveRow,lastmoveCol):
        piece = board[lastmoveRow][lastmoveCol]
        DIRECTIONS = [[0, 1], [1, 0], [1, 1], [1, -1]]
        for dr,dc in DIRECTIONS:
            count = 1
            for opr,opc in [[dr,dc],[dr*-1,dc*-1]]: #3ks el direction
                r = lastmoveRow + opr
                c = lastmoveCol + opc
                while r>=0 and r<self.ROW and c>=0 and c<self.COLUMN and board[r][c] == piece:
                    count += 1
                    r += opr
                    c += opc
            if count >= self.WIN:
                return True
        return False
    def inputBoardSize(self):
        row = int(input("row: "))
        if row < self.ROW :
            print("cant be less than 6")
            return self.ROW,self.COLUMN
        if row > 20:
            print("cant be more than 10")
            return self.ROW,self.COLUMN
        col = int(input("col: "))
        if col<self.COLUMN:
            print("cant be less than 7")
            return self.ROW,self.COLUMN
        if col>15:
            print("cant be more than 10")
            return self.ROW,self.COLUMN

        return row, col
    def draw_board(self,board):
        self.screen.fill(self.DARKERBLUE)
        for c in range(self.COLUMN):
            for r in range(self.ROW):
                pygame.draw.rect(self.screen, self.BLUE, (c*self.SQAURESSIZE +25, r*self.SQAURESSIZE +self.SQAURESSIZE,self.SQAURESSIZE , self.SQAURESSIZE))
                piece = board[self.ROW - 1 - r][c]
                color = self.BLACK if piece == 0 else self.RED if piece == 1 else self.YELLOW
                pygame.draw.circle(self.screen, color, (int(c*self.SQAURESSIZE + self.SQAURESSIZE/2 +25), int(r*self.SQAURESSIZE + self.SQAURESSIZE/2 +self.SQAURESSIZE)), self.SQAURESSIZE/2 - 5)

        pygame.draw.line(self.screen, self.BLACK, (self.COLUMN*self.SQAURESSIZE +25, self.ROW*self.SQAURESSIZE +self.SQAURESSIZE), (25, self.ROW*self.SQAURESSIZE +self.SQAURESSIZE), 7)
        pygame.draw.rect(self.screen, self.DARKERBLUE, (0, self.ROW*self.SQAURESSIZE +self.SQAURESSIZE, self.width, self.SQAURESSIZE))
        self.draw_exit_button()   # added
    def exit_button(self):
        # added: the Exit button sits in the bottom strip, under the board
        return pygame.Rect(self.width - 110, self.ROW*self.SQAURESSIZE + self.SQAURESSIZE + 8, 100, 34)

    def draw_exit_button(self):
        # added
        if not hasattr(self, "exit_font"):
            self.exit_font = pygame.font.SysFont("monospace", 20)
        button = self.exit_button()
        pygame.draw.rect(self.screen, (170, 40, 40), button)
        label = self.exit_font.render("Exit", True, (255, 255, 255))
        self.screen.blit(label, label.get_rect(center=button.center))

    def animate_drop_peice_gui(self,player,row,col,board):
        x = col*self.SQAURESSIZE + self.SQAURESSIZE/2 +25
        target_y = (self.ROW-row)*self.SQAURESSIZE + self.SQAURESSIZE/2 
        y = self.SQAURESSIZE//2
        speed = 0
        while y < target_y:
            y += speed
            speed += 0.5
            self.draw_board(board)
            pygame.draw.circle(self.screen, self.RED if player == 1 else self.YELLOW, (int(x), int(y)), self.SQAURESSIZE/2 - 5)
            pygame.display.update()
            pygame.time.delay(20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


    def win_announcment(self,screen, player, subtitle=""):
        pygame.display.get_surface().fill((0,0,0))
        pygame.display.update()
        font = pygame.font.SysFont("monospace", 90)
        if player == 0:   # added: 0 means a draw
            message = "Draw!"
        else:
            message = "Player " + str(player) + " wins!"
        text = font.render(message, 1, (255,255,255))
        textpos = text.get_rect(centerx=screen.get_width()/2)
        screen.blit(text, textpos)
        font3 = pygame.font.SysFont("monospace", 30)
        subtext = font3.render(subtitle, 1, (255,255,255))
        screen.blit(subtext, subtext.get_rect(centerx=screen.get_width()/2, y=150))
        playagainBtn = pygame.draw.rect(screen, (255,255,255), (screen.get_width()/2 - 100, screen.get_height()/2 + 100, 200, 50))
        font2 = pygame.font.SysFont("monospace", 30)
        textpa = font2.render("Play Again", 1, (0,0,0))
        textpos2 = textpa.get_rect(centerx=playagainBtn.centerx, centery=playagainBtn.centery)
        screen.blit(textpa, textpos2)
        # added: Exit button under Play Again
        exitBtn = pygame.Rect(screen.get_width()/2 - 100, screen.get_height()/2 + 170, 200, 50)
        pygame.draw.rect(screen, (170, 40, 40), exitBtn)
        textex = font2.render("Exit", 1, (255,255,255))
        screen.blit(textex, textex.get_rect(centerx=exitBtn.centerx, centery=exitBtn.centery))

        pygame.display.update()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if exitBtn.collidepoint(event.pos):   # added
                        pygame.quit()
                        sys.exit()
                    if playagainBtn.collidepoint(event.pos):
                        
                        self.start()

    def board_is_full(self, board):
    
        for c in range(self.COLUMN):
            if board[self.ROW-1][c] == 0:
                return False
        return True

    def to_agent_board(self, board, human_piece):
        
        game = Board(self.ROW, self.COLUMN)
        for c in range(self.COLUMN):
            for r in range(self.ROW):
                piece = board[r][c]
                if piece == 0:
                    break      
                if piece == human_piece:
                    game.drop(c, HUMAN)
                else:
                    game.drop(c, AGENT)
        return game

    def maybe_slip(self, board, col):
        if not (self.expecti and RANDOM_DROPS_IN_EXPECTED):
            return col
        game = self.to_agent_board(board, 1)
        options = agent.landing_options(game, col)
        columns = [c for c, p in options]
        probabilities = [p for c, p in options]
        landing = random.choices(columns, probabilities)[0]
        if landing != col:
            print("The disc slipped from column", col, "to column", landing)
        return landing

    def end_game(self, board):
        
        game = self.to_agent_board(board, 1)    
        red = game.scores[HUMAN]
        yellow = game.scores[AGENT]
        subtitle = "Red: " + str(red) + "   Yellow: " + str(yellow)
        print("Game over.", subtitle)
        if red > yellow:
            self.win_announcment(self.screen, 1, subtitle)
        elif yellow > red:
            self.win_announcment(self.screen, 2, subtitle)
        else:
            self.win_announcment(self.screen, 0, subtitle)

    def ai_move(self, board, ai_piece):
        
        human_piece = 3 - ai_piece
        game = self.to_agent_board(board, human_piece)

        if self.expecti:
            choose = agent.choose_move_expected
        elif self.alpha:
            choose = agent.choose_move_alphabeta
        else:
            choose = agent.choose_move

        pygame.display.set_caption("AI is thinking...")
        agent.set_tree_building(self.tree_console or self.tree_window)
        start_time = time.perf_counter()
        col = choose(game, self.K)
        seconds = time.perf_counter() - start_time
        pygame.display.set_caption("Your turn")

        if self.tree_console:                        
            print_tree(agent.get_tree())
        if self.tree_window and agent.get_tree() is not None:      
            GIU_TREE(agent.get_tree()).show("AI tree")   
            self.screen = pygame.display.get_surface()    
            self.draw_board(board)                     
            pygame.display.update()
        print("AI chose column", col, " nodes expanded:", agent.get_nodes(), " time:", round(seconds, 4), "s")

        col = self.maybe_slip(board, col)      # mmkn disc y slip fel expi minimax
        row = self.get_next_open_row(board, col)
        self.animate_drop_peice_gui(ai_piece, row, col, board)
        self.drop_piece(board, row, col, ai_piece)
        self.draw_board(board)
        pygame.display.update()
        pygame.event.clear(pygame.MOUSEBUTTONDOWN)   #while ai is thinking, han ignore ay clicks

        if self.board_is_full(board):
            self.end_game(board)

    def get_data(self):
        screen = self.screen
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
        inputbox3 = pygame.Rect(530, 55, 100, 32)     
        textK = font.render("Enter K: ", 1, (255,255,255))
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')

        chooseplayerText = font.render("Choose player type", 1, (255,255,255))
        circle1 = pygame.Rect(335, 315, 20, 20)
        circle2 = pygame.Rect(335, 370, 20, 20)
        circle1Text = font.render("RED", 1, self.RED)
        circle2Text = font.render("YELLOW", 1, self.YELLOW)
        # added: the user chooses how to see the tree (both are on by default)
        treeText = font.render("Show the tree", 1, (255,255,255))
        circletc = pygame.Rect(535, 315, 20, 20)
        circletw = pygame.Rect(535, 370, 20, 20)
        treeconsoleText = font.render("in the console", 1, (255,255,255))
        treewindowText = font.render("in a window", 1, (255,255,255))
        active = False
        active2 = False
        active3 = False
        textinput1 = ''
        textinput2 = ''
        textinput3 = ''
        done = False
        alpha = 0
        expectimax = 0
        player =1 
        tree_console = 1
        tree_window = 1
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if donebtn.collidepoint(event.pos):
                        done = True
                    active = inputbox1.collidepoint(event.pos)
                    active2 = inputbox2.collidepoint(event.pos)
                    active3 = inputbox3.collidepoint(event.pos)
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
                    if circletc.collidepoint(event.pos):
                        tree_console = 1 - tree_console
                    if circletw.collidepoint(event.pos):
                        tree_window = 1 - tree_window
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
                    elif active3:
                        if event.key == pygame.K_BACKSPACE:
                            textinput3 = textinput3[:-1]
                        elif event.unicode.isdigit():
                            textinput3 += event.unicode

            screen.fill((30, 30, 30))
            screen.blit(text, (40, 60))
            screen.blit(text2, (40, 110))
            screen.blit(textK, (420, 60))
            screen.blit(textChooseminimax, (40, 160))
            screen.blit(alpha_betapruningText, (370, 158))
            screen.blit(expectiminimaxText, (370, 208))
            screen.blit(minimaxnorm, (370, 258))
            screen.blit(chooseplayerText, (40, 290))
            screen.blit(circle1Text, (370, 313))
            screen.blit(circle2Text, (370, 368))
            screen.blit(treeText, (520, 290))
            screen.blit(treeconsoleText, (570, 313))
            screen.blit(treewindowText, (570, 368))
            pygame.draw.rect(screen, color_active if active else color_inactive, inputbox1, 2)
            pygame.draw.rect(screen, color_active if active2 else color_inactive, inputbox2, 2)
            pygame.draw.rect(screen, color_active if active3 else color_inactive, inputbox3, 2)
            screen.blit(font.render(textinput1, True, (255, 255, 255)), (inputbox1.x + 5, inputbox1.y + 5))
            screen.blit(font.render(textinput2, True, (255, 255, 255)), (inputbox2.x + 5, inputbox2.y + 5))
            screen.blit(font.render(textinput3, True, (255, 255, 255)), (inputbox3.x + 5, inputbox3.y + 5))
            pygame.draw.circle(screen, (255, 255, 255) if alpha else (0, 0, 0), circleab.center, 10)
            pygame.draw.circle(screen, (255, 255, 255) if expectimax else (0, 0, 0), circleem.center, 10)
            pygame.draw.circle(screen, (255, 255, 255) if not alpha and not expectimax else (0, 0, 0), circlemn.center, 10)
            pygame.draw.circle(screen, self.RED if player == 1 else (0, 0, 0), circle1.center, 10)
            pygame.draw.circle(screen, self.YELLOW if player == 2 else (0, 0, 0), circle2.center, 10)
            pygame.draw.circle(screen, (255, 255, 255) if tree_console else (0, 0, 0), circletc.center, 10)
            pygame.draw.circle(screen, (255, 255, 255) if tree_window else (0, 0, 0), circletw.center, 10)
            pygame.draw.rect(screen, color_inactive, donebtn)
            done_text = font.render("Done", True, (255, 255, 255))
            screen.blit(done_text, done_text.get_rect(center=donebtn.center))
            pygame.display.update()

        self.K = max(1, int(textinput3)) if textinput3 else 3   
        self.tree_console = bool(tree_console)     
        self.tree_window = bool(tree_window)     
        row = int(textinput1) if textinput1 else self.ROW
        col = int(textinput2) if textinput2 else self.COLUMN
        if not self.ROW <= row <= 20 or not self.COLUMN <= col <= 15:
            return self.ROW, self.COLUMN, alpha, player, expectimax
        return row, col,alpha,player,expectimax
    def start(self):
        
        
        self.ROW = 6
        self.COLUMN = 7
        self.screen = pygame.display.set_mode((850, 460))
        self.ROW, self.COLUMN,self.alpha,self.Hplayer,self.expecti = self.get_data()
        self.width = self.COLUMN * self.SQAURESSIZE + 50
        self.height = (self.ROW + 1) * self.SQAURESSIZE + 50
        self.screen = pygame.display.set_mode((self.width, self.height))
        board = self.create_board()
        game_over = False
        turn = 0
        self.draw_board(board)
        pygame.display.update()

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    game_over = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.exit_button().collidepoint(event.pos):   
                        pygame.quit()
                        sys.exit()
                    if turn == 0 and self.Hplayer ==1:
                        position = event.pos[0] #25dna x bas 
                        select = (position - 25) // self.SQAURESSIZE 
                    
                        if 0 <= select < self.COLUMN and self.is_valid_location(board,select):
                            select = self.maybe_slip(board, select)   
                            row = self.get_next_open_row(board,select)
                            self.animate_drop_peice_gui(1,row,select,board)
                            self.drop_piece(board,row,select,1)
                            self.draw_board(board)
                            pygame.display.update()
                            if self.board_is_full(board):   #game bykhlas lama el board btkon FULL
                                game_over = True
                                self.end_game(board)
                            turn+=1 #le8ayet ba2a ma el ai yed5ol fl howar 
                            turn = turn%2
                        
                        
                    elif turn ==1 and self.Hplayer ==2:
                        #player 2
                        position = event.pos[0] #25dna x bas 
                        select = (position - 25) // self.SQAURESSIZE 
                        if 0 <= select < self.COLUMN and self.is_valid_location(board,select):
                            select = self.maybe_slip(board, select)   
                            row = self.get_next_open_row(board,select)
                            self.animate_drop_peice_gui(2,row,select,board)
                            self.drop_piece(board,row,select,2)
                            self.draw_board(board)
                            pygame.display.update()
                            if self.board_is_full(board):   
                                game_over = True
                                self.end_game(board)
                            turn+=1 #le8ayet ba2a ma el ai yed5ol fl howar 
                            turn = turn%2
            if turn ==0 and self.Hplayer!=1:
                self.ai_move(board, 1)   
                turn+=1 
                turn = turn%2
            elif turn ==1 and self.Hplayer!=2:
                self.ai_move(board, 2)   
                turn+=1 
                turn = turn%2
                
                

if __name__ == "__main__":
    GIU_GAME()
