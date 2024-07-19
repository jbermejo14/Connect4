import time
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

    # POSTS TO DYNAMO DB ("GAME_ID, SELF.PIECE, SELF.COLOR, SELF.COORDS(NEW COORDS)")
    # TODO
    #   ADD A CHECK IF THE OWN_TURN IS THE SAME AS THE CURRENT TURN
    #   NEEDS TO CHANGE AND RETURN GLOBAL TURN!!!!!!!!
    #   GRAPHICAL MOVEMENT
    def move(self, game_id):
        url = f"{API_GATEWAY_URL}/move"
        payload = {
            "game_id": game_id,
            "piece": self,
            "turn": global_turn,
            "coords": self.coords
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return response.json()


class Space:
    def __init__(self, coords, piece):
        self.piece = piece
        self.coords = coords
        self.top_rect = pygame.Rect(self.coords, (80, 80))

    def check_click(self):
        global turn
        posm = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(posm):
            if pygame.mouse.get_pressed()[0] is True:
                pass
#             TODO
#                   ADD THE MOVE FUNCTION


def create_board(game_id, player):
    print(player)
    def get_second_player():
        # TODO
        #   GET FROM DB IF A SECOND PLAYER HAS ENTER THE GAME
        pass

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

    # LIST OF SPACES FOR MAKING THE CHECK_CLICK ON EACH OF THEM
    column_list = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20,
                   s21, s22, s23, s24, s25, s26, s27, s28, s29, s30, s31, s32, s33, s34, s35, s36, s37, s38,
                   s39, s40, s41, s42]

    # ADDS THE GAME ID TO THE SCREEN
    font = pygame.font.SysFont(None, 30)
    img = font.render('Game Num: ' + str(game_id), True, white)
    gameDisplay.blit(img, (10, 20))

    pygame.display.update()

    while not gameExit:
        # TODO
        #   GET GET IF A SECOND PLAYER HAS CONNECTED THEN START THE GAME
        #   UNTIL THEN, 'WAIT FOR SECOND PLAYER' TEXT SHOULD APPEAR
        get_second_player()
        if own_turn == global_turn:
            for i in column_list:
                i.check_click()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
