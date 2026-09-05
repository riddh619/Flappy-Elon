# 
#  bird.py    Bird sprite, physics, animation
# 

import pygame
import os
from config import *


class Bird:
    """
    Handles the player-controlled bird.

    Physics:
        - Gravity pulls the bird down every frame.
        - flap() gives an instant upward velocity burst.
        - Rotation is derived from vertical velocity so the
          bird tilts up on flap and nose-dives when falling.
    """

    MAX_UP_ANGLE   =  25   # degrees tilted up  on flap
    MAX_DOWN_ANGLE = -70   # degrees tilted down at terminal velocity

    def __init__(self):
        # Load & scale sprite
        raw = pygame.image.load(IMG_BIRD).convert_alpha()
        self.image_orig = pygame.transform.scale(raw, (BIRD_WIDTH, BIRD_HEIGHT))

        self.rect     = self.image_orig.get_rect(center=(BIRD_START_X, BIRD_START_Y))
        self.velocity = 0          # current vertical speed (+ = down)
        self.angle    = 0          # current render angle
        self.alive    = True

        # Mask for pixel-accurate collision
        self.mask = pygame.mask.from_surface(self.image_orig)

    #  Public API 

    def flap(self):
        """Called on spacebar / click."""
        if self.alive:
            self.velocity = JUMP_STRENGTH

    def update(self):
        """Advance physics one frame."""
        if not self.alive:
            # Still fall after death for death animation
            self.velocity = min(self.velocity + GRAVITY * 2, MAX_FALL_SPEED * 1.5)
            self.rect.y  += int(self.velocity)
            self.angle    = self.MAX_DOWN_ANGLE
            return

        # Gravity
        self.velocity = min(self.velocity + GRAVITY, MAX_FALL_SPEED)
        self.rect.y  += int(self.velocity)

        # Clamp to top of screen
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0

        # Rotation: map velocity range  angle range
        t = (self.velocity - JUMP_STRENGTH) / (MAX_FALL_SPEED - JUMP_STRENGTH)
        t = max(0.0, min(1.0, t))
        self.angle = self.MAX_UP_ANGLE + t * (self.MAX_DOWN_ANGLE - self.MAX_UP_ANGLE)

    def draw(self, surface):
        """Rotate around centre and blit."""
        rotated = pygame.transform.rotate(self.image_orig, self.angle)
        rotated_rect = rotated.get_rect(center=self.rect.center)
        surface.blit(rotated, rotated_rect)

    def get_mask(self):
        """Return a fresh mask matching current rotation (for collision)."""
        rotated = pygame.transform.rotate(self.image_orig, self.angle)
        return pygame.mask.from_surface(rotated), rotated.get_rect(center=self.rect.center)

    def hit_ground(self):
        ground_y = WINDOW_HEIGHT - GROUND_HEIGHT
        return self.rect.bottom >= ground_y

    def reset(self):
        self.rect.center = (BIRD_START_X, BIRD_START_Y)
        self.velocity     = 0
        self.angle        = 0
        self.alive        = True
