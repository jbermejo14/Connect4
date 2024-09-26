import ast
import time
import random
import pygame
import sys
import json
import requests
import os

from dotenv import load_dotenv

load_dotenv()

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
gameDisplay = pygame.display.set_mode((1200, 800))

gameExit = False
table = pygame.image.load("resources/board.png")
yellow_piece_img = pygame.image.load("resources/yellow_piece.png")
red_piece_img = pygame.image.load("resources/red_piece.png")

API_GATEWAY_URL = os.getenv('AWS_API_GW_URL')
game_id = None
yellow_list = []
red_list = []
piece_list = {}
move = 0

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
    def __init__(self, color, coords, name):
        self.color = color
        self.coords = coords
        self.name = name
        self.top_rect = pygame.Rect(self.coords, (75, 75))
        if self.color == 'yellow':
            gameDisplay.blit(yellow_piece_img, (self.coords[0], self.coords[1], 10, 10))
        if self.color == 'red':
            gameDisplay.blit(red_piece_img, (self.coords[0], self.coords[1], 10, 10))

    # SENDS THE MOVE TO THE LAMBDA FUNCTION TO THEN PUT IT IN DYNAMO DB TABLE
    # TODO
    #   ADD A PIECE TAG "RP-1"... "YP-1"...

    def lambda_move(self, game_id):
        url = f"{API_GATEWAY_URL}/move"

        payload = {
            "game_id": game_id,
            "piece": self.name,
            "coords": self.coords
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return response.json()

    # IT DOESN'T SEEM TO UPDATE THE DATABASE
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
            piece.lambda_move(game_id)
        if num == 4:
            self.coords = [space.coords[0], 245]
            col.append(self)
            piece.lambda_move(game_id)
        if num == 5:
            self.coords = [space.coords[0], 165]
            col.append(self)
            piece.lambda_move(game_id)
        if num == 6:
            pass
        pygame.display.update()


# REFRESHES THE SCREEN
def refresh():
    global game_id
    gameDisplay.fill(black)
    gameDisplay.blit(table, (320, 160))
    font = pygame.font.SysFont(None, 30)
    img = font.render('Game Num: ' + str(game_id), True, white)
    gameDisplay.blit(img, (10, 20))
    try:
        for i in piece_list.values():
            if i[0].color == 'red':
                gameDisplay.blit(red_piece_img, (i[0].coords[0], i[0].coords[1], 10, 10))
            elif i[0].color == 'yellow':
                gameDisplay.blit(yellow_piece_img, (i[0].coords[0], i[0].coords[1], 10, 10))
    except Exception as e:
        print(e)
    pygame.display.update()


def get_status(game_id):
    global move_list, global_turn, move
    try:
        url = f"{API_GATEWAY_URL}/status"
        headers = {"Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            move_data_list = json.loads(response.json()['body'])
            move_list = []
            for data_move in move_data_list:
                for piece in piece_list.values():
                    piece_name = piece[1]
                    if data_move["ID"] == piece_name + str(game_id):
                        if type(data_move["coords"]) == str:
                            data_move["coords"] = ast.literal_eval(data_move["coords"])
                        piece[0].coords = data_move["coords"]

                        if piece[0].coords not in move_list:
                            move_list.append(piece[0].coords)  # ADDS THE COORDS TO A LIST TO GET THE NUM OF MOVEMENTS
                        move = len(move_list)  # TURNS THE NUM OF ITEMS IN THE LIST INTO A VARIABLE

                        # ADDS THE PIECE COORDS TO THE COLUMNS LIST

                        # TODO
                        #   WHEN A PIECE GOES ON TOP OF A PIECES OF SAME COLOR WORKS, BUT IF IS OTHER COLOR IT BUGS
                        #   PROBABLY BECAUSE IT DOESN'T GET THE COORDS PROPERLY FROM THE DB
                        try:
                            for col in cols:
                                for i in col:

                                    print("i: ", i, i.coords, "piece: ", piece[0].coords)

                                    if i.coords == piece[0].coords:
                                        if piece[0] not in col:
                                            col.append(piece[0])

                        except Exception as e:
                            print("Exception occurred in data_move:", str(e))

            if move % 2 != 0:
                global_turn = 1
                print(move, "change to 1")
            elif move % 2 == 0:
                global_turn = 2
                print(move, "change to 2")
        else:
            print(f"Failed to retrieve games. Status Code: {response.status_code}")
            print("Response:", response.text)


    except Exception as e:
        print("Exception occurred in get status:", str(e))


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
                try:
                    col = self.get_col()
                    piece_list.get(move)[0].graphical_move(col, self, piece_list.get(move)[0])

                    pygame.display.update()
                    time.sleep(0.2)
                except Exception as e:
                    print("Exception occurred in Space.check_click(): ", str(e))


def create_board(player, gameid):
    global yellow_list, red_list, game_id, cols, piece_list, global_turn
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
                waiting_font = pygame.font.SysFont(None, 50)
                for game in data:
                    if game["ID"] == str(game_id) and game["players"] == '1':
                        waiting_text = waiting_font.render('Waiting for second player', True, white)
                        gameDisplay.blit(waiting_text, (440, 40))
                        pygame.display.update()
                        players = 1
                        return players

                    elif game["ID"] == str(game_id) and game["players"] == '2':
                        waiting_text = waiting_font.render('Waiting for second player', True, black)
                        gameDisplay.blit(waiting_text, (440, 40))
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
    yp1 = Piece('yellow', [50, 120], 'yp1')
    yp2 = Piece('yellow', [130, 120], 'yp2')
    yp3 = Piece('yellow', [210, 120], 'yp3')
    yp4 = Piece('yellow', [50, 200], 'yp4')
    yp5 = Piece('yellow', [130, 200], 'yp5')
    yp6 = Piece('yellow', [210, 200], 'yp6')
    yp7 = Piece('yellow', [50, 280], 'yp7')
    yp8 = Piece('yellow', [130, 280], 'yp8')
    yp9 = Piece('yellow', [210, 280], 'yp9')
    yp10 = Piece('yellow', [50, 360], 'yp10')
    yp11 = Piece('yellow', [130, 360], 'yp11')
    yp12 = Piece('yellow', [210, 360], 'yp12')
    yp13 = Piece('yellow', [50, 440], 'yp13')
    yp14 = Piece('yellow', [130, 440], 'yp14')
    yp15 = Piece('yellow', [210, 440], 'yp15')
    yp16 = Piece('yellow', [50, 520], 'yp16')
    yp17 = Piece('yellow', [130, 520], 'yp17')
    yp18 = Piece('yellow', [210, 520], 'yp18')
    yp19 = Piece('yellow', [50, 600], 'yp19')
    yp20 = Piece('yellow', [130, 600], 'yp20')
    yp21 = Piece('yellow', [210, 600], 'yp21')

    # RED PIECES CREATION
    rp1 = Piece('red', [1010, 120], 'rp1')
    rp2 = Piece('red', [1090, 120], 'rp2')
    rp3 = Piece('red', [1170, 120], 'rp3')
    rp4 = Piece('red', [1010, 200], 'rp4')
    rp5 = Piece('red', [1090, 200], 'rp5')
    rp6 = Piece('red', [1170, 200], 'rp6')
    rp7 = Piece('red', [1010, 280], 'rp7')
    rp8 = Piece('red', [1090, 280], 'rp8')
    rp9 = Piece('red', [1170, 280], 'rp9')
    rp10 = Piece('red', [1010, 360], 'rp10')
    rp11 = Piece('red', [1090, 360], 'rp11')
    rp12 = Piece('red', [1170, 360], 'rp12')
    rp13 = Piece('red', [1010, 440], 'rp13')
    rp14 = Piece('red', [1090, 440], 'rp14')
    rp15 = Piece('red', [1170, 440], 'rp15')
    rp16 = Piece('red', [1010, 520], 'rp16')
    rp17 = Piece('red', [1090, 520], 'rp17')
    rp18 = Piece('red', [1170, 520], 'rp18')
    rp19 = Piece('red', [1010, 600], 'rp19')
    rp20 = Piece('red', [1090, 600], 'rp20')
    rp21 = Piece('red', [1170, 600], 'rp21')

    # Column 1
    s1 = Space([335, 165], None)
    s2 = Space([335, 245], None)
    s3 = Space([335, 325], None)
    s4 = Space([335, 405], None)
    s5 = Space([335, 485], None)
    s6 = Space([335, 565], None)

    # Column 2
    s7 = Space([425, 165], None)
    s8 = Space([425, 245], None)
    s9 = Space([425, 325], None)
    s10 = Space([425, 405], None)
    s11 = Space([425, 485], None)
    s12 = Space([425, 565], None)

    # Column 3
    s13 = Space([515, 165], None)
    s14 = Space([515, 245], None)
    s15 = Space([515, 325], None)
    s16 = Space([515, 405], None)
    s17 = Space([515, 485], None)
    s18 = Space([515, 565], None)

    # Column 4
    s19 = Space([605, 165], None)
    s20 = Space([605, 245], None)
    s21 = Space([605, 325], None)
    s22 = Space([605, 405], None)
    s23 = Space([605, 485], None)
    s24 = Space([605, 565], None)

    # Column 5
    s25 = Space([695, 165], None)
    s26 = Space([695, 245], None)
    s27 = Space([695, 325], None)
    s28 = Space([695, 405], None)
    s29 = Space([695, 485], None)
    s30 = Space([695, 565], None)

    # Column 6
    s31 = Space([785, 165], None)
    s32 = Space([785, 245], None)
    s33 = Space([785, 325], None)
    s34 = Space([785, 405], None)
    s35 = Space([785, 485], None)
    s36 = Space([785, 565], None)

    # Column 7
    s37 = Space([875, 165], None)
    s38 = Space([875, 245], None)
    s39 = Space([875, 325], None)
    s40 = Space([875, 405], None)
    s41 = Space([875, 485], None)
    s42 = Space([875, 565], None)

    col1 = [s1, s2, s3, s4, s5, s6]
    col2 = [s7, s8, s9, s10, s11, s12]
    col3 = [s13, s14, s15, s16, s17, s18]
    col4 = [s19, s20, s21, s22, s23, s24]
    col5 = [s25, s26, s27, s28, s29, s30]
    col6 = [s31, s32, s33, s34, s35, s36]
    col7 = [s37, s38, s39, s40, s41, s42]

    cols = [col1, col2, col3, col4, col5, col6, col7]

    # LIST OF SPACES FOR MAKING THE CHECK_CLICK ON EACH OF THEM
    column_list: list[Space] = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19,
                                s20, s21, s22, s23, s24, s25, s26, s27, s28, s29, s30, s31, s32, s33, s34, s35, s36,
                                s37, s38,
                                s39, s40, s41, s42]

    # piece_list = [yp1, rp1, yp2, rp2, yp3, rp3, yp4, rp4, yp5, rp5, yp6, rp6, yp7, rp7, yp8, rp8, yp9, rp9, yp10, rp10,
    #                yp11, rp11, yp12, rp12, yp13, rp13, yp14, rp14, yp15, rp15, yp16, rp16, yp17, rp17, yp18, rp18, yp19,
    #                rp19, yp20, rp20, yp21, rp21]

    piece_list = {
        0: (yp1, 'yp1'), 1: (rp1, 'rp1'), 2: (yp2, 'yp2'), 3: (rp2, 'rp2'),
        4: (yp3, 'yp3'), 5: (rp3, 'rp3'), 6: (yp4, 'yp4'), 7: (rp4, 'rp4'),
        8: (yp5, 'yp5'), 9: (rp5, 'rp5'), 10: (yp6, 'yp6'), 11: (rp6, 'rp6'),
        12: (yp7, 'yp7'), 13: (rp7, 'rp7'), 14: (yp8, 'yp8'), 15: (rp8, 'rp8'),
        16: (yp9, 'yp9'), 17: (rp9, 'rp9'), 18: (yp10, 'yp10'), 19: (rp10, 'rp10'),
        20: (yp11, 'yp11'), 21: (rp11, 'rp11'), 22: (yp12, 'yp12'), 23: (rp12, 'rp12'),
        24: (yp13, 'yp13'), 25: (rp13, 'rp13'), 26: (yp14, 'yp14'), 27: (rp14, 'rp14'),
        28: (yp15, 'yp15'), 29: (rp15, 'rp15'), 30: (yp16, 'yp16'), 31: (rp16, 'rp16'),
        32: (yp17, 'yp17'), 33: (rp17, 'rp17'), 34: (yp18, 'yp18'), 35: (rp18, 'rp18'),
        36: (yp19, 'yp19'), 37: (rp19, 'rp19'), 38: (yp20, 'yp20'), 39: (rp20, 'rp20'),
        40: (yp21, 'yp21'), 41: (rp21, 'rp21')
    }

    # ADDS THE GAME ID TO THE SCREEN
    font = pygame.font.SysFont(None, 30)
    img = font.render('Game Num: ' + str(game_id), True, white)
    gameDisplay.blit(img, (10, 20))

    pygame.display.update()
    players = get_second_player()

    while players == 1:
        players = get_second_player()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    while not gameExit:
        if own_turn == global_turn:
            for i in column_list:
                i.check_click()
        get_status(game_id)

        refresh()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# TODO
#   ADD TRY/EXCEPT TO ALL FUNCTIONALITIES OF THE CODE
#   ADD TAGGING
#   SPACES HAVE AN ATTRIBUTE CALLED PIECE TO INDICATE IF THERE IS A PIECE INSIDE IT, MAYBE USE IT
#   ADD AUTO REMOVING OF MOVEMENTS AND GAME ID IN DYNAMODB
#   ADD WHO STARTS BEFORE STARTING THE GAME
#
