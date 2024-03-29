import pygame

pygame.init()

# Define the design
WIDTH = 1000
HEIGHT = 1000
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('UltraCHESS')
font = pygame.font.Font('res/Pix.ttf', 20)
medium_font = pygame.font.Font('res/Pix.ttf', 40)
big_font = pygame.font.Font('res/Pix.ttf', 50)
start_screen_font = pygame.font.Font('res/Pix.ttf', 100)
timer = pygame.time.Clock()
fps = 60

# Game variables
white = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
whiteCoords = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
blackCoords = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

acquiredWhite = []
acquiredBlack = []
step = 0 # 0: white(no sel); 1:white turn(sel. piece); 2: black turn(no sel), 3: black turn(sel. piece)
selection = 100
valid_moves = []

# Load images for pieces(sprites), initialise em
# Pieces defined like this: "{first letter of color}_{piece name}"
b_queen = pygame.image.load('res/images/b_queen.png')
b_queen = pygame.transform.scale(b_queen, (80, 80))
b_queen_small = pygame.transform.scale(b_queen, (45, 45))
b_king = pygame.image.load('res/images/b_king.png')
b_king = pygame.transform.scale(b_king, (80, 80))
b_king_small = pygame.transform.scale(b_king, (45, 45))
b_rook = pygame.image.load('res/images/b_rook.png')
b_rook = pygame.transform.scale(b_rook, (80, 80))
b_rook_small = pygame.transform.scale(b_rook, (45, 45))
b_bishop = pygame.image.load('res/images/b_bishop.png')
b_bishop = pygame.transform.scale(b_bishop, (80, 80))
b_bishop_small = pygame.transform.scale(b_bishop, (45, 45))
b_knight = pygame.image.load('res/images/b_knight.png')
b_knight = pygame.transform.scale(b_knight, (80, 80))
b_knight_small = pygame.transform.scale(b_knight, (45, 45))
b_pawn = pygame.image.load('res/images/b_pawn.png')
b_pawn = pygame.transform.scale(b_pawn, (65, 65))
b_pawn_small = pygame.transform.scale(b_pawn, (45, 45))
w_queen = pygame.image.load('res/images/w_queen.png')
w_queen = pygame.transform.scale(w_queen, (80, 80))
w_queen_small = pygame.transform.scale(w_queen, (45, 45))
w_king = pygame.image.load('res/images/w_king.png')
w_king = pygame.transform.scale(w_king, (80, 80))
w_king_small = pygame.transform.scale(w_king, (45, 45))
w_rook = pygame.image.load('res/images/w_rook.png')
w_rook = pygame.transform.scale(w_rook, (80, 80))
w_rook_small = pygame.transform.scale(w_rook, (45, 45))
w_bishop = pygame.image.load('res/images/w_bishop.png')
w_bishop = pygame.transform.scale(w_bishop, (80, 80))
w_bishop_small = pygame.transform.scale(w_bishop, (45, 45))
w_knight = pygame.image.load('res/images/w_knight.png')
w_knight = pygame.transform.scale(w_knight, (80, 80))
w_knight_small = pygame.transform.scale(w_knight, (45, 45))
w_pawn = pygame.image.load('res/images/w_pawn.png')
w_pawn = pygame.transform.scale(w_pawn, (65, 65))
w_pawn_small = pygame.transform.scale(w_pawn, (45, 45))

w_figures_sprites = [w_pawn, w_queen, w_king,
                w_knight, w_rook, w_bishop]
wS_figures_sprites = [w_pawn_small, w_queen_small, w_king_small, w_knight_small,
                      w_rook_small, w_bishop_small]
b_figures_sprites = [b_pawn, b_queen, b_king,
                b_knight, b_rook, b_bishop]
wS_figures_sprites = [b_pawn_small, b_queen_small, b_king_small, b_knight_small,
                      b_rook_small, b_bishop_small]
pieces = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
counter = 0
winner = ''
game_over = False


# Board-drawing function
def draw_board():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, (32, 32, 32), [
                             600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, (32, 32, 32), [
                             700 - (column * 200), row * 100, 100, 100])
        pygame.draw.rect(screen, (48, 48, 48), [0, 800, WIDTH, 100])
        pygame.draw.rect(screen, (255, 255, 255), [0, 800, WIDTH, 100], 5)
        pygame.draw.rect(screen, (255, 255, 255), [800, 0, 200, HEIGHT], 5)
        status_text = ['Current Move: White', 'Make your move, White',
                       'Current Move: Black', 'Make your move, Black']
        screen.blit(big_font.render(
            status_text[step], True, 'white'), (20, 820))
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
        screen.blit(medium_font.render('Give Up', True, 'red'), (810, 830))


# Piece-drawing function
def draw_pieces():
    for i in range(len(white)):
        index = pieces.index(white[i])
        if white[i] == 'pawn':
            screen.blit(
                w_pawn, (whiteCoords[i][0] * 100 + 22, whiteCoords[i][1] * 100 + 30))
        else:
            screen.blit(w_figures_sprites[index], (whiteCoords[i]
                        [0] * 100 + 10, whiteCoords[i][1] * 100 + 10))
        if step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'green', [whiteCoords[i][0] * 100 + 1, whiteCoords[i][1] * 100 + 1,
                                                 100, 100], 2)

    for i in range(len(black)):
        index = pieces.index(black[i])
        if black[i] == 'pawn':
            screen.blit(
                b_pawn, (blackCoords[i][0] * 100 + 22, blackCoords[i][1] * 100 + 30))
        else:
            screen.blit(b_figures_sprites[index], (blackCoords[i]
                        [0] * 100 + 10, blackCoords[i][1] * 100 + 10))
        if step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'green', [blackCoords[i][0] * 100 + 1, blackCoords[i][1] * 100 + 1,
                                                  100, 100], 2)


# Piece-move(hinting system) validation
def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list


# King moves
def check_king(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = blackCoords
        friends_list = whiteCoords
    else:
        friends_list = blackCoords
        enemies_list = whiteCoords
    # 8 squares to check for kings, they can go one square any direction
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0),
               (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


# Queen moves
def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list


# Bishop moves
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = blackCoords
        friends_list = whiteCoords
    else:
        friends_list = blackCoords
        enemies_list = whiteCoords
    for i in range(4):
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append(
                    (position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# Rook moves
def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = blackCoords
        friends_list = whiteCoords
    else:
        friends_list = blackCoords
        enemies_list = whiteCoords
    for i in range(4):
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append(
                    (position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# Pawn moves
def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        if (position[0], position[1] + 1) not in whiteCoords and \
                (position[0], position[1] + 1) not in blackCoords and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
        if (position[0], position[1] + 2) not in whiteCoords and \
                (position[0], position[1] + 2) not in blackCoords and position[1] == 1:
            moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in blackCoords:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in blackCoords:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in whiteCoords and \
                (position[0], position[1] - 1) not in blackCoords and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
        if (position[0], position[1] - 2) not in whiteCoords and \
                (position[0], position[1] - 2) not in blackCoords and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in whiteCoords:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in whiteCoords:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list


# Knight moves
def check_knight(position, color):
    moves = []
    if color == 'white':
        oppPieces = blackCoords
        selfPieces = whiteCoords
    else:
        selfPieces = blackCoords
        oppPieces = whiteCoords
    targets = [(1, 2), (1, -2), (2, 1), (2, -1),
               (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in selfPieces and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves.append(target)
    return moves


# Check valid moves
def check_valid_moves():
    if step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options


# Draw hints
def draw_valid(moves):
    if step < 2:
        color = 'green'
    else:
        color = 'green'
    for i in range(len(moves)):
        pygame.draw.circle(
            screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)


# Draw acquired pieces
def draw_captured():
    for i in range(len(acquiredWhite)):
        captured_piece = acquiredWhite[i]
        index = pieces.index(captured_piece)
        screen.blit(wS_figures_sprites[index], (825, 5 + 50 * i))
    for i in range(len(acquiredBlack)):
        captured_piece = acquiredBlack[i]
        index = pieces.index(captured_piece)
        screen.blit(wS_figures_sprites[index], (925, 5 + 50 * i))


# If king is in check, draw the check square around him
def draw_check():
    if step < 2:
        if 'king' in white:
            king_index = white.index('king')
            king_location = whiteCoords[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [whiteCoords[king_index][0] * 100 + 1,
                                                              whiteCoords[king_index][1] * 100 + 1, 100, 100], 5)
    else:
        if 'king' in black:
            king_index = black.index('king')
            king_location = blackCoords[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [blackCoords[king_index][0] * 100 + 1,
                                                               blackCoords[king_index][1] * 100 + 1, 100, 100], 5)


def draw_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    screen.blit(font.render(
        f'{winner} is the winner! Congrats!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Press RETURN or ENTER to restart the game!',
                True, 'white'), (210, 240))


start_menu = True
start_button_rect = pygame.Rect(300, 400, 400, 100)
quit_button_rect = pygame.Rect(300, 550, 400, 100)

while start_menu:
    screen.fill((32, 32, 32))

    pygame.draw.rect(screen, (0, 255, 0), start_button_rect)
    pygame.draw.rect(screen, (255, 0, 0), quit_button_rect)

    screen.blit(start_screen_font.render("UltraCHESS", True, 'gray'), (220, 150))
    screen.blit(medium_font.render("created by Yes & levs16", True, 'gray'), (276, 680))
    screen.blit(medium_font.render("version 1.1.3", True, 'gray'), (402, 720))
    screen.blit(medium_font.render("Start Game", True, 'dark green'), (376, 430))
    screen.blit(medium_font.render("Quit", True, 'dark red'), (460, 580))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start_menu = False
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if start_button_rect.collidepoint(event.pos):
                start_menu = False
            elif quit_button_rect.collidepoint(event.pos):
                start_menu = False
                exit()

# Main game loop
black_options = check_options(black, blackCoords, 'black')
white_options = check_options(white, whiteCoords, 'white')
run = True
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            if step <= 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'black'
                if click_coords in whiteCoords:
                    selection = whiteCoords.index(click_coords)
                    if step == 0:
                        step = 1
                if click_coords in valid_moves and selection != 100:
                    whiteCoords[selection] = click_coords
                    if click_coords in blackCoords:
                        black_piece = blackCoords.index(click_coords)
                        acquiredWhite.append(black[black_piece])
                        if black[black_piece] == 'king':
                            winner = 'white'
                        black.pop(black_piece)
                        blackCoords.pop(black_piece)
                    black_options = check_options(
                        black, blackCoords, 'black')
                    white_options = check_options(
                        white, whiteCoords, 'white')
                    step = 2
                    selection = 100
                    valid_moves = []
            if step > 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'white'
                if click_coords in blackCoords:
                    selection = blackCoords.index(click_coords)
                    if step == 2:
                        step = 3
                if click_coords in valid_moves and selection != 100:
                    blackCoords[selection] = click_coords
                    if click_coords in whiteCoords:
                        white_piece = whiteCoords.index(click_coords)
                        acquiredBlack.append(white[white_piece])
                        if white[white_piece] == 'king':
                            winner = 'black'
                        white.pop(white_piece)
                        whiteCoords.pop(white_piece)
                    black_options = check_options(
                        black, blackCoords, 'black')
                    white_options = check_options(
                        white, whiteCoords, 'white')
                    step = 0
                    selection = 100
                    valid_moves = []
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                whiteCoords = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                black = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                blackCoords = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                acquiredWhite = []
                acquiredBlack = []
                step = 0
                selection = 100
                valid_moves = []
                black_options = check_options(
                    black, blackCoords, 'black')
                white_options = check_options(
                    white, whiteCoords, 'white')

    if winner != '':
        game_over = True
        draw_game_over()

    pygame.display.flip()

pygame.quit()
