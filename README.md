# Flappy Elon 🐦

Your custom Flappy Bird built with Python + Pygame.

## Project Structure

```
FlappyBird/
├── main.py          ← Entry point & game loop
├── bird.py          ← Bird physics & sprite
├── pipe.py          ← Pipe pair logic & collision
├── ground.py        ← Scrolling ground
├── audio.py         ← BGM & SFX manager
├── config.py        ← All tunable constants
├── requirements.txt
└── assets/
    ├── images/
    │   ├── elon_bird.png   ✅ (your file)
    │   ├── pipe.png        ✅ (your file)
    │   ├── ground.png      ✅ (your file)
    │   └── background.png  ← drop yours here (optional)
    ├── audio/
    │   ├── bgm.ogg         ← your background music
    │   ├── flap.wav        ← wing flap sound
    │   ├── score.wav       ← point scored sound
    │   └── hit.wav         ← collision sound
    └── fonts/              ← drop custom fonts here (optional)
```

## Setup

```bash
pip install -r requirements.txt
python main.py
```

## Controls

| Key / Action     | Effect       |
|------------------|--------------|
| Space / Click    | Flap / Start |
| Escape           | Quit         |

## Adding your assets

- **Background**: Save as `assets/images/background.png` — game auto-detects it.
- **BGM**: Save as `assets/audio/bgm.ogg` (use `.ogg` or `.wav`, NOT `.mp3`).
- **SFX**: Drop `flap.wav`, `score.wav`, `hit.wav` into `assets/audio/`.
- All missing audio files are silently skipped — game runs fine without them.

## Tuning the game feel

Everything is in `config.py`:

| Constant        | What it controls              |
|-----------------|-------------------------------|
| `GRAVITY`       | How fast the bird falls       |
| `JUMP_STRENGTH` | How high one flap takes you   |
| `PIPE_GAP`      | Gap size between pipes        |
| `PIPE_SPEED`    | Base scroll speed             |
| `PIPE_SPAWN_MS` | Time between pipe spawns (ms) |
| `SPEED_INCREMENT` | How much harder it gets     |
