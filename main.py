import os
import sys
import pygame
import requests

response = None
z = 14  # масштаб
print("Масштаб изменяется по нажатию на W и S")
coordinates = input("Введите координаты(через запятую и без пробелов):\n")
map_params = {
    "l": "map",
    "ll": coordinates,
    "z": str(z)
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
    keys = pygame.key.get_pressed()

    if keys[pygame.K_s]:
        nz -= 1
        nz = max(nz, 0)
    elif keys[pygame.K_w]:
        nz += 1
        nz = min(nz, 17)

    if nz != z:
        z = nz
        map_params = {
            "l": "map",
            "ll": coordinates,
            "z": z
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        os.remove(map_file)
        response = requests.get(map_api_server, params=map_params)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        screen.fill("black")
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
pygame.quit()
os.remove(map_file)
# 37.530887,55.703118
