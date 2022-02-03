import os
import sys
import pygame
import requests

response = None
z = 10  # масштаб
coordinates = input("Введите координаты(через запятую и без пробелов):\n")
map_params = {
    "l": "map",
    "ll": coordinates,
    "spn": "0.002,0.002",
    "z": z
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

if not response:
    print("Ошибка выполнения запроса:")
    print(response.url)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    nz = z
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            print("ddd")
            if event.key == pygame.K_DOWN:
                print("down")
                nz -= 1
                nz = max(nz, 1)
            elif event.key == pygame.K_UP:
                print("up")
                nz += 1
                nz = min(nz, 17)
    print(nz)
    if nz != z:
        z = nz
        map_params = {
            "l": "map",
            "ll": coordinates,
            "spn": "0.002,0.002",
            "z": z
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
pygame.quit()
os.remove(map_file)
# 37.530887,55.703118
