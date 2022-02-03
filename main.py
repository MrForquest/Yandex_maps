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
    ncoordinates = coordinates
    keys = pygame.key.get_pressed()
    ncoordinates = [float(i) for i in ncoordinates.split(",")]
    if keys[pygame.K_s]:
        nz -= 1
        nz = max(nz, 0)
    if keys[pygame.K_w]:
        nz += 1
        nz = min(nz, 17)
    if nz != 0:
        if keys[pygame.K_UP]:
            ncoordinates[1] += 10000 * (1 / nz) ** 5
        if keys[pygame.K_DOWN]:
            ncoordinates[1] -= 10000 * (1 / nz) ** 5
        if keys[pygame.K_LEFT]:
            ncoordinates[0] -= 10000 * (1 / nz) ** 5
        if keys[pygame.K_RIGHT]:
            ncoordinates[0] += 10000 * (1 / nz) ** 5
    ncoordinates = ",".join([str(i) for i in ncoordinates])
    if nz != z or ncoordinates != coordinates:
        map_params = {
            "l": "map",
            "ll": ncoordinates,
            "z": nz
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"

        response = requests.get(map_api_server, params=map_params)
        if not response:
            print("Ошибка выполнения запроса:")
            print(response.url)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            continue
        z = nz
        coordinates = ncoordinates
        map_file = "map.png"
        os.remove(map_file)
        with open(map_file, "wb") as file:
            file.write(response.content)
        screen.fill("black")
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
pygame.quit()
os.remove(map_file)
# 37.530887,55.703118
