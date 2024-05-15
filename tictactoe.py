import sys
import pygame
import numpy as np

# COLORS
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# GAME PROPORTIONS AND SIZES
WIDTH = 300
HEIGHT = 300
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

# TIC TAC TOE BOARD
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# GAMEPLAY FUNCTIONS
def draw_lines(color=WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT), LINE_WIDTH)

def draw_figures(color=WHITE):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row*SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), CROSS_WIDTH)
                pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), CROSS_WIDTH)

# player is either 0 (for O) or 1 (for X)
def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full(check_board=board):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if check_board[row][col] == 0:
                return False
    return True

def check_win(player, check_board=board):
    for col in range(BOARD_COLS):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True
        
    for row in range(BOARD_ROWS):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True
        
    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True
    
    if check_board[2][0] == player and check_board[1][1] == player and check_board[0][2] == player:
        return True
    
    return False

def restart_game():
    screen.fill(BLACK)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

# AI ALGORITHMS
def minimax(minimax_board, depth, is_maximizing):
    if check_win(2, minimax_board):
        return float('inf')
    elif check_win(1, minimax_board):
        return float('-inf')
    elif is_board_full(minimax_board):
        return 0
    
    if is_maximizing:
        best_score = -1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth+1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth+1, True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = -1000
    move = (-1, -1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False

# TIC TAC TOE GAME LOOP
# vsAI is a boolean that indicates whether the player is facing against the AI or not
def game_loop(vsAI):
    pygame.display.set_caption('Tic Tac Toe')
    screen.fill(BLACK)
    draw_lines()
    draw_figures()

    currentPlayer = 1
    game_over = False

    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0] // SQUARE_SIZE
                mouseY = event.pos[1] // SQUARE_SIZE

                if available_square(mouseY, mouseX):
                    mark_square(mouseY, mouseX, currentPlayer)
                    if check_win(currentPlayer):
                        game_over = True
                    currentPlayer = currentPlayer % 2 + 1

                    # Make AI move if in AI mode and if game is not over
                    if vsAI and not game_over:
                        if best_move():
                            if check_win(2):
                                game_over = True
                            currentPlayer = currentPlayer % 2 + 1
                    
                    if not game_over and is_board_full():
                        game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r or event.key == pygame.K_ESCAPE:
                    restart_game()
                    game_over = False
                    currentPlayer = 1
                    if event.key == pygame.K_ESCAPE:
                        main_menu()

        if not game_over:
            draw_figures()
        else:
            if check_win(1):
                draw_figures(GREEN)
                draw_lines(GREEN)
            elif check_win(2):
                draw_figures(RED)
                draw_lines(RED)
            else:
                draw_figures(GRAY)
                draw_lines(GRAY)
        
        pygame.display.update()

# MAIN MENU PROPERTIES
TITLE_TEXT = 'Tic Tac Toe'
TITLE_TEXT_SIZE = 50
TITLE_TEXT_POS = (150, 30) # (center)
MENU_FONT = 'Calibri'

MENU_BUTTON_TEXT_SIZE = 24
MENU_BUTTON_WIDTH = 200
MENU_BUTTON_HEIGHT = 80

PVP_BUTTON_POS = (50, 70) # (top left corner)
PVP_TEXT = 'Player vs. Player'
PVP_TEXT_POS = (150, 110)

AI_BUTTON_POS = (50, 170) # (top left corner)
AI_TEXT = 'Player vs. AI'
AI_TEXT_POS = (150, 210)

INFO_TEXT = 'R = Reset Board  |  ESC = Main Menu'
INFO_TEXT_SIZE = 15
INFO_TEXT_POS = (150, 280) # (center)

# MAIN MENU FUNCTIONS
def draw_rectangle(top_left, rect_width, rect_height):
    pygame.draw.line(screen, WHITE, top_left, (top_left[0] + rect_width, top_left[1]), LINE_WIDTH)
    pygame.draw.line(screen, WHITE, top_left, (top_left[0], top_left[1] +  rect_height), LINE_WIDTH)
    pygame.draw.line(screen, WHITE, (top_left[0], top_left[1] +  rect_height), (top_left[0] + rect_width, top_left[1] + rect_height), LINE_WIDTH)
    pygame.draw.line(screen, WHITE, (top_left[0] + rect_width, top_left[1]), (top_left[0] + rect_width, top_left[1] + rect_height), LINE_WIDTH)

def render_text(text, text_size, font, position):
    surface = pygame.font.SysFont(font, text_size).render(text, True, WHITE)
    screen.blit(surface, surface.get_rect(center=position))

def within_rect(pos, top_left, rect_width, rect_height):
    if pos[0] in range(top_left[0], top_left[0] + rect_width) and pos[1] in range(top_left[1], top_left[1] + rect_height):
        return True
    return False

# MAIN MENU LOGIC LOOP
def main_menu():
    pygame.display.set_caption('Main Menu')
    screen.fill(BLACK)

    # Render title text on screen
    render_text(TITLE_TEXT, TITLE_TEXT_SIZE, MENU_FONT, TITLE_TEXT_POS)

    # Render play buttons on screen (vs. Player and vs. AI)
    draw_rectangle(PVP_BUTTON_POS, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
    draw_rectangle(AI_BUTTON_POS, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT)
    render_text(PVP_TEXT, MENU_BUTTON_TEXT_SIZE, MENU_FONT, PVP_TEXT_POS)
    render_text(AI_TEXT, MENU_BUTTON_TEXT_SIZE, MENU_FONT, AI_TEXT_POS)

    # Render info text
    render_text(INFO_TEXT, INFO_TEXT_SIZE, MENU_FONT, INFO_TEXT_POS)

    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                if within_rect((mouseX, mouseY), PVP_BUTTON_POS, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT):
                    # Start Player vs. Player game
                    game_loop(False)
                elif within_rect((mouseX, mouseY), AI_BUTTON_POS, MENU_BUTTON_WIDTH, MENU_BUTTON_HEIGHT):
                    # Start Player vs. AI game
                    game_loop(True)

        pygame.display.update()

# MAIN
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    main_menu()