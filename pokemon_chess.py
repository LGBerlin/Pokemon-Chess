from pathlib import Path
import base64
import hashlib
import runpy
import zlib

folder = Path(__file__).resolve().parent
archive = folder / 'game_source.zlib.b64'
game = folder / 'pokemon_chess_app.py'

try:
    source = zlib.decompress(base64.b64decode(archive.read_text(encoding='ascii')))
except (OSError, ValueError, zlib.error) as error:
    raise SystemExit('Unable to load game data: ' + str(error))

if not game.exists() or hashlib.sha256(game.read_bytes()).digest() != hashlib.sha256(source).digest():
    game.write_bytes(source)

runpy.run_path(str(game), run_name='__main__')
