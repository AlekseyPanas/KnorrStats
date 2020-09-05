import pygame
from PIL import Image, ImageFilter
from enum import Enum
pygame.init()

SCREEN_SIZE = (700, 700)


class Colors(Enum):
    BLACK = (0, 0, 0)
    GRAY = (50, 50, 50)
    LIGHT_GRAY = (100, 100, 100)
    LIGHT_BLUE = (173, 216, 230)
    MAROON = (120, 0, 0)
    DARK_GREEN = (0, 102, 0)
    RED = (200, 0, 0)
    GREEN = (0, 200, 0)
    YELLOW = (155, 135, 12)


def convert():
    global bg_image, tab_image, delete_button_image, edit_button_image, new_button_image, sword_loading_image, \
           retry_button_image, typefield_image, back_button_image, arrow_button_image, yes_image, no_image
    bg_image = bg_image.convert_alpha()
    tab_image = tab_image.convert_alpha()
    edit_button_image = edit_button_image.convert_alpha()
    delete_button_image = delete_button_image.convert_alpha()
    new_button_image = new_button_image.convert_alpha()
    sword_loading_image = sword_loading_image.convert_alpha()
    retry_button_image = retry_button_image.convert_alpha()
    typefield_image = typefield_image.convert_alpha()
    back_button_image = back_button_image.convert_alpha()
    arrow_button_image = arrow_button_image.convert_alpha()
    yes_image = yes_image.convert_alpha()
    no_image = no_image.convert_alpha()


# Scales a set of coordinates to the current screen size based on a divisor factor
def cscale(*coordinate, divisor=900):
    if len(coordinate) > 1:
        return tuple([int(coordinate[x] / divisor * SCREEN_SIZE[x % 2]) for x in range(len(coordinate))])
    else:
        return int(coordinate[0] / divisor * SCREEN_SIZE[0])


# Scales a set of coordinates to the current screen size based on a divisor factor. Doesn't return integers
def posscale(*coordinate, divisor=900):
    if len(coordinate) > 1:
        return tuple([coordinate[x] / divisor * SCREEN_SIZE[x] for x in range(len(coordinate))])
    else:
        return coordinate[0] / divisor * SCREEN_SIZE[0]


# blurmargin = (top, right, bottom, left)
def create_shadow(color, surf=None, rect=False, rectsize=None, blurmargin=(50, 50, 50, 50), opacity=200, radius=7):
    if rectsize is not None:
        size = rectsize
    else:
        size = surf.get_size()

    surface = pygame.Surface((size[0] + blurmargin[1] + blurmargin[3], size[1] + blurmargin[0] + blurmargin[2]), pygame.SRCALPHA, 32)
    surface = surface.convert_alpha()

    if rect:
        pygame.draw.rect(surface, color, (blurmargin[3], blurmargin[0], size[0], size[1]))
    else:
        surface.blit(surf, (blurmargin[3], blurmargin[0]))

    # Blurs the rect surface
    surface = Image.frombytes('RGBA', surface.get_size(),
                                  pygame.image.tostring(surface, 'RGBA', False)).filter(
        ImageFilter.GaussianBlur(radius=radius))

    # Changes color of the blurred surface to 1 single color
    if not rect:
        pixels = surface.load()
        for i in range(surface.size[0]):  # for every pixel:
            for j in range(surface.size[1]):
                pixels[i, j] = (*color, pixels[i, j][3])

    surface = pygame.image.frombuffer(surface.tobytes(), surface.size, surface.mode)

    # This is how you set the transparency of this surface if needed
    surface.fill((255, 255, 255, opacity), None, pygame.BLEND_RGBA_MULT)

    return surface


# Searches raw player json to find the object matching the ID
def getPlayerFromJson(id, raw_data):
    for player in raw_data:
        if player["player_id"] == id:
            return player
    return None


bg_image = pygame.transform.smoothscale(pygame.image.load("assets/images/bg.png"), cscale(900, 900))
tab_image = pygame.transform.smoothscale(pygame.image.load("assets/images/game_tab.png"), cscale(832, 63))
typefield_image = pygame.image.load("assets/images/typefield.png")

delete_button_image = pygame.image.load("assets/images/delete_button.png")
edit_button_image = pygame.image.load("assets/images/edit_button.png")
new_button_image = pygame.image.load("assets/images/new_button.png")
add_button_image = pygame.image.load("assets/images/add_button.png")
subtract_button_image = pygame.image.load("assets/images/subtract_button.png")
retry_button_image = pygame.image.load("assets/images/retry_button.png")
back_button_image = pygame.image.load("assets/images/backbutton.png")
arrow_button_image = pygame.image.load("assets/images/arrowbutton.png")

sword_loading_image = pygame.transform.smoothscale(pygame.image.load("assets/images/knorr_sword.png"), cscale(200, 100))

no_image = pygame.image.load("assets/images/no.png")
yes_image = pygame.image.load("assets/images/yes.png")


def get_rockwell_font(size):
    return pygame.font.Font("assets/fonts/ROCCB.ttf", size)


def get_code_font(size):
    return pygame.font.Font("assets/fonts/jd_code.ttf", size)
