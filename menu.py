import random
import pygame
import requests
import json
import sys
import main

gameDisplay = pygame.display.set_mode((1280, 800))
API_GATEWAY_URL = "https://jb1wabab38.execute-api.us-east-1.amazonaws.com/dev"
pygame.init()
pygame.display.set_caption("Connect4")
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 0, 255)
end = True
gameExit = False
game_id = None
data = []


class Buttons:
    def __init__(self, coords):
        self.coords = coords
        self.top_rect = pygame.Rect(self.coords[0], self.coords[1], 240, 50)


class Game:
    def __init__(self, coords, game_id):
        self.coords = coords
        self.top_rect = pygame.Rect(self.coords[0], self.coords[1], 240, 50)
        self.game_id = game_id

    def join_game(self):
        main.create_board(self.game_id)


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


def search_games():
    global data
    try:
        url = f"{API_GATEWAY_URL}/search"
        headers = {"Content-Type": "application/json"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = json.loads(response.json()['body'])

        else:
            print(f"Failed to retrieve games. Status Code: {response.status_code}")
            print("Response:", response.text)

    except Exception as e:
        print("Exception occurred:", str(e))


search_games()
pygame.display.update()
button1 = Buttons((515, 100))
update = Buttons((50, 50))

while not gameExit:
    gamelist = []
    height = 200
    font = pygame.font.SysFont(None, 50)
    posm = pygame.mouse.get_pos()
    gameDisplay.fill(black)
    img = font.render('Bienvenido a Connect4!', True, white)
    gameDisplay.blit(img, (440, 40))
    if button1.top_rect.collidepoint(posm):
        button1_img = pygame.image.load("resources/Buttons/creategame_button2.png")
        gameDisplay.blit(button1_img, (520, 100, 218, 50))
    else:
        button1_img = pygame.image.load("resources/Buttons/creategame_button.png")
        gameDisplay.blit(button1_img, (528, 102, 218, 50))

    if update.top_rect.collidepoint(posm):
        update_img = pygame.image.load("resources/Buttons/update_button2.png")
        gameDisplay.blit(update_img, (50, 50, 218, 50))
    else:
        update_img = pygame.image.load("resources/Buttons/update_button.png")
        gameDisplay.blit(update_img, (55, 55, 218, 50))

    for game in data:
        game_text = font.render(f"Game ID: {game.get('ID')}", True, white)
        gameDisplay.blit(game_text, (525, height))
        game = Game((525, height), game.get('ID'))
        gamelist.append(game)
        height += 70

    if pygame.mouse.get_pressed()[0] is True:
        posm = pygame.mouse.get_pos()
        if button1.top_rect.collidepoint(posm):
            create_game()
        if update.top_rect.collidepoint(posm):
            print(len(gamelist))
            search_games()
        for i in gamelist:
            if i.top_rect.collidepoint(posm):
                gameExit = True
                i.join_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
