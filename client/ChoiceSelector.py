import pygame
import Constants as c


class Chooser:
    def __init__(self, size, yes_image, no_image, center):
        self.yes_surf = pygame.transform.smoothscale(yes_image, size)
        self.no_surf = pygame.transform.smoothscale(no_image, size)

        # Size of each image, not the two of them side by side
        self.size = size

        # Yes = True, No = False
        self.state = False

        self.center = center
        self.yes_center = (self.center[0] - self.size[0] // 2, self.center[1])
        self.no_center = (self.center[0] + self.size[0] // 2, self.center[1])

    def draw_handler(self, screen):
        # Draws icons
        screen.blit(self.yes_surf, self.yes_surf.get_rect(center=self.yes_center))
        screen.blit(self.no_surf, self.no_surf.get_rect(center=self.no_center))

        circle_center = self.yes_center if self.state else self.no_center
        pygame.draw.circle(screen, (255, 0, 0), circle_center, self.size[0] // 1.5, width=1)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.yes_surf.get_rect(center=self.yes_center).collidepoint(event.pos):
                    self.state = True
                elif self.no_surf.get_rect(center=self.no_center).collidepoint(event.pos):
                    self.state = False
