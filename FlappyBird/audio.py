# 
#  audio.py    Sound & music manager
# 

import pygame
import os
from config import *


class AudioManager:
    """
    Wraps pygame.mixer.
    Gracefully skips any file that doesn't exist yet so the game
    runs fine even before you've added audio assets.
    """

    def __init__(self):
        pygame.mixer.init()
        self._sfx  = {}
        self._load_sfx("flap",  SFX_FLAP)
        self._load_sfx("score", SFX_SCORE)
        self._load_sfx("hit",   SFX_HIT)
        self._bgm_loaded = False
        self._load_bgm()

    #  Private helpers 

    def _load_sfx(self, name, path):
        if os.path.exists(path):
            try:
                self._sfx[name] = pygame.mixer.Sound(path)
            except Exception as e:
                print(f"[Audio] Could not load SFX '{name}': {e}")

    def _load_bgm(self):
        if os.path.exists(BGM_TRACK):
            try:
                pygame.mixer.music.load(BGM_TRACK)
                self._bgm_loaded = True
            except Exception as e:
                print(f"[Audio] Could not load BGM: {e}")

    #  Public API 

    def play_bgm(self, loops=-1):
        if self._bgm_loaded:
            pygame.mixer.music.play(loops)

    def stop_bgm(self):
        pygame.mixer.music.stop()

    def play(self, name):
        sfx = self._sfx.get(name)
        if sfx:
            sfx.play()
