# 
#  main.py    Entry point & game loop
# 

import pygame
import sys
import os
import math
import asyncio
from config import *
from bird   import Bird
from pipe   import Pipe
from ground import Ground
from audio  import AudioManager

#  Game States 
MENU      = "menu"
PLAYING   = "playing"
GAME_OVER = "game_over"

#  Background (loaded once, cached) 
_bg_surface = None

def get_background():
    global _bg_surface
    if _bg_surface is None:
        if os.path.exists(IMG_BG):
            raw = pygame.image.load(IMG_BG).convert()
            _bg_surface = pygame.transform.scale(raw, (WINDOW_WIDTH, WINDOW_HEIGHT))
        else:
            _bg_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            _bg_surface.fill(SKY)
    return _bg_surface


#  Font loader (retro TTF  system Arial fallback) 
_font_cache = {}

def get_font(size, bold=False):
    key = (size, bold)
    if key not in _font_cache:
        ttf_candidates = [
            os.path.join(FONT_DIR, "PressStart2P.ttf"),
            os.path.join(FONT_DIR, "04B_19.ttf"),
            os.path.join(FONT_DIR, "pixel.ttf"),
        ]
        loaded = None
        for path in ttf_candidates:
            if os.path.exists(path):
                try:
                    loaded = pygame.font.Font(path, size)
                    break
                except Exception:
                    pass
        if loaded is None:
            loaded = pygame.font.SysFont("Arial", size, bold=bold)
        _font_cache[key] = loaded
    return _font_cache[key]


def draw_text(surface, text, size, color, center, bold=False, alpha=255):
    font = get_font(size, bold)
    img  = font.render(text, True, color)
    if alpha < 255:
        img.set_alpha(alpha)
    rect = img.get_rect(center=center)
    surface.blit(img, rect)
    return rect


#  HUD score (top of screen while playing) 
def draw_hud(surface, score, high_score):
    # Drop shadow
    draw_text(surface, str(score), 40, BLACK,
              (WINDOW_WIDTH // 2 + 2, 62), bold=True)
    draw_text(surface, str(score), 40, WHITE,
              (WINDOW_WIDTH // 2,     60), bold=True)
    draw_text(surface, f"BEST  {high_score}", 18, YELLOW,
              (WINDOW_WIDTH // 2, 100))


#  Menu screen 
def draw_menu(surface):
    # Title banner with shadow
    draw_text(surface, "FLAPPY ELON", 30, BLACK,
              (WINDOW_WIDTH // 2 + 2, 152), bold=True)
    draw_text(surface, "FLAPPY ELON", 30, YELLOW,
              (WINDOW_WIDTH // 2,     150), bold=True)

    draw_text(surface, "SPACE / TAP to Start", 14, WHITE,
              (WINDOW_WIDTH // 2, 560))


#  Game Over modal (pixel-board card) 
def draw_game_over_modal(surface, score, high_score, blink_visible):
    #  full-screen dim 
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    surface.blit(overlay, (0, 0))

    cx = WINDOW_WIDTH  // 2
    cy = WINDOW_HEIGHT // 2

    #  "GAME OVER" banner 
    banner_w, banner_h = 300, 52
    banner_rect = pygame.Rect(0, 0, banner_w, banner_h)
    banner_rect.center = (cx, cy - 118)

    # Banner background  red gradient via two rects
    pygame.draw.rect(surface, (180, 20, 20), banner_rect, border_radius=6)
    pygame.draw.rect(surface, (220, 50, 50),
                     pygame.Rect(banner_rect.x, banner_rect.y,
                                 banner_w, banner_h // 2), border_radius=6)
    pygame.draw.rect(surface, WHITE, banner_rect, 3, border_radius=6)

    draw_text(surface, "GAME OVER", 20, WHITE, banner_rect.center, bold=True)

    #  score card 
    card_w, card_h = 300, 160
    card_rect = pygame.Rect(0, 0, card_w, card_h)
    card_rect.center = (cx, cy + 10)

    # Card body  parchment white
    pygame.draw.rect(surface, (240, 235, 210), card_rect, border_radius=8)
    # Pixel-style black border (double line for retro look)
    pygame.draw.rect(surface, BLACK, card_rect, 4, border_radius=8)
    pygame.draw.rect(surface, (80, 60, 20),
                     card_rect.inflate(-8, -8), 2, border_radius=6)

    # Divider
    mid_y = card_rect.centery
    pygame.draw.line(surface, (180, 170, 140),
                     (card_rect.x + 16, mid_y),
                     (card_rect.right - 16, mid_y), 2)

    # Score row
    draw_text(surface, "SCORE", 13, (80, 60, 20),
              (cx - 60, card_rect.y + 38))
    draw_text(surface, str(score), 22, BLACK,
              (cx + 70, card_rect.y + 38), bold=True)

    # Medal icon (gold circle for score  10, silver otherwise)
    medal_color = (255, 200, 0) if score >= 10 else (180, 180, 180)
    medal_x = card_rect.x + 30
    medal_y = card_rect.y + 38
    pygame.draw.circle(surface, medal_color, (medal_x, medal_y), 16)
    pygame.draw.circle(surface, BLACK,       (medal_x, medal_y), 16, 2)
    draw_text(surface, "" if score >= 10 else "", 14, WHITE, (medal_x, medal_y))

    # Best row
    draw_text(surface, "BEST",  13, (80, 60, 20),
              (cx - 60, card_rect.y + 118))
    draw_text(surface, str(high_score), 22, (180, 130, 0),
              (cx + 70, card_rect.y + 118), bold=True)

    # Best medal
    pygame.draw.circle(surface, (255, 215, 0), (medal_x, card_rect.y + 118), 16)
    pygame.draw.circle(surface, BLACK,         (medal_x, card_rect.y + 118), 16, 2)
    draw_text(surface, "", 14, WHITE, (medal_x, card_rect.y + 118))

    #  blinking restart prompt 
    if blink_visible:
        draw_text(surface, "SPACE / TAP to Restart", 13, WHITE,
                  (cx, cy + 135))


#  Speed helper 
def current_speed(score):
    bumps = score // SPEED_INCREMENT_EVERY
    return min(PIPE_SPEED + bumps * SPEED_INCREMENT, MAX_SPEED)


#  Main 
async def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)   # must be before pygame.init()
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock  = pygame.time.Clock()

    Pipe.load_assets()

    bird   = Bird()
    ground = Ground()
    audio  = AudioManager()

    state      = MENU
    pipes      = []
    score      = 0
    high_score = 0

    # Blink timer for "Press SPACE" prompt
    blink_visible  = True
    blink_timer_ms = 0
    BLINK_INTERVAL = 550   # ms

    last_pipe_spawn_time = 0

    def reset_game():
        nonlocal pipes, score, last_pipe_spawn_time
        bird.reset()
        pipes  = []
        score  = 0
        last_pipe_spawn_time = pygame.time.get_ticks()
        audio.play_bgm()

    while True:
        dt = clock.tick(FPS)

        #  Blink counter 
        if state == GAME_OVER:
            blink_timer_ms += dt
            if blink_timer_ms >= BLINK_INTERVAL:
                blink_visible  = not blink_visible
                blink_timer_ms = 0
        else:
            blink_visible  = True
            blink_timer_ms = 0

        #  Events 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()

            flap_pressed = (
                (event.type == pygame.KEYDOWN      and event.key == pygame.K_SPACE) or
                (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)
            )

            if flap_pressed:
                if state == MENU:
                    audio.play("swoosh")
                    state = PLAYING
                    reset_game()
                elif state == PLAYING:
                    bird.flap()
                    audio.play("flap")
                elif state == GAME_OVER:
                    state = PLAYING
                    reset_game()

        #  Update 
        if state == PLAYING:
            current_time = pygame.time.get_ticks()
            if current_time - last_pipe_spawn_time > PIPE_SPAWN_MS:
                pipes.append(Pipe(speed=current_speed(score)))
                last_pipe_spawn_time = current_time

            spd = current_speed(score)
            bird.update()
            ground.update(speed=spd)

            for pipe in pipes:
                pipe.speed = spd
                pipe.update()

                if pipe.bird_passed(bird):
                    score += POINTS_PER_PIPE
                    audio.play("score")

                if pipe.collides_with(bird):
                    bird.alive = False
                    audio.play("hit")
                    audio.stop_bgm()
                    state = GAME_OVER
                    high_score = max(high_score, score)

            pipes = [p for p in pipes if not p.is_off_screen()]

            if bird.hit_ground():
                bird.alive = False
                audio.play("die")
                audio.stop_bgm()
                state = GAME_OVER
                high_score = max(high_score, score)

        elif state == MENU:
            ground.update()
            bird.rect.y = BIRD_START_Y + int(10 * abs(
                math.sin(pygame.time.get_ticks() * 0.003)
            ))

        #  Draw 
        screen.blit(get_background(), (0, 0))

        for pipe in pipes:
            pipe.draw(screen)

        ground.draw(screen)
        bird.draw(screen)

        if state == MENU:
            draw_menu(screen)

        if state == PLAYING:
            draw_hud(screen, score, high_score)

        if state == GAME_OVER:
            draw_hud(screen, score, high_score)
            draw_game_over_modal(screen, score, high_score, blink_visible)

        pygame.display.flip()
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
