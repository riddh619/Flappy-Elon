# 
#  pipe.py    Pipe pair (top + bottom)
# 

import pygame
import random
from config import *


class Pipe:
    """
    Represents one top+bottom pipe pair.

    The pipe image (cap facing UP) is used as-is for the bottom pipe.
    It is flipped vertically for the top pipe.

    gap_y  = y-coordinate of the TOP edge of the gap.
    """

    PIPE_IMG      = None   # class-level cache so we load once
    PIPE_IMG_FLIP = None

    @classmethod
    def load_assets(cls):
        raw = pygame.image.load(IMG_PIPE).convert_alpha()
        # Scale to a fixed rendered width; height kept tall enough to fill screen
        scale_h = WINDOW_HEIGHT   # generous  we offset it out of view
        cls.PIPE_IMG      = pygame.transform.scale(raw, (PIPE_WIDTH, scale_h))
        cls.PIPE_IMG_FLIP = pygame.transform.flip(cls.PIPE_IMG, False, True)

    def __init__(self, speed=PIPE_SPEED):
        # Random vertical gap position
        gap_y = random.randint(PIPE_MIN_HEIGHT, PIPE_MAX_HEIGHT)

        self.speed   = speed
        self.scored  = False   # True once the bird has passed this pair

        img_h = self.PIPE_IMG.get_height()

        # Bottom pipe rect  cap at top, body extends down off-screen
        self.rect_bottom = self.PIPE_IMG.get_rect()
        self.rect_bottom.topleft = (WINDOW_WIDTH, gap_y + PIPE_GAP)

        # Top pipe rect  cap faces down (flipped), body extends up off-screen
        self.rect_top = self.PIPE_IMG_FLIP.get_rect()
        self.rect_top.bottomleft = (WINDOW_WIDTH, gap_y)

        # Collision masks
        self.mask_bottom = pygame.mask.from_surface(self.PIPE_IMG)
        self.mask_top    = pygame.mask.from_surface(self.PIPE_IMG_FLIP)

    #  Public API 

    def update(self):
        self.rect_bottom.x -= int(self.speed)
        self.rect_top.x    -= int(self.speed)

    def draw(self, surface):
        surface.blit(self.PIPE_IMG,      self.rect_bottom)
        surface.blit(self.PIPE_IMG_FLIP, self.rect_top)

    def is_off_screen(self):
        return self.rect_bottom.right < 0

    def collides_with(self, bird):
        """Pixel-accurate collision check against bird."""
        bird_mask, bird_rect = bird.get_mask()

        # Check bottom pipe
        offset_b = (self.rect_bottom.x - bird_rect.x,
                    self.rect_bottom.y - bird_rect.y)
        if bird_mask.overlap(self.mask_bottom, offset_b):
            return True

        # Check top pipe
        offset_t = (self.rect_top.x - bird_rect.x,
                    self.rect_top.y - bird_rect.y)
        if bird_mask.overlap(self.mask_top, offset_t):
            return True

        return False

    def bird_passed(self, bird):
        """Returns True the first time the bird's x clears this pipe."""
        if not self.scored and bird.rect.left > self.rect_bottom.right:
            self.scored = True
            return True
        return False
