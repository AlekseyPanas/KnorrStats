import pygame
from PIL import Image, ImageFilter
from enum import Enum
pygame.init()

SCREEN_SIZE = (900, 900)


class Colors(Enum):
    BLACK = (0, 0, 0)
    GRAY = (50, 50, 50)


def convert():
    global bg_image, tab_image, delete_button_image, edit_button_image, new_button_image
    bg_image = bg_image.convert_alpha()
    tab_image = tab_image.convert_alpha()
    edit_button_image = edit_button_image.convert_alpha()
    delete_button_image = delete_button_image.convert_alpha()
    new_button_image = new_button_image.convert_alpha()


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


bg_image = pygame.transform.scale(pygame.image.load("assets/images/bg.png"), cscale(900, 900))
tab_image = pygame.transform.scale(pygame.image.load("assets/images/game_tab.png"), cscale(832, 63))

delete_button_image = pygame.image.load("assets/images/delete_button.png")
edit_button_image = pygame.image.load("assets/images/edit_button.png")
new_button_image = pygame.image.load("assets/images/new_button.png")
add_button_image = pygame.image.load("assets/images/add_button.png")
subtract_button_image = pygame.image.load("assets/images/subtract_button.png")


def get_rockwell_font(size):
    return pygame.font.Font("assets/fonts/ROCCB.ttf", size)
