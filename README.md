# Pokémon Chess

A local two-player / four-bot Pokémon-themed chess game built with Python and Tkinter.

This is the **latest version** with the simple grey interface, muted green buttons, larger Gen 5-style pixel Pokémon, and white circles behind the Pokémon portraits. The original chessboard remains the same.

## Run it in VS Code on macOS

1. Click **Code → Download ZIP** and extract the folder.
2. Open the extracted **Pokemon-Chess-main** folder in VS Code using **File → Open Folder**.
3. Open **Run and Debug** and choose **Play Pokemon Chess**.
4. Click the green Play button.

The repository is configured to use `/opt/homebrew/bin/python3.14`, which must have Tkinter installed.

Alternatively, double-click **Play Pokemon Chess.command** (macOS security settings may require opening it via right-click → Open).

The first run reconstructs `pokemon_chess_app.py` from `game_source.zlib.b64` and launches it automatically. You do not need to manually unpack or combine any code. The generated Python file is kept alongside the launcher.

## Features

- 176 Pokémon to choose from
- Two independent teams and a Randomize Team button
- Friend mode or bots labeled 500, 750, 1300 and 1500 Elo
- Standard chess rules with the custom evolved movement abilities
- Pokémon evolution progression based on two captures
- Normal sprites for White and shiny sprites for Black
- Larger Gen 5-style pixel portraits with white circular backing
- Clear chess-piece shapes and letters
- Undo, restart, move history, fullscreen and board flipping in friend mode

## Sprites

The game checks its image folders and downloads missing Pokémon and chess-piece images when launched with internet access. **The third-party PNG artwork is not included in this GitHub repository.** Some sprites may be unavailable from the image sources; the game provides visual fallbacks and a retry option.

## Tests

In VS Code, use the integrated terminal to run:

```bash
/opt/homebrew/bin/python3.14 pokemon_chess.py --test
```

The game's built-in tests pass in the development environment, but actual sprite downloads depend on the network and sources.
