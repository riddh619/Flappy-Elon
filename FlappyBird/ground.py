# 
#  ground.py    Infinitely scrolling ground
# 

import pygame
from config import *


class Ground:
    """
    Tiles the ground image horizontally and scrolls it left
    at GROUND_SPEED px/frame to match pipe movement.

    We keep two copies side-by-side and wrap them seamlessly.
    """

    def __init__(self):
        raw = pygame.image.load(IMG_GROUND).convert()

        # Scale to full window width, fixed ground height
        self.image = pygame.transform.scale(raw, (WINDOW_WIDTH, GROUND_HEIGHT))
        self.y     = WINDOW_HEIGHT - GROUND_HEIGHT

        # Two side-by-side copies for seamless looping
        self.x1 = 0
        self.x2 = WINDOW_WIDTH

    def update(self, speed=GROUND_SPEED):
        self.x1 -= speed
        self.x2 -= speed

        # When a copy scrolls fully off the left, jump it to the right
        if self.x1 + WINDOW_WIDTH <= 0:
            self.x1 = self.x2 + WINDOW_WIDTH
        if self.x2 + WINDOW_WIDTH <= 0:
            self.x2 = self.x1 + WINDOW_WIDTH

    def draw(self, surface):
        surface.blit(self.image, (self.x1, self.y))
        surface.blit(self.image, (self.x2, self.y))

    @property
    def top_y(self):
        """Y coordinate of the top of the ground strip."""
        return self.y
