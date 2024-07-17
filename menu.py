import random
import pygame
import requests
import json
import sys

gameDisplay = pygame.display.set_mode((1280, 800))
API_GATEWAY_URL = "https://jb1wabab38.execute-api.us-east-1.amazonaws.com/dev"
pygame.init()
pygame.display.set_caption("Connect4")
black = pygame.Color(0, 0, 0)
white = pygame.Color(0, 255, 255)
end = True
gameExit = False
game_id = None


class InitButtons:
    def __init__(self, coords):
        self.coords = coords
        self.top_rect = pygame.Rect(self.coords[0], self.coords[1], 240, 50)


# CREATES A MULTIPLAYER GAME
def create_game():
    global game_id
    game_id = random.randint(1, 10000)
    url = f"{API_GATEWAY_URL}/create"
    payload = {"game_id": game_id}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        return {"error": "HTTP error occurred", "details": str(http_err)}

    except Exception as err:
        return {"error": "An error occurred", "details": str(err)}


# SEARCH CREATED GAMES WAITING FOR
# IT SHOULD GET A LIST OF CREATED GAMES FROM DYNAMODB
# WHEN CLICKING IN A CREATED GAME, IT SHOULD JOIN THE GAME (CREATE THE GAME WITH THE OTHER PLAYER)
def search_games(query_type, query_value):
    url = f"{API_GATEWAY_URL}/search"
    params = {"query_type": query_type, "query_value": query_value}
    response = requests.get(url, params=params)
    return response.json()



pygame.display.update()
button1 = InitButtons((392, 100))

while not gameExit:
    font = pygame.font.SysFont(None, 50)
    posm = pygame.mouse.get_pos()
    if button1.top_rect.collidepoint(posm):
        bg = pygame.image.load("resources/bg.png")
        gameDisplay.blit(bg, (0, 0))
        button1_img = pygame.image.load("resources/Buttons/creategame_button2.png")
        gameDisplay.blit(button1_img, (392, 100, 218, 50))
        img = font.render('Bienvenido a Connect4!', True, white)
        gameDisplay.blit(img, (320, 40))
    else:
        bg = pygame.image.load("resources/bg.png")
        gameDisplay.blit(bg, (0, 0))
        button1_img = pygame.image.load("resources/Buttons/creategame_button.png")
        gameDisplay.blit(button1_img, (403, 102, 218, 50))
        img = font.render('Bienvenido a Connect4!', True, white)
        gameDisplay.blit(img, (320, 40))

    if pygame.mouse.get_pressed()[0] is True:
        posm = pygame.mouse.get_pos()
        if button1.top_rect.collidepoint(posm):
            create_game()
            import main

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()


# TODO
# ADD SEARCH GAMES FROM DYNAMODB WITH API GW
