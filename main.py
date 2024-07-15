import pygame
import sys
import json
import requests

black = pygame.Color(0, 0, 0)
white = pygame.Color(0, 0, 255)
gameDisplay = pygame.display.set_mode((1280, 800))
pygame.init()
pygame.display.set_caption("Connect4")
gameExit = False
table = pygame.image.load("resources/board.png")
yellow_piece_img = pygame.image.load("resources/yellow_piece.png")
red_piece_img = pygame.image.load("resources/red_piece.png")
gameDisplay.blit(table, (320, 160))

API_GATEWAY_URL = "https://YOUR_API_GATEWAY_INVOKE_URL"


class Piece:
    def __init__(self, color, coords):
        self.color = color
        self.coords = coords
        self.top_rect = pygame.Rect(self.coords, (75, 75))
        if self.color == 'yellow':
            gameDisplay.blit(yellow_piece_img, (self.coords[0], self.coords[1], 10, 10))
        if self.color == 'red':
            gameDisplay.blit(red_piece_img, (self.coords[0], self.coords[1], 10, 10))

    # POSTS TO DYNAMO DB ("GAME_ID, SELF.PIECE, SELF.COLOR, SELF.COORDS(NEW COORDS))
    # TODO
    # GRAPHICAL MOVEMENT
    def move(self, game_id):
        url = f"{API_GATEWAY_URL}/move"
        payload = {
            "game_id": game_id,
            "piece": self,
            "color": self.color,
            "coords": self.coords
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        return response.json()


class Space:
    def __init__(self, coords, piece):
        self.piece = None
        self.color = color
        self.coords = coords
        self.top_rect = pygame.Rect(self.coords, (75, 75))

    def check_click(self):
        posm = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(posm):
            if pygame.mouse.get_pressed()[0] is True:
                # self.select()
                pass


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


pygame.display.update()
while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
