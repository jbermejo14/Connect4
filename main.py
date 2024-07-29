import time
import random
import pygame
import sys
import json
import requests

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
gameDisplay = pygame.display.set_mode((1280, 800))
gameExit = False
table = pygame.image.load("resources/board.png")
yellow_piece_img = pygame.image.load("resources/yellow_piece.png")
red_piece_img = pygame.image.load("resources/red_piece.png")
API_GATEWAY_URL = "https://jb1wabab38.execute-api.us-east-1.amazonaws.com/dev"
move = 0
game_id = None
yellow_list = []
red_list = []

# GLOBAL TURN (CURRENT TURN) TO COMPARE WITH OWN TURN
global_turn = 1

if not pygame.get_init():
    pygame.init()

if not pygame.font.get_init():
    pygame.font.init()


class Player:
    def __init__(self, num):
        self.num = num


class Piece:
    def __init__(self, color, coords):
        self.color = color
        self.coords = coords
        self.top_rect = pygame.Rect(self.coords, (75, 75))
        if self.color == 'yellow':
            gameDisplay.blit(yellow_piece_img, (self.coords[0], self.coords[1], 10, 10))
        if self.color == 'red':
            gameDisplay.blit(red_piece_img, (self.coords[0], self.coords[1], 10, 10))

    # SENDS THE MOVE TO THE LAMBDA FUNCTION TO THEN PUT IT IN DYNAMO DB TABLE
    def lambda_move(self, game_id):
        move_id = random.randint(1, 100000)
        url = f"{API_GATEWAY_URL}/move"
        payload = {
            "move_id": move_id,
            "game_id": game_id,
            "piece": str(self),
            "turn": global_turn,
            "coords": self.coords
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return response.json()

    def graphical_move(self, col, space, piece):
        num = 0
        for i in col:
            if isinstance(i, Piece):
                num = num + 1
        if num == 0:
            self.coords = [space.coords[0], 565]
            col.append(self)
            piece.lambda_move(game_id)
        if num == 1:
            self.coords = [space.coords[0], 485]
            col.append(self)
            piece.lambda_move(game_id)
        if num == 2:
            self.coords = [space.coords[0], 405]
            col.append(self)
            piece.lambda_move(game_id)
        if num == 3:
            self.coords = [space.coords[0], 325]
            col.append(self)
        if num == 4:
            self.coords = [space.coords[0], 245]
            col.append(self)
        if num == 5:
            self.coords = [space.coords[0], 165]
        if num == 6:
            pass
        gameDisplay.blit(yellow_piece_img, (self.coords[0], self.coords[1], 10, 10))
        pygame.display.update()

    # POSTS TO DYNAMO DB ("GAME_ID, SELF.PIECE, SELF.COLOR, SELF.COORDS(NEW COORDS)")
    # TODO
    #   ADD A CHECK IF THE OWN_TURN IS THE SAME AS THE CURRENT TURN
    #   NEEDS TO CHANGE AND RETURN GLOBAL TURN!!!!!!!!


# REFRESHES THE SCREEN
def refresh():
    global game_id
    gameDisplay.fill(black)
    gameDisplay.blit(table, (320, 160))
    font = pygame.font.SysFont(None, 30)
    img = font.render('Game Num: ' + str(game_id), True, white)
    gameDisplay.blit(img, (10, 20))
    for y in yellow_list:
        gameDisplay.blit(yellow_piece_img, (y.coords[0], y.coords[1], 10, 10))
    for r in red_list:
        gameDisplay.blit(red_piece_img, (r.coords[0], r.coords[1], 10, 10))
    pygame.display.update()


class Space:
    def __init__(self, coords, piece):
        self.piece = piece
        self.coords = coords
        self.top_rect = pygame.Rect(self.coords, (80, 80))

    def get_col(self):
        for col in cols:
            for space in col:
                if self == space:
                    return col

    def check_click(self):
        global turn, move, global_turn
        posm = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(posm):
            if pygame.mouse.get_pressed()[0] is True:
                col = self.get_col()
                yellow_list[move].graphical_move(col, self, yellow_list[move])
                refresh()
                pygame.display.update()
                move = move + 1

                if global_turn == 1:
                    global_turn = 2
                elif global_turn == 2:
                    global_turn = 1

                time.sleep(0.7)


def create_board(player, gameid):
    global yellow_list, red_list, game_id, cols
    game_id = gameid

    def get_second_player():
        global data
        search_type = 'players'
        try:
            url = f"{API_GATEWAY_URL}/search?search_type={search_type}&game_id={game_id}"
            headers = {"Content-Type": "application/json"}

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = json.loads(response.json()['body'])
                for game in data:
                    if game["ID"] == str(game_id) and game["players"] == '1':
                        font = pygame.font.SysFont(None, 50)
                        img = font.render('Waiting for second player', True, white)
                        gameDisplay.blit(img, (440, 40))
                        pygame.display.update()

                        players = 1
                        return players

                    elif game["ID"] == str(game_id) and game["players"] == '2':
                        font = pygame.font.SysFont(None, 50)
                        img = font.render('Waiting for second player', True, black)
                        gameDisplay.blit(img, (440, 40))
                        pygame.display.update()
                        players = 2
                        return players

            else:
                print(f"Failed to retrieve games. Status Code: {response.status_code}")
                print("Response:", response.text)

        except Exception as e:
            print("Exception occurred:", str(e))

    gameDisplay.fill(black)
    gameDisplay.blit(table, (320, 160))

    # OWN_TURN IMPORTANT!!!
    own_turn = player.num

    # CLASSES CREATION

    # YELLOW PIECES CREATION
    yp1 = Piece('yellow', (50, 120))
    yp2 = Piece('yellow', (130, 120))
    yp3 = Piece('yellow', (210, 120))
    yp4 = Piece('yellow', (50, 200))
    yp5 = Piece('yellow', (130, 200))
    yp6 = Piece('yellow', (210, 200))
    yp7 = Piece('yellow', (50, 280))
    yp8 = Piece('yellow', (130, 280))
    yp9 = Piece('yellow', (210, 280))
    yp10 = Piece('yellow', (50, 360))
    yp11 = Piece('yellow', (130, 360))
    yp12 = Piece('yellow', (210, 360))
    yp13 = Piece('yellow', (50, 440))
    yp14 = Piece('yellow', (130, 440))
    yp15 = Piece('yellow', (210, 440))
    yp16 = Piece('yellow', (50, 520))
    yp17 = Piece('yellow', (130, 520))
    yp18 = Piece('yellow', (210, 520))
    yp19 = Piece('yellow', (50, 600))
    yp20 = Piece('yellow', (130, 600))
    yp21 = Piece('yellow', (210, 600))

    # RED PIECES CREATION
    rp1 = Piece('red', (1010, 120))
    rp2 = Piece('red', (1090, 120))
    rp3 = Piece('red', (1170, 120))
    rp4 = Piece('red', (1010, 200))
    rp5 = Piece('red', (1090, 200))
    rp6 = Piece('red', (1170, 200))
    rp7 = Piece('red', (1010, 280))
    rp8 = Piece('red', (1090, 280))
    rp9 = Piece('red', (1170, 280))
    rp10 = Piece('red', (1010, 360))
    rp11 = Piece('red', (1090, 360))
    rp12 = Piece('red', (1170, 360))
    rp13 = Piece('red', (1010, 440))
    rp14 = Piece('red', (1090, 440))
    rp15 = Piece('red', (1170, 440))
    rp16 = Piece('red', (1010, 520))
    rp17 = Piece('red', (1090, 520))
    rp18 = Piece('red', (1170, 520))
    rp19 = Piece('red', (1010, 600))
    rp20 = Piece('red', (1090, 600))
    rp21 = Piece('red', (1170, 600))

    # Column 1
    s1 = Space((335, 165), None)
    s2 = Space((335, 245), None)
    s3 = Space((335, 325), None)
    s4 = Space((335, 405), None)
    s5 = Space((335, 485), None)
    s6 = Space((335, 565), None)

    # Column 2
    s7 = Space((425, 165), None)
    s8 = Space((425, 245), None)
    s9 = Space((425, 325), None)
    s10 = Space((425, 405), None)
    s11 = Space((425, 485), None)
    s12 = Space((425, 565), None)

    # Column 3
    s13 = Space((515, 165), None)
    s14 = Space((515, 245), None)
    s15 = Space((515, 325), None)
    s16 = Space((515, 405), None)
    s17 = Space((515, 485), None)
    s18 = Space((515, 565), None)

    # Column 4
    s19 = Space((605, 165), None)
    s20 = Space((605, 245), None)
    s21 = Space((605, 325), None)
    s22 = Space((605, 405), None)
    s23 = Space((605, 485), None)
    s24 = Space((605, 565), None)

    # Column 5
    s25 = Space((695, 165), None)
    s26 = Space((695, 245), None)
    s27 = Space((695, 325), None)
    s28 = Space((695, 405), None)
    s29 = Space((695, 485), None)
    s30 = Space((695, 565), None)

    # Column 6
    s31 = Space((785, 165), None)
    s32 = Space((785, 245), None)
    s33 = Space((785, 325), None)
    s34 = Space((785, 405), None)
    s35 = Space((785, 485), None)
    s36 = Space((785, 565), None)

    # Column 7
    s37 = Space((875, 165), None)
    s38 = Space((875, 245), None)
    s39 = Space((875, 325), None)
    s40 = Space((875, 405), None)
    s41 = Space((875, 485), None)
    s42 = Space((875, 565), None)

    col1 = [s1, s2, s3, s4, s5, s6]
    col2 = [s7, s8, s9, s10, s11, s12]
    col3 = [s13, s14, s15, s16, s17, s18]
    col4 = [s19, s20, s21, s22, s23, s24]
    col5 = [s25, s26, s27, s28, s29, s30]
    col6 = [s31, s32, s33, s34, s35, s36]
    col7 = [s37, s38, s39, s40, s41, s42]

    cols = [col1, col2, col3, col4, col5, col6, col7]

    # LIST OF SPACES FOR MAKING THE CHECK_CLICK ON EACH OF THEM
    column_list = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20,
                   s21, s22, s23, s24, s25, s26, s27, s28, s29, s30, s31, s32, s33, s34, s35, s36, s37, s38,
                   s39, s40, s41, s42]

    yellow_list = [yp1, yp2, yp3, yp4, yp5, yp6, yp7, yp8, yp9, yp10, yp11, yp12, yp13, yp14, yp15, yp16, yp17, yp18,
                   yp19, yp20, yp21]

    red_list = [rp1, rp2, rp3, rp4, rp5, rp6, rp7, rp8, rp9, rp10, rp11, rp12, rp13, rp14, rp15, rp16, rp17, rp18, rp19,
                rp20, rp21]

    # ADDS THE GAME ID TO THE SCREEN
    font = pygame.font.SysFont(None, 30)
    img = font.render('Game Num: ' + str(game_id), True, white)
    gameDisplay.blit(img, (10, 20))

    pygame.display.update()
    players = get_second_player()

    # TODO
    #   REMOVED FOR TESTING
    # while players == 1:
    #     players = get_second_player()
    #
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             sys.exit()

    while not gameExit:
        # TODO
        #   AFTER A MOVE (TOUCHING A SPACE) IT SHOULD CHANGE TURN
        if own_turn == global_turn:
            for i in column_list:
                i.check_click()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
