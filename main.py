import os
import sys
import pygame
import requests

response = None
z = 14  # масштаб
print("Масштаб изменяется по нажатию на W и S")
coordinates = "37.530887,55.703118"
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


def get_point(name_place):
    apikey = "40d1649f-0493-4b70-98ba-98533de7710b"
    url = "http://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": apikey,
        "geocode": name_place,
        "format": "json"
    }
    response = requests.get(url, params=params)
    if not response:
        print("brrrrr")
        print(response.url)
    data = response.json()
    if data["response"]["GeoObjectCollection"]["featureMember"]:
        place = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        place_coodrinates = place["Point"]["pos"].replace(" ", ",")
        return place_coodrinates
    else:
        return ncoordinates


pygame.init()
screen = pygame.display.set_mode((600, 450))

font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()
input_box = pygame.Rect(10, 10, 140, 32)
color_inactive = pygame.Color(148, 28, 28)
color_active = pygame.Color(255, 28, 28)
color = color_inactive
active = False
text = ''
running = True
map = pygame.image.load(map_file)
types_map = ["map", "sat", "sat,skl"]
res_text = ""
count = 0
while running:
    nz = z
    ncoordinates = coordinates
    ncount = count
    keys = pygame.key.get_pressed()
    ncoordinates = [float(i) for i in ncoordinates.split(",")]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    res_text = text
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
            if event.key == pygame.K_s:
                nz -= 1
                nz = max(nz, 0)
            if event.key == pygame.K_w:
                nz += 1
                nz = min(nz, 17)
            if nz != 0:
                if event.key == pygame.K_UP:
                    ncoordinates[1] += 10000 * (1 / nz) ** 5
                if event.key == pygame.K_DOWN:
                    ncoordinates[1] -= 10000 * (1 / nz) ** 5
                if event.key == pygame.K_LEFT:
                    ncoordinates[0] -= 10000 * (1 / nz) ** 5
                if event.key == pygame.K_RIGHT:
                    ncoordinates[0] += 10000 * (1 / nz) ** 5
    ncoordinates = ",".join([str(i) for i in ncoordinates])
    if nz != z or ncoordinates != coordinates or count != ncount or res_text != "":
        if res_text != "":
            ncoordinates = get_point(res_text)
        res_text = ""
        count = ncount
        map_params = {
            "l": types_map[count],
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
        map = pygame.image.load(map_file)

    screen.blit(map, (0, 0))
    txt_surface = font.render(text, True, color)
    width = max(200, txt_surface.get_width() + 10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, color, input_box, 2)
    pygame.display.flip()
    clock.tick(30)
pygame.quit()
os.remove(map_file)
# 37.530887,55.703118
