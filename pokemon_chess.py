from __future__ import annotations
import copy
import math
import random
import os
import sys
import json
import threading
import time
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

WIDTH, HEIGHT = 1320, 900
FPS = 60
BOT_DIFFICULTIES = (500, 750, 1300, 1500)
BOT_COLOR = 'black'
PIXEL_ART_SPRITES = True
BOARD_SIZE = 792
CELL = BOARD_SIZE // 8
BOARD_X, BOARD_Y = 28, 60
PANEL_X = BOARD_X + BOARD_SIZE + 28
BG = (39, 37, 34)
PANEL = (49, 46, 43)
LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
TEXT = (236, 234, 229)
MUTED = (171, 168, 162)
ACCENT = (129, 182, 76)
SELECTED = (245, 246, 130, 120)
LAST_MOVE = (245, 246, 130, 78)
CHECK = (214, 86, 73, 150)
PIECE_WHITE = (250, 248, 243)
PIECE_BLACK = (58, 61, 66)
SPRITE_ROOT = Path(__file__).resolve().parent / 'pokemon_chess_sprites'
CHESS_PIECE_ROOT = Path(__file__).resolve().parent / 'chess_piece_sprites' / 'neo_verified_v2'
                                                                 
CHESS_PIECE_URLS = (
    'https://images.chesscomfiles.com/chess-themes/pieces/neo/300/{name}.png',
    'https://images.chesscomfiles.com/chess-themes/pieces/neo/150/{name}.png',
    'https://www.chess.com/chess-themes/pieces/neo/300/{name}.png',
)
CHESS_PIECE_SIZE = 91
POKEMON_BOARD_SIZE = 57
POKEMON_CORNER_PADDING = 4

AUTO_DOWNLOAD_SPRITES = True                                                          
SPRITE_NETWORK_TIMEOUT = 7                          
SPRITE_WORKERS = 16                                                               
SPRITE_SOURCE = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon'
POKEAPI_INDEX = 'https://pokeapi.co/api/v2/pokemon?limit=1600'
SPRITE_ALIASES = {'lycanroc': 'lycanroc-midday', 'toxtricity': 'toxtricity-amped',
                  'oinkologne': 'oinkologne-male'}

SELECTION_PER_ROLE = {'pawn': 8, 'rook': 2, 'bishop': 2, 'knight': 2,
                      'queen': 1, 'king': 1}
ROLE_SYMBOL = {'pawn': 'P', 'rook': 'R', 'bishop': 'B', 'knight': 'N',
               'queen': 'Q', 'king': 'K'}
ROLE_GLYPHS = {'pawn': '♟', 'rook': '♜', 'bishop': '♝', 'knight': '♞',
               'queen': '♛', 'king': '♚'}
BACK_ROW = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']

                                                              
ROSTER = {
    'pawn': ['Caterpie', 'Weedle', 'Pidgey', 'Rattata', 'Zubat', 'Oddish',
             'Venonat', 'Psyduck', 'Poliwag', 'Bellsprout', 'Tentacool',
             'Grimer', 'Cubone', 'Koffing', 'Staryu', 'Igglybuff', 'Hoppip',
             'Wooper', 'Zigzagoon', 'Lotad', 'Seedot', 'Shroomish',
             'Meditite', 'Cherubi', 'Drifloon', 'Joltik', 'Grubbin',
             'Nickit', 'Toxel', 'Sizzlipede', 'Lechonk', 'Tarountula'],
    'rook': ['Sandshrew', 'Diglett', 'Geodude', 'Onix', 'Omanyte',
             'Larvitar', 'Aron', 'Roggenrola', 'Dwebble', 'Golett',
             'Pawniard', 'Meltan', 'Rolycoly', 'Nacli',
             'Rhyhorn', 'Phanpy', 'Nosepass', 'Shieldon', 'Cranidos', 'Bronzor', 'Hippopotas', 'Swinub', 'Ferroseed', 'Klink', 'Tirtouga', 'Bergmite', 'Mudbray', 'Sandygast', 'Cufant', 'Stonjourner', 'Orthworm', 'Varoom'],
    'bishop': ['Abra', 'Gastly', 'Misdreavus', 'Ralts', 'Duskull',
               'Wynaut', 'Solosis', 'Elgyem', 'Litwick', 'Phantump',
               'Impidimp', 'Snom', 'Dreepy', 'Tinkatink',
             'Natu', 'Hoothoot', 'Smoochum', 'Spoink', 'Chingling', 'Munna', 'Gothita', 'Espurr', 'Inkay', 'Hatenna', 'Sinistea', 'Milcery', 'Flittle', 'Greavard', 'Shuppet', 'Yamask', 'Honedge', 'Morelull'],
    'knight': ['Ponyta', 'Poochyena', 'Taillow', 'Electrike', 'Shinx',
               'Riolu', 'Blitzle', 'Zorua', 'Axew', 'Froakie',
               'Fletchling', 'Rockruff', 'Scorbunny', 'Sobble',
             'Growlithe', 'Vulpix', 'Houndour', 'Mareep', 'Numel', 'Buneary', 'Buizel', 'Deerling', 'Lillipup', 'Sandile', 'Mienfoo', 'Goomy', 'Noibat', 'Litten', 'Yamper', 'Sprigatito', 'Fuecoco', 'Quaxly'],
    'queen': ['Dratini', 'Togepi', 'Beldum', 'Gible', 'Deino', 'Popplio',
              'Jangmo-o', 'Applin',
             'Bagon', 'Trapinch', 'Feebas', 'Swablu', 'Snorunt', 'Budew', 'Happiny', 'Porygon', 'Magnemite', 'Larvesta', 'Skrelp', 'Cutiefly', 'Fomantis', 'Salandit', 'Bounsweet', 'Duraludon'],
    'king': ['Bulbasaur', 'Charmander', 'Squirtle', 'Treecko',
             'Torchic', 'Mudkip', 'Rowlet', 'Grookey',
             'Chikorita', 'Cyndaquil', 'Totodile', 'Turtwig', 'Chimchar', 'Piplup', 'Snivy', 'Tepig', 'Oshawott', 'Chespin', 'Fennekin', 'Pikachu', 'Eevee', 'Tynamo', 'Minccino', 'Pawmi'],
}

                                                                                   
EVOLUTIONS = dict(zip(
    [s for role, count in (('pawn',32), ('rook',14), ('bishop',14), ('knight',14), ('queen',8), ('king',8))
     for s in ROSTER[role][:count]],
    [
                                     
      'Butterfree', 'Beedrill', 'Pidgeot', 'Raticate', 'Crobat', 'Vileplume',
      'Venomoth', 'Golduck', 'Poliwrath', 'Victreebel', 'Tentacruel',
      'Muk', 'Marowak', 'Weezing', 'Starmie', 'Wigglytuff', 'Jumpluff',
      'Quagsire', 'Obstagoon', 'Ludicolo', 'Shiftry', 'Breloom',
      'Medicham', 'Cherrim', 'Drifblim', 'Galvantula', 'Vikavolt',
      'Thievul', 'Toxtricity', 'Centiskorch', 'Oinkologne', 'Spidops',
                                     
      'Sandslash', 'Dugtrio', 'Golem', 'Steelix', 'Omastar',
      'Tyranitar', 'Aggron', 'Gigalith', 'Crustle', 'Golurk',
      'Kingambit', 'Melmetal', 'Coalossal', 'Garganacl',
                                       
      'Alakazam', 'Gengar', 'Mismagius', 'Gardevoir', 'Dusknoir',
      'Wobbuffet', 'Reuniclus', 'Beheeyem', 'Chandelure', 'Trevenant',
      'Grimmsnarl', 'Frosmoth', 'Dragapult', 'Tinkaton',
                                       
      'Rapidash', 'Mightyena', 'Swellow', 'Manectric', 'Luxray',
      'Lucario', 'Zebstrika', 'Zoroark', 'Haxorus', 'Greninja',
      'Talonflame', 'Lycanroc', 'Cinderace', 'Inteleon',
                                      
      'Dragonite', 'Togekiss', 'Metagross', 'Garchomp', 'Hydreigon',
      'Primarina', 'Kommo-o', 'Flapple',
                                     
      'Venusaur', 'Charizard', 'Blastoise', 'Sceptile',
      'Blaziken', 'Swampert', 'Decidueye', 'Rillaboom',
    ]
))

                                                          
              
EVOLUTIONS['Rhyhorn'] = 'Rhyperior'
EVOLUTIONS['Phanpy'] = 'Donphan'
EVOLUTIONS['Nosepass'] = 'Probopass'
EVOLUTIONS['Shieldon'] = 'Bastiodon'
EVOLUTIONS['Cranidos'] = 'Rampardos'
EVOLUTIONS['Bronzor'] = 'Bronzong'
EVOLUTIONS['Hippopotas'] = 'Hippowdon'
EVOLUTIONS['Swinub'] = 'Mamoswine'
EVOLUTIONS['Ferroseed'] = 'Ferrothorn'
EVOLUTIONS['Klink'] = 'Klinklang'
EVOLUTIONS['Tirtouga'] = 'Carracosta'
EVOLUTIONS['Bergmite'] = 'Avalugg'
EVOLUTIONS['Mudbray'] = 'Mudsdale'
EVOLUTIONS['Sandygast'] = 'Palossand'
EVOLUTIONS['Cufant'] = 'Copperajah'
EVOLUTIONS['Stonjourner'] = 'Stonjourner'
EVOLUTIONS['Orthworm'] = 'Orthworm'
EVOLUTIONS['Varoom'] = 'Revavroom'
                
EVOLUTIONS['Natu'] = 'Xatu'
EVOLUTIONS['Hoothoot'] = 'Noctowl'
EVOLUTIONS['Smoochum'] = 'Jynx'
EVOLUTIONS['Spoink'] = 'Grumpig'
EVOLUTIONS['Chingling'] = 'Chimecho'
EVOLUTIONS['Munna'] = 'Musharna'
EVOLUTIONS['Gothita'] = 'Gothitelle'
EVOLUTIONS['Espurr'] = 'Meowstic'
EVOLUTIONS['Inkay'] = 'Malamar'
EVOLUTIONS['Hatenna'] = 'Hatterene'
EVOLUTIONS['Sinistea'] = 'Polteageist'
EVOLUTIONS['Milcery'] = 'Alcremie'
EVOLUTIONS['Flittle'] = 'Espathra'
EVOLUTIONS['Greavard'] = 'Houndstone'
EVOLUTIONS['Shuppet'] = 'Banette'
EVOLUTIONS['Yamask'] = 'Cofagrigus'
EVOLUTIONS['Honedge'] = 'Aegislash'
EVOLUTIONS['Morelull'] = 'Shiinotic'
                
EVOLUTIONS['Growlithe'] = 'Arcanine'
EVOLUTIONS['Vulpix'] = 'Ninetales'
EVOLUTIONS['Houndour'] = 'Houndoom'
EVOLUTIONS['Mareep'] = 'Ampharos'
EVOLUTIONS['Numel'] = 'Camerupt'
EVOLUTIONS['Buneary'] = 'Lopunny'
EVOLUTIONS['Buizel'] = 'Floatzel'
EVOLUTIONS['Deerling'] = 'Sawsbuck'
EVOLUTIONS['Lillipup'] = 'Stoutland'
EVOLUTIONS['Sandile'] = 'Krookodile'
EVOLUTIONS['Mienfoo'] = 'Mienshao'
EVOLUTIONS['Goomy'] = 'Goodra'
EVOLUTIONS['Noibat'] = 'Noivern'
EVOLUTIONS['Litten'] = 'Incineroar'
EVOLUTIONS['Yamper'] = 'Boltund'
EVOLUTIONS['Sprigatito'] = 'Meowscarada'
EVOLUTIONS['Fuecoco'] = 'Skeledirge'
EVOLUTIONS['Quaxly'] = 'Quaquaval'
               
EVOLUTIONS['Bagon'] = 'Salamence'
EVOLUTIONS['Trapinch'] = 'Flygon'
EVOLUTIONS['Feebas'] = 'Milotic'
EVOLUTIONS['Swablu'] = 'Altaria'
EVOLUTIONS['Snorunt'] = 'Froslass'
EVOLUTIONS['Budew'] = 'Roserade'
EVOLUTIONS['Happiny'] = 'Blissey'
EVOLUTIONS['Porygon'] = 'Porygon-Z'
EVOLUTIONS['Magnemite'] = 'Magnezone'
EVOLUTIONS['Larvesta'] = 'Volcarona'
EVOLUTIONS['Skrelp'] = 'Dragalge'
EVOLUTIONS['Cutiefly'] = 'Ribombee'
EVOLUTIONS['Fomantis'] = 'Lurantis'
EVOLUTIONS['Salandit'] = 'Salazzle'
EVOLUTIONS['Bounsweet'] = 'Tsareena'
EVOLUTIONS['Duraludon'] = 'Archaludon'
              
EVOLUTIONS['Chikorita'] = 'Meganium'
EVOLUTIONS['Cyndaquil'] = 'Typhlosion'
EVOLUTIONS['Totodile'] = 'Feraligatr'
EVOLUTIONS['Turtwig'] = 'Torterra'
EVOLUTIONS['Chimchar'] = 'Infernape'
EVOLUTIONS['Piplup'] = 'Empoleon'
EVOLUTIONS['Snivy'] = 'Serperior'
EVOLUTIONS['Tepig'] = 'Emboar'
EVOLUTIONS['Oshawott'] = 'Samurott'
EVOLUTIONS['Chespin'] = 'Chesnaught'
EVOLUTIONS['Fennekin'] = 'Delphox'
EVOLUTIONS['Pikachu'] = 'Raichu'
EVOLUTIONS['Eevee'] = 'Sylveon'
EVOLUTIONS['Tynamo'] = 'Eelektross'
EVOLUTIONS['Minccino'] = 'Cinccino'
EVOLUTIONS['Pawmi'] = 'Pawmot'

                                                            
                                                                     
ABILITY_UNLOCK_CAPTURES = 2
MIDDLE_FORM_CAPTURES = 1
FINAL_FORM_CAPTURES = 2

                                                                        
                                                                              
MIDDLE_EVOLUTIONS = {
    'Caterpie': 'Metapod', 'Weedle': 'Kakuna', 'Pidgey': 'Pidgeotto',
    'Zubat': 'Golbat', 'Oddish': 'Gloom', 'Poliwag': 'Poliwhirl',
    'Bellsprout': 'Weepinbell', 'Igglybuff': 'Jigglypuff',
    'Hoppip': 'Skiploom', 'Zigzagoon': 'Linoone',
    'Lotad': 'Lombre', 'Seedot': 'Nuzleaf', 'Grubbin': 'Charjabug',
    'Larvitar': 'Pupitar', 'Aron': 'Lairon', 'Roggenrola': 'Boldore',
    'Pawniard': 'Bisharp', 'Rolycoly': 'Carkol', 'Nacli': 'Naclstack',
    'Rhyhorn': 'Rhydon', 'Swinub': 'Piloswine', 'Klink': 'Klang',
    'Abra': 'Kadabra', 'Gastly': 'Haunter', 'Ralts': 'Kirlia',
    'Duskull': 'Dusclops', 'Solosis': 'Duosion', 'Litwick': 'Lampent',
    'Impidimp': 'Morgrem', 'Dreepy': 'Drakloak', 'Tinkatink': 'Tinkatuff',
    'Gothita': 'Gothorita', 'Hatenna': 'Hattrem', 'Honedge': 'Doublade',
    'Shinx': 'Luxio', 'Axew': 'Fraxure', 'Froakie': 'Frogadier',
    'Fletchling': 'Fletchinder', 'Scorbunny': 'Raboot',
    'Sobble': 'Drizzile', 'Mareep': 'Flaaffy', 'Lillipup': 'Herdier',
    'Sandile': 'Krokorok', 'Goomy': 'Sliggoo', 'Litten': 'Torracat',
    'Sprigatito': 'Floragato', 'Fuecoco': 'Crocalor',
    'Quaxly': 'Quaxwell', 'Dratini': 'Dragonair', 'Togepi': 'Togetic',
    'Beldum': 'Metang', 'Gible': 'Gabite', 'Deino': 'Zweilous',
    'Popplio': 'Brionne', 'Jangmo-o': 'Hakamo-o', 'Bagon': 'Shelgon',
    'Trapinch': 'Vibrava', 'Budew': 'Roselia', 'Happiny': 'Chansey',
    'Porygon': 'Porygon2', 'Magnemite': 'Magneton',
    'Bounsweet': 'Steenee', 'Bulbasaur': 'Ivysaur',
    'Charmander': 'Charmeleon', 'Squirtle': 'Wartortle',
    'Treecko': 'Grovyle', 'Torchic': 'Combusken',
    'Mudkip': 'Marshtomp', 'Rowlet': 'Dartrix', 'Grookey': 'Thwackey',
    'Chikorita': 'Bayleef', 'Cyndaquil': 'Quilava',
    'Totodile': 'Croconaw', 'Turtwig': 'Grotle',
    'Chimchar': 'Monferno', 'Piplup': 'Prinplup',
    'Snivy': 'Servine', 'Tepig': 'Pignite', 'Oshawott': 'Dewott',
    'Chespin': 'Quilladin', 'Fennekin': 'Braixen',
    'Tynamo': 'Eelektrik', 'Pawmi': 'Pawmo',
}

                                                    
ABILITIES = {
    'pawn': {'extra_empty_steps': [(1, 0), (-1, 0), (0, -1)],
             'allow_normal_two_step': True},
    'bishop': {'jump_enemy_pieces': True, 'friendly_blocks': True},
    'knight': {'extra_jumps': [(3, 1), (1, 3)], 'extra_forward': 1},
    'rook': {'allow_king_swap': True},
    'queen': {'add_knight_jumps': True},
    'king': {'max_distance': 2, 'require_safe_intermediate': True},
}
                                                                             
                                                                             
                                                                          
                                                            
                                                                               
                                                                  

DIRS_DIAGONAL = [(-1,-1),(-1,1),(1,-1),(1,1)]
DIRS_ORTHOGONAL = [(-1,0),(1,0),(0,-1),(0,1)]
DIRS_ALL = DIRS_DIAGONAL + DIRS_ORTHOGONAL
KNIGHT_OFFSETS = [(dx*sx,dy*sy) for dx,dy in ((1,2),(2,1))
                  for sx in (-1,1) for sy in (-1,1)]


def slug(name: str) -> str:
    return name.lower().replace(' ', '-').replace("'", '').replace('.', '')


def in_board(x, y):
    return 0 <= x < 8 and 0 <= y < 8


def algebraic(square):
    x,y = square
    return chr(97+x) + str(8-y)


@dataclass
class Piece:
    role: str
    color: str
    species: str
    evolved: bool = False
    moved: bool = False
    captures: int = 0

    @property
    def display_species(self):
        if self.species in MIDDLE_EVOLUTIONS:
            if self.captures >= FINAL_FORM_CAPTURES:
                return EVOLUTIONS.get(self.species, self.species)
            if self.captures >= MIDDLE_FORM_CAPTURES:
                return MIDDLE_EVOLUTIONS[self.species]
            return self.species
        if self.captures >= FINAL_FORM_CAPTURES:
            return EVOLUTIONS.get(self.species, self.species)
        return self.species


@dataclass(frozen=True)
class Move:
    src: tuple[int,int]
    dst: tuple[int,int]
    kind: str = 'normal'                                               
    promote: str = ''


class TeamDraft:





    def __init__(self):
        self.teams = {c: {r: [] for r in ROSTER} for c in ('white', 'black')}
        self.turn = 'white'

    def count(self, color):
        return sum(len(group) for group in self.teams[color].values())

    def complete(self, color):
        return all(len(self.teams[color][role]) == required
                   for role, required in SELECTION_PER_ROLE.items())

    def _advance_if_complete(self):
                                                                      
        if self.turn == 'white' and self.complete('white'):
            self.turn = 'black'

    def select(self, role, name):
        color = self.turn
        choices = self.teams[color]
        if self.complete(color) or role not in ROSTER or name not in ROSTER[role]:
            return False
        if any(name in group for group in choices.values()):
            return False
        if len(choices[role]) >= SELECTION_PER_ROLE[role]:
            return False
        choices[role].append(name)
        self._advance_if_complete()
        return True

    def randomize(self, rng=None):






        color = self.turn
        if self.complete(color):
            return False
        rng = rng if rng is not None else random.SystemRandom()
        used = {species for group in self.teams[color].values() for species in group}
        additions = {}
        for role, required in SELECTION_PER_ROLE.items():
            needed = required - len(self.teams[color][role])
            available = [name for name in ROSTER[role] if name not in used]
            if needed < 0 or needed > len(available):
                return False
            additions[role] = rng.sample(available, needed)
            used.update(additions[role])
        for role, species in additions.items():
            self.teams[color][role].extend(species)
        self._advance_if_complete()
        return True

    @property
    def done(self):
        return all(self.complete(color) for color in ('white', 'black'))


class ChessGame:
    def __init__(self, teams):
        self.teams = copy.deepcopy(teams)
        self.reset()

    def reset(self):
        self.board = {}
        for color in ('white','black'):
            y0, yp = (7,6) if color == 'white' else (0,1)
            role_index = Counter()
            for x, role in enumerate(BACK_ROW):
                species = self.teams[color][role][role_index[role]]
                role_index[role] += 1
                self.board[(x,y0)] = Piece(role,color,species)
            for x, species in enumerate(self.teams[color]['pawn']):
                self.board[(x,yp)] = Piece('pawn',color,species)
        self.turn = 'white'
        self.en_passant = None                                    
        self.halfmove = 0
        self.fullmove = 1
        self.history = []
        self.move_names = []
        self.last_move = None
        self.result = None
        self.position_counts = Counter()
        self.position_counts[self.position_key()] += 1
        self.refresh_result()

    @staticmethod
    def enemy(color):
        return 'black' if color == 'white' else 'white'

    def get(self, square):
        return self.board.get(square)

    def king_square(self, color):
        for sq, p in self.board.items():
            if p.role == 'king' and p.color == color:
                return sq
        return None

    def position_key(self):
                                                                              
                                                                    
        pieces = tuple(sorted((x,y,p.color,p.role,p.species,p.evolved,p.moved,p.captures)
                              for (x,y),p in self.board.items()))
        return (pieces, self.turn, self.en_passant)

    def snapshots(self):
        return (copy.deepcopy(self.board),self.turn,self.en_passant,
                self.halfmove,self.fullmove,self.last_move,
                copy.deepcopy(self.position_counts),self.result,
                self.move_names[:])

    def restore(self, state):
        (self.board,self.turn,self.en_passant,self.halfmove,self.fullmove,
         self.last_move,self.position_counts,self.result,self.move_names) = state

    def undo(self):
        if not self.history:
            return False
        self.restore(self.history.pop())
        return True

    def trace(self, src, dirs, color, jump_enemy=False):

        out = []
        for dx,dy in dirs:
            x,y = src
            while True:
                x += dx; y += dy
                if not in_board(x,y): break
                target = self.get((x,y))
                if target and target.color == color: break
                out.append((x,y))
                if target and not jump_enemy: break
        return out

    def targets(self, src, attacks_only=False):




        p = self.get(src)
        if p is None: return []
        x,y = src
        color = p.color
        direction = -1 if color == 'white' else 1
        out = []
        if p.role == 'pawn':
            for dx in (-1,1):
                dst = (x+dx,y+direction)
                if not in_board(*dst): continue
                occupant = self.get(dst)
                if attacks_only:
                    out.append(Move(src,dst)); continue
                if occupant and occupant.color != color and occupant.role != 'king':
                    out.append(Move(src,dst,'promotion' if dst[1] in (0,7) else 'normal'))
                elif dst == self.en_passant and not occupant:
                    victim = self.get((dst[0], y))
                    if victim and victim.role == 'pawn' and victim.color != color:
                        out.append(Move(src,dst,'en_passant'))
            if not attacks_only:
                forward = (x,y+direction)
                if in_board(*forward) and not self.get(forward):
                    out.append(Move(src,forward,'promotion' if forward[1] in (0,7) else 'normal'))
                    two = (x,y+2*direction)
                    if (not p.moved and y == (6 if color=='white' else 1)
                            and in_board(*two) and not self.get(two)
                            and (not p.evolved or ABILITIES['pawn']['allow_normal_two_step'])):
                        out.append(Move(src,two))
                if p.evolved:
                                                                          
                    for dx,dy in ABILITIES['pawn']['extra_empty_steps']:
                        extra = (x+dx,y+dy*direction)
                        if in_board(*extra) and not self.get(extra):
                            out.append(Move(src,extra))
        elif p.role == 'knight':
            offsets = KNIGHT_OFFSETS[:]
            if p.evolved:
                for a,b in ABILITIES['knight']['extra_jumps']:
                    offsets += [(sx*dx,sy*dy) for dx,dy in ((a,b),(b,a))
                                for sx in (-1,1) for sy in (-1,1)]
                offsets += [(0, direction*i) for i in range(1,ABILITIES['knight']['extra_forward']+1)]
            for dx,dy in set(offsets):
                dst = (x+dx,y+dy)
                if in_board(*dst) and (not self.get(dst) or self.get(dst).color != color):
                    out.append(Move(src,dst))
        elif p.role in ('bishop','rook','queen'):
            dirs = (DIRS_DIAGONAL if p.role == 'bishop' else
                    DIRS_ORTHOGONAL if p.role == 'rook' else DIRS_ALL)
            targets = self.trace(src,dirs,color,
                p.role=='bishop' and p.evolved and ABILITIES['bishop']['jump_enemy_pieces'])
            for dst in targets:
                out.append(Move(src,dst))
            if p.role == 'queen' and p.evolved and ABILITIES['queen']['add_knight_jumps']:
                for dx,dy in KNIGHT_OFFSETS:
                    dst=(x+dx,y+dy)
                    if in_board(*dst) and (not self.get(dst) or self.get(dst).color!=color):
                        out.append(Move(src,dst))
            if (p.role == 'rook' and p.evolved and ABILITIES['rook']['allow_king_swap']
                    and not attacks_only):
                king_pos = self.king_square(color)
                if king_pos is not None:
                    out.append(Move(src,king_pos,'swap'))
        elif p.role == 'king':
            distance = ABILITIES['king']['max_distance'] if p.evolved else 1
            for dx,dy in DIRS_ALL:
                for i in range(1,distance+1):
                    dst = (x+dx*i,y+dy*i)
                    if not in_board(*dst): break
                    target = self.get(dst)
                    if target and target.color == color: break
                    out.append(Move(src,dst))
                    if target: break
            if not attacks_only and not p.moved and x==4 and y==(7 if color=='white' else 0):
                for rook_x,king_dst,between in ((7,6,(5,6)),(0,2,(1,2,3))):
                    rook=self.get((rook_x,y))
                    if (rook and rook.role=='rook' and rook.color==color and not rook.moved
                            and all(not self.get((bx,y)) for bx in between)):
                        out.append(Move(src,(king_dst,y),'castle'))
        if attacks_only:
            return out
                                                                                     
        return [m for m in out if m.kind=='swap' or not
                (self.get(m.dst) and self.get(m.dst).role=='king')]

    def square_attacked(self, sq, by_color):
        for origin,p in self.board.items():
            if p.color == by_color:
                if any(m.dst==sq for m in self.targets(origin,True)):
                    return True
        return False

    def in_check(self, color):
        king = self.king_square(color)
        return king is None or self.square_attacked(king,self.enemy(color))

    def apply(self, move):

        p = self.board.pop(move.src)
        captured = None
        if move.kind == 'swap':
            king=self.board.pop(move.dst)
            self.board[move.src]=king
            self.board[move.dst]=p
            king.moved=True; p.moved=True
        elif move.kind == 'castle':
            row=move.src[1]
            rook_from=(7,row) if move.dst[0]==6 else (0,row)
            rook_to=(5,row) if move.dst[0]==6 else (3,row)
            rook=self.board.pop(rook_from)
            rook.moved=True
            self.board[rook_to]=rook
            self.board[move.dst]=p
            p.moved=True
        else:
            captured=self.board.pop(move.dst,None)
            if move.kind=='en_passant':
                captured=self.board.pop((move.dst[0],move.src[1]))
            self.board[move.dst]=p
            p.moved=True
            if captured:
                self.evolve(p)
            if p.role=='pawn' and move.dst[1] in (0,7):
                p.role = move.promote or 'queen'
        self.en_passant=None
        if p.role=='pawn' and abs(move.dst[1]-move.src[1])==2 and move.kind=='normal':
            self.en_passant=(move.src[0],(move.src[1]+move.dst[1])//2)
        self.halfmove = 0 if captured or p.role=='pawn' or (move.kind=='promotion') else self.halfmove+1
        if self.turn=='black': self.fullmove+=1
        self.turn=self.enemy(self.turn)
        self.last_move=move
        return captured

    def evolve(self, piece):

        piece.captures += 1
        if piece.captures >= ABILITY_UNLOCK_CAPTURES:
            piece.evolved = True

    def legal_moves(self, color=None, only_from=None):
        color = color or self.turn
        sources = [only_from] if only_from else list(self.board)
        legal=[]
        for src in sources:
            p = self.get(src)
            if not p or p.color!=color: continue
            for m in self.targets(src):
                                                                             
                if m.kind=='castle':
                    if self.in_check(color): continue
                    step=1 if m.dst[0]>src[0] else -1
                    cross=(src[0]+step,src[1])
                    if self.square_attacked(cross,self.enemy(color)): continue
                if p.role=='king' and m.kind != 'castle' and p.evolved:
                    dx=m.dst[0]-src[0]; dy=m.dst[1]-src[1]
                    if max(abs(dx),abs(dy))>1 and ABILITIES['king']['require_safe_intermediate']:
                        step=(src[0]+(dx>0)-(dx<0),src[1]+(dy>0)-(dy<0))
                        if self.square_attacked(step,self.enemy(color)): continue
                                                                                
                                                                             
                saved_board=copy.deepcopy(self.board)
                saved_meta=(self.turn,self.en_passant,self.halfmove,
                            self.fullmove,self.last_move)
                try:
                    self.apply(m)
                    safe=not self.in_check(color)
                finally:
                    self.board=saved_board
                    (self.turn,self.en_passant,self.halfmove,
                     self.fullmove,self.last_move)=saved_meta
                if safe: legal.append(m)
        return legal

    def make_move(self, move):
        legal=self.legal_moves(only_from=move.src)
        valid=next((m for m in legal if m.dst==move.dst and m.kind==move.kind),None)
        if valid is None or self.result: return False
        if valid.kind=='promotion':
            if move.promote not in ('queen','rook','bishop','knight'):
                return False
            valid=Move(valid.src,valid.dst,valid.kind,move.promote)
        piece=self.get(valid.src)
        former=piece.display_species
        role=piece.role
        captured=self.get(valid.dst)
        if valid.kind=='en_passant': captured=self.get((valid.dst[0],valid.src[1]))
        captured_name=captured.display_species if captured else ''
        state=self.snapshots()
        self.apply(valid)
        self.history.append(state)
        notation = (ROLE_SYMBOL[role] + algebraic(valid.src) +
                    ('x' if captured else '-') + algebraic(valid.dst))
        if valid.kind=='castle': notation='O-O' if valid.dst[0]==6 else 'O-O-O'
        if valid.kind=='swap': notation='Swap '+algebraic(valid.src)+'↔'+algebraic(valid.dst)
        if valid.kind=='en_passant': notation+=' e.p.'
        if valid.kind=='promotion': notation+='='+ROLE_SYMBOL[valid.promote]
        if captured: notation+=f' ({former} → {piece.display_species}; took {captured_name})'
        self.position_counts[self.position_key()]+=1
        self.refresh_result()
        if self.in_check(self.turn): notation += '#' if self.result and 'checkmate' in self.result else '+'
        self.move_names.append(notation)
        return True

    def insufficient_material(self):
                                                                              
                                                                           
        others=[(sq,p) for sq,p in self.board.items() if p.role!='king']
        if not others:
            return True
        if any(p.evolved for p in self.board.values() if p.role=='king'):
            return False
        if len(others)==1 and others[0][1].role in ('bishop','knight') and not others[0][1].evolved:
            return True
        if (all(p.role=='bishop' and not p.evolved for _,p in others)
                and len({(sq[0]+sq[1])%2 for sq,_ in others})==1):
            return True
        return False

    def refresh_result(self):
        self.result=None
        moves=self.legal_moves()
        if not moves:
            if self.in_check(self.turn):
                self.result=f'{self.enemy(self.turn).title()} wins by checkmate'
            else:
                self.result='Draw by stalemate'
        elif self.halfmove >= 150:
            self.result='Draw by 75-move rule'
        elif self.position_counts[self.position_key()] >= 5:
            self.result='Draw by fivefold repetition'
        elif self.insufficient_material():
            self.result='Draw by insufficient material'

    def claimable_draw(self):
        if self.halfmove>=100: return '50-move rule'
        if self.position_counts[self.position_key()]>=3: return 'threefold repetition'
        return None

    def claim_draw(self):
        reason=self.claimable_draw()
        if reason and not self.result:
            self.result=f'Draw claimed by {reason}'
            return True
        return False


                                                                              
                                                                
                                                                              
                                            
                                                                           
                                                                        
                                                                          
                                                                            

def all_species():
    original = [name for items in ROSTER.values() for name in items]
    forms = {EVOLUTIONS[name] for name in original}
    forms.update(MIDDLE_EVOLUTIONS.values())
    return [('normal', name) for name in original] + [
        ('evolved', name) for name in sorted(forms)]


def sprite_destination(group, color, name):
    folder = SPRITE_ROOT / ('evolved' if group == 'evolved' else '') / color
    return folder / (slug(name) + '.png')


def valid_png(path):
    try:
        with open(path, 'rb') as image:
            header = image.read(24)
        if len(header) != 24 or header[:8] != b'\x89PNG\r\n\x1a\n' or header[12:16] != b'IHDR':
            return False
        width = int.from_bytes(header[16:20], 'big')
        height = int.from_bytes(header[20:24], 'big')
        return 1 <= width <= 4096 and 1 <= height <= 4096 and Path(path).stat().st_size > 68
    except OSError:
        return False


def png_data_valid(data):
    return (len(data) > 68 and data[:8] == b'\x89PNG\r\n\x1a\n'
            and data[12:16] == b'IHDR'
            and 0 < int.from_bytes(data[16:20], 'big') <= 4096
            and 0 < int.from_bytes(data[20:24], 'big') <= 4096)


def sprites_missing():
    return [(group, color, name) for group, name in all_species()
            for color in ('normal', 'shiny')
            if not valid_png(sprite_destination(group, color, name))]


def fetch_bytes(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 PokemonChess/2.0',
                                'Accept': 'image/png,application/json,*/*'})
    with urlopen(req, timeout=SPRITE_NETWORK_TIMEOUT) as response:
        return response.read()


def save_png(destination, data):
    if not png_data_valid(data):
        return False
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix('.part')
    temporary.write_bytes(data)
    temporary.replace(destination)
    return True


def pokemon_sprite_urls(pokemon_id, color):
    shiny = 'shiny/' if color == 'shiny' else ''
    return [
        f'{SPRITE_SOURCE}/versions/generation-v/black-white/{shiny}{pokemon_id}.png',
        f'{SPRITE_SOURCE}/{shiny}{pokemon_id}.png',
    ]


def download_sprite(task):
    group, color, name, pokemon_id = task
    dest = sprite_destination(group, color, name)
    if valid_png(dest):
        return True
    for url in pokemon_sprite_urls(pokemon_id, color):
        try:
            if save_png(dest, fetch_bytes(url)):
                return True
        except (OSError, HTTPError, URLError, TimeoutError, ValueError):
            pass
    return False


def chess_piece_filename(role, color):
    return ('w' if color == 'white' else 'b') + {'pawn':'p', 'rook':'r',
        'knight':'n', 'bishop':'b', 'queen':'q', 'king':'k'}[role] + '.png'


def chess_pieces_missing():
    return [(role, color) for role in SELECTION_PER_ROLE
            for color in ('white', 'black')
            if not valid_png(CHESS_PIECE_ROOT / chess_piece_filename(role, color))]


def download_chess_piece(task):
    role, color = task
    filename = chess_piece_filename(role, color)
    destination = CHESS_PIECE_ROOT / filename
    if valid_png(destination):
        return True
    for template in CHESS_PIECE_URLS:
        try:
            if save_png(destination, fetch_bytes(template.format(name=filename[:-4]))):
                return True
        except (OSError, HTTPError, URLError, TimeoutError, ValueError):
            pass
    return False


def get_pokemon_numbers():
    try:
        catalog = json.loads(fetch_bytes(POKEAPI_INDEX))
        names = {entry['name']: entry['url'].rstrip('/').rsplit('/', 1)[-1]
                 for entry in catalog['results']}
        if names:
            return names
    except (OSError, ValueError, KeyError, TypeError, URLError, TimeoutError):
        pass
    try:
        csv_text = fetch_bytes('https://raw.githubusercontent.com/PokeAPI/pokeapi/master/data/v2/csv/pokemon.csv').decode('utf-8')
        import csv
        import io
        return {row['identifier']: row['id'] for row in csv.DictReader(io.StringIO(csv_text))}
    except (OSError, ValueError, KeyError, TypeError, URLError, TimeoutError):
        return {}


class SpriteDownloadProgress:
    def __init__(self):
        self.done = False
        self.total = 0
        self.completed = 0
        self.successes = 0
        self.errors = []
        self.status = 'Checking online sprite catalogue...'


def install_sprites(progress=None):
    progress = progress or SpriteDownloadProgress()
    missing_pokemon = sprites_missing()
    missing_chess = chess_pieces_missing()
    progress.total = len(missing_pokemon) + len(missing_chess)
    if progress.total == 0:
        progress.status = 'All Pokémon and chess-piece sprites are installed.'
        progress.done = True
        return progress

    if missing_chess:
        progress.status = 'Downloading Neo chess-piece images...'
        with ThreadPoolExecutor(max_workers=min(SPRITE_WORKERS, 8)) as pool:
            futures = {pool.submit(download_chess_piece, item): item for item in missing_chess}
            for future in as_completed(futures):
                role, color = futures[future]
                try:
                    ok = future.result()
                except Exception:
                    ok = False
                progress.completed += 1
                if ok:
                    progress.successes += 1
                else:
                    progress.errors.append(f'Chess.com Neo {color} {role}')

    if missing_pokemon:
        progress.status = 'Downloading normal, shiny, and evolved Pokémon PNGs...'
        numbers = get_pokemon_numbers()
        tasks = []
        for group, color, name in missing_pokemon:
            identifier = numbers.get(SPRITE_ALIASES.get(slug(name), slug(name)))
            if identifier and str(identifier).isdigit():
                tasks.append((group, color, name, str(identifier)))
            else:
                progress.completed += 1
                progress.errors.append(f'Pokémon ID unavailable: {name} ({color})')
        with ThreadPoolExecutor(max_workers=min(SPRITE_WORKERS, 12)) as pool:
            futures = {pool.submit(download_sprite, item): item for item in tasks}
            for future in as_completed(futures):
                group, color, name, number = futures[future]
                try:
                    ok = future.result()
                except Exception:
                    ok = False
                progress.completed += 1
                if ok:
                    progress.successes += 1
                else:
                    progress.errors.append(f'{group} {color} {name}')

    remaining_pokemon = sprites_missing()
    remaining_chess = chess_pieces_missing()
    if progress.errors:
        report = SPRITE_ROOT.parent / 'sprite_download_report.txt'
        report.write_text('Sprites still missing after attempted download:\n' +
                          '\n'.join(progress.errors) + '\n\n'
                          'Re-run with: python3 pokemon_chess_pygame.py --download-sprites\n',
                          encoding='utf-8')
    progress.done = True
    remaining = len(remaining_pokemon) + len(remaining_chess)
    progress.status = (f'Sprite installation: {progress.successes} downloaded, {remaining} still missing'
                       if remaining else 'All Pokémon and chess-piece sprites installed')
    return progress


class BotBudgetExceeded(Exception):
    pass


BOT_VALUES = {'pawn': 100, 'knight': 325, 'bishop': 335,
              'rook': 510, 'queen': 925, 'king': 0}


def bot_evaluate(game):
    score = 0
    for (x, y), piece in game.board.items():
        value = BOT_VALUES[piece.role]
        value += (55 if piece.evolved else 0) + min(piece.captures, 2) * 20
        if piece.role in ('pawn', 'knight', 'bishop'):
            value += 12 * (3.5 - abs(x - 3.5))
            if piece.role == 'pawn':
                value += (6-y if piece.color == 'white' else y-1)*7
        score += value if piece.color == 'black' else -value
    return score


def bot_move_score(game, move):
    actor = game.get(move.src)
    target = game.get(move.dst)
    capture = BOT_VALUES[target.role] if target else 0
    if move.kind == 'en_passant':
        capture = 100
    if move.kind == 'promotion':
        capture += 800
    center = 4 - abs(move.dst[0] - 3.5) - abs(move.dst[1] - 3.5)
    return capture * 12 - BOT_VALUES[actor.role] * (0.1 if target else 0) + center


def bot_search(game, depth, alpha, beta, start, budget, nodes):
    nodes[0] += 1
    if nodes[0] % 12 == 0 and time.monotonic() - start > budget:
        raise BotBudgetExceeded()
    if depth == 0:
        return bot_evaluate(game)
    moves = game.legal_moves()
    if not moves:
        if game.in_check(game.turn):
            return -100000 - depth if game.turn == 'black' else 100000 + depth
        return 0
    maximize = game.turn == 'black'
    moves.sort(key=lambda move: bot_move_score(game, move), reverse=True)
    best = -float('inf') if maximize else float('inf')
    for move in moves:
        board = copy.deepcopy(game.board)
        state = (game.turn, game.en_passant, game.halfmove,
                 game.fullmove, game.last_move)
        try:
            game.apply(move)
            score = bot_search(game, depth-1, alpha, beta, start, budget, nodes)
        finally:
            game.board = board
            (game.turn, game.en_passant, game.halfmove,
             game.fullmove, game.last_move) = state
        if maximize:
            best = max(best, score)
            alpha = max(alpha, best)
        else:
            best = min(best, score)
            beta = min(beta, best)
        if beta <= alpha:
            break
    return best


def bot_complete_promotion(move):
    if move is not None and move.kind == 'promotion' and not move.promote:
        return Move(move.src, move.dst, move.kind, 'queen')
    return move


def choose_bot_move(game, difficulty, rng=None):
    rng = rng or random.Random()
    moves = game.legal_moves()
    if not moves:
        return None
    if difficulty == 500:
        weights = [1 + max(0,bot_move_score(game,m))/500 for m in moves]
        return bot_complete_promotion(rng.choices(moves, weights=weights, k=1)[0])
    if difficulty == 750:
        scores = [(bot_move_score(game,m) + rng.gauss(0,320),m) for m in moves]
        return bot_complete_promotion(max(scores,key=lambda item:item[0])[1])
    max_time = 1.6 if difficulty == 1300 else 4.0
    depth = 2 if difficulty == 1300 else 3
    start = time.monotonic()
    candidates = sorted(moves, key=lambda m:bot_move_score(game,m), reverse=True)
    if difficulty == 1300:
        candidates = candidates[:min(12,len(candidates))]
    else:
        candidates = candidates[:min(14,len(candidates))]
    best = candidates[0]
    best_score = -float('inf')
    nodes = [0]
    for move in candidates:
        if time.monotonic()-start > max_time:
            break
        board = copy.deepcopy(game.board)
        state=(game.turn,game.en_passant,game.halfmove,game.fullmove,game.last_move)
        try:
            game.apply(move)
            score = bot_search(game,depth-1,-float('inf'),float('inf'),
                               start,max_time,nodes)
        except BotBudgetExceeded:
            break
        finally:
            game.board=board
            (game.turn,game.en_passant,game.halfmove,
             game.fullmove,game.last_move)=state
        score += rng.uniform(-15,15) if difficulty == 1300 else rng.uniform(-3,3)
        if score>best_score:
            best_score,best=score,move
    return bot_complete_promotion(best)

WINDOW_BG = '#292725'
PANEL_BG = '#34312e'
BUTTON_BG = '#52504a'
BUTTON_HOVER = '#656158'
GREEN = '#81a65b'
FG = '#f2efe9'
FAINT = '#b7b3aa'
LIGHT_SQUARE = '#f0d9b5'
DARK_SQUARE = '#b58863'
PIECE_GLYPH = {'pawn': '♟', 'rook': '♜', 'bishop': '♝',
               'knight': '♞', 'queen': '♛', 'king': '♚'}


class PixelImages:
    def __init__(self):
        self.cache = {}

    def load(self, path, limit):
        path = Path(path)
        if not valid_png(path):
            return None
        try:
            stamp = path.stat().st_mtime_ns
            key = (str(path), limit, stamp)
            if key in self.cache:
                return self.cache[key]
            im = tk.PhotoImage(file=str(path))
            w, h = im.width(), im.height()
            if w <= 0 or h <= 0:
                return None
            desired = limit / max(w, h)
            candidates = [(p / q, p, q)
                          for p in range(1, 7) for q in range(1, 13)
                          if p / q <= desired]
            if candidates:
                _, numer, denom = max(candidates)
                if numer != 1:
                    im = im.zoom(numer)
                if denom != 1:
                    im = im.subsample(denom)
            elif max(w, h) > limit:
                im = im.subsample(math.ceil(max(w, h) / limit))
            if len(self.cache) > 950:
                self.cache.clear()
            self.cache[key] = im
            return im
        except (tk.TclError, OSError):
            return None

    def pokemon(self, species, color, original, limit):
        folder = SPRITE_ROOT / ('shiny' if color == 'black' else 'normal')
        if species != original:
            path = SPRITE_ROOT / 'evolved' / ('shiny' if color == 'black' else 'normal') / (slug(species)+'.png')
            image = self.load(path, limit)
            if image is not None:
                return image
        return self.load(folder / (slug(original)+'.png'), limit)

    def chess(self, role, color, limit):
        return self.load(CHESS_PIECE_ROOT / chess_piece_filename(role, color), limit)


class PokemonChessTk:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Pokemon Chess')
        self.root.configure(bg=WINDOW_BG)
        self.root.geometry('1270x850')
        self.root.minsize(850, 640)
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', lambda e: self.set_fullscreen(False))
        self.fullscreen = False
        self.images = PixelImages()
        self.mode = 'menu'
        self.opponent = 'friend'
        self.difficulty = 500
        self.draft = TeamDraft()
        self.role = 'pawn'
        self.game = None
        self.selected = None
        self.drag_start = None
        self.drag_active = False
        self.bot_busy = False
        self.bot_token = 0
        self.events = queue.Queue()
        self.download_busy = False
        self.status = tk.StringVar(value='')
        self.content = tk.Frame(self.root, bg=WINDOW_BG)
        self.content.pack(fill='both', expand=True)
        self.root.after(125, self.poll_events)
        self.show_menu()
        try:
            self.set_fullscreen(True)
        except tk.TclError:
            self.set_fullscreen(False)
        self.begin_download()

    def set_fullscreen(self, value):
        self.fullscreen = value
        self.root.attributes('-fullscreen', value)

    def toggle_fullscreen(self, event=None):
        self.set_fullscreen(not self.fullscreen)

    def clear_content(self):
        self.root.unbind_all('<MouseWheel>')
        for widget in self.content.winfo_children():
            widget.destroy()

    def label(self, parent, content, size=15, color=FG, bold=False, **kwargs):
        return tk.Label(parent, text=content, bg=parent.cget('bg'), fg=color,
                        font=('Helvetica', size, 'bold' if bold else 'normal'), **kwargs)

    def button(self, parent, content, command, primary=False, **kwargs):
        return tk.Button(parent, text=content, command=command, bg=GREEN if primary else BUTTON_BG,
                         fg='#ffffff', activebackground='#91b86c' if primary else BUTTON_HOVER,
                         activeforeground='#ffffff', bd=0, highlightthickness=0,
                         relief='flat', font=('Helvetica', 13), cursor='hand2',
                         padx=14, pady=11, **kwargs)

    def show_menu(self):
        self.mode = 'menu'
        self.bot_token += 1
        self.clear_content()
        box = tk.Frame(self.content, bg=WINDOW_BG)
        box.place(relx=.5, rely=.46, anchor='center')
        self.label(box, 'POKÉMON CHESS', 35, GREEN, True).pack(pady=(0, 8))
        self.label(box, 'Choose how you want to play', 15, FAINT).pack(pady=(0, 35))
        self.button(box, 'Play with a Friend', lambda: self.start_draft('friend'), True, width=27).pack(pady=6)
        self.button(box, 'Play a Bot', self.show_bots, width=27).pack(pady=6)
        if self.game:
            self.button(box, 'Resume Game', self.show_game, width=27).pack(pady=6)
        self.button(box, 'Quit', self.root.destroy, width=27).pack(pady=6)
        self.label(box, 'F11 = Fullscreen     •     F5 = Retry sprites', 11, FAINT).pack(pady=26)
        self.root.bind('<F5>', lambda e: self.begin_download())

    def show_bots(self):
        self.mode = 'bots'
        self.clear_content()
        box = tk.Frame(self.content, bg=WINDOW_BG)
        box.place(relx=.5, rely=.45, anchor='center')
        self.label(box, 'PLAY A BOT', 31, GREEN, True).pack(pady=20)
        self.label(box, 'You play White. Bot plays Black.', 13, FAINT).pack(pady=(0, 20))
        for elo in BOT_DIFFICULTIES:
            self.button(box, f'{elo} Elo', lambda value=elo: self.start_draft('bot', value),
                        width=25).pack(pady=5)
        self.button(box, 'Back', self.show_menu, width=25).pack(pady=22)

    def start_draft(self, opponent, difficulty=500):
        self.opponent = opponent
        self.difficulty = difficulty
        self.draft = TeamDraft()
        self.role = 'pawn'
        self.game = None
        self.show_draft()

    def show_draft(self):
        self.mode = 'draft'
        self.clear_content()
        color = self.draft.turn
        header = tk.Frame(self.content, bg=WINDOW_BG)
        header.pack(fill='x', padx=24, pady=(18, 12))
        self.label(header, f"{'WHITE' if color=='white' else 'BLACK'} TEAM", 26, GREEN, True).pack(side='left')
        self.label(header, f'{self.draft.count(color)} / 16 selected', 14, FAINT).pack(side='left', padx=25)
        self.button(header, 'Randomize Team', self.random_team, True).pack(side='right', padx=8)
        self.button(header, 'Menu', self.show_menu).pack(side='right')
        tabs = tk.Frame(self.content, bg=WINDOW_BG)
        tabs.pack(fill='x', padx=24, pady=(0, 14))
        for role in ROSTER:
            num = len(self.draft.teams[color][role]); total = SELECTION_PER_ROLE[role]
            b = self.button(tabs, f'{role.title()} {num}/{total}', lambda r=role: self.change_role(r),
                            primary=role==self.role)
            b.pack(side='left', padx=(0, 6))
        holder = tk.Frame(self.content, bg=WINDOW_BG)
        holder.pack(fill='both', expand=True, padx=24, pady=(0, 18))
        scroller = tk.Canvas(holder, bg=WINDOW_BG, highlightthickness=0)
        bar = ttk.Scrollbar(holder, orient='vertical', command=scroller.yview)
        scroller.configure(yscrollcommand=bar.set)
        bar.pack(side='right', fill='y')
        scroller.pack(side='left', fill='both', expand=True)
        cards = tk.Frame(scroller, bg=WINDOW_BG)
        window = scroller.create_window((0, 0), window=cards, anchor='nw')
        cards.bind('<Configure>', lambda e: scroller.configure(scrollregion=scroller.bbox('all')))
        scroller.bind('<Configure>', lambda e: scroller.itemconfigure(window, width=e.width))
        chosen = {s for values in self.draft.teams[color].values() for s in values}
        full = len(self.draft.teams[color][self.role]) >= SELECTION_PER_ROLE[self.role]
        self.card_refs = []
        for i, name in enumerate(ROSTER[self.role]):
            item = tk.Frame(cards, bg=PANEL_BG, highlightthickness=1,
                            highlightbackground=GREEN if name in chosen else '#47443f', height=92)
            item.grid(row=i//4, column=i%4, padx=6, pady=6, sticky='nsew')
            cards.grid_columnconfigure(i%4, weight=1)
            image = self.images.pokemon(name, color, name, 66)
            if image:
                pic = tk.Label(item, image=image, bg=PANEL_BG)
                pic.image = image
                pic.pack(side='left', padx=(10, 4), pady=7)
                self.card_refs.append(image)
            else:
                self.label(item, name[:2].upper(), 18, GREEN, True).pack(side='left', padx=14)
            info = tk.Frame(item, bg=PANEL_BG)
            info.pack(side='left', fill='both', expand=True, padx=4)
            self.label(info, name, 12, FG, True).pack(anchor='w', pady=(14, 2))
            state = 'Selected' if name in chosen else ('Full' if full else 'Choose')
            self.label(info, state, 10, GREEN if name in chosen else FAINT).pack(anchor='w')
            if name not in chosen and not full:
                for widget in (item, info, *info.winfo_children()):
                    widget.bind('<Button-1>', lambda e, role=self.role, species=name: self.pick(role, species))
                for widget in item.winfo_children():
                    widget.bind('<Button-1>', lambda e, role=self.role, species=name: self.pick(role, species))
            item.grid_propagate(False)
        self.root.bind_all('<MouseWheel>', lambda e: scroller.yview_scroll(-1 if e.delta>0 else 1, 'units'))

    def change_role(self, role):
        self.role = role
        self.show_draft()

    def pick(self, role, name):
        if self.draft.select(role, name):
            self.after_pick()

    def random_team(self):
        if self.draft.randomize():
            self.after_pick()

    def after_pick(self):
        if self.opponent == 'bot' and self.draft.complete('white'):
            self.draft.randomize()
        if self.draft.done:
            self.game = ChessGame(self.draft.teams)
            self.show_game()
        else:
            if len(self.draft.teams[self.draft.turn][self.role]) >= SELECTION_PER_ROLE[self.role]:
                self.role = next((r for r in ROSTER if len(self.draft.teams[self.draft.turn][r]) < SELECTION_PER_ROLE[r]), 'pawn')
            self.show_draft()

    def show_game(self):
        if not self.game:
            return self.show_menu()
        self.mode = 'game'
        self.clear_content()
        self.selected = None
        self.drag_start = None
        self.drag_active = False
        self.bot_busy = False
        area = tk.Frame(self.content, bg=WINDOW_BG)
        area.pack(fill='both', expand=True, padx=14, pady=12)
        self.board_canvas = tk.Canvas(area, bg=WINDOW_BG, bd=0, highlightthickness=0)
        self.board_canvas.pack(side='left', fill='both', expand=True)
        side = tk.Frame(area, bg=PANEL_BG, width=265)
        side.pack(side='right', fill='y', padx=(15, 0))
        side.pack_propagate(False)
        self.label(side, 'POKÉMON CHESS', 17, GREEN, True).pack(anchor='w', padx=16, pady=(18, 8))
        self.turn_label = self.label(side, '', 15, FG, True)
        self.turn_label.pack(anchor='w', padx=16, pady=5)
        self.info_label = self.label(side, '', 11, FAINT)
        self.info_label.pack(anchor='w', padx=16, pady=6)
        self.button(side, 'Undo', self.undo).pack(fill='x', padx=16, pady=(17, 5))
        self.button(side, 'Restart', self.restart).pack(fill='x', padx=16, pady=5)
        self.button(side, 'New Teams', lambda: self.start_draft(self.opponent, self.difficulty)).pack(fill='x', padx=16, pady=5)
        self.button(side, 'Main Menu', self.show_menu).pack(fill='x', padx=16, pady=5)
        self.button(side, 'Claim Draw', self.claim_draw).pack(fill='x', padx=16, pady=5)
        self.label(side, 'MOVE HISTORY', 12, FAINT, True).pack(anchor='w', padx=16, pady=(22, 5))
        history_container = tk.Frame(side, bg=PANEL_BG)
        history_container.pack(fill='both', expand=True, padx=16, pady=(0, 16))
        scrollbar = ttk.Scrollbar(history_container)
        scrollbar.pack(side='right', fill='y')
        self.history_box = tk.Text(history_container, bg='#302e2a', fg=FG,
                                   font=('Helvetica', 11), relief='flat', bd=0,
                                   wrap='word', state='disabled', yscrollcommand=scrollbar.set)
        self.history_box.pack(side='left', fill='both', expand=True)
        scrollbar.configure(command=self.history_box.yview)
        self.board_canvas.bind('<Configure>', lambda e: self.render_board())
        self.board_canvas.bind('<ButtonPress-1>', self.on_press)
        self.board_canvas.bind('<B1-Motion>', self.on_drag)
        self.board_canvas.bind('<ButtonRelease-1>', self.on_release)
        self.render_board()
        self.maybe_bot()

    def flipped(self):
        return self.opponent == 'friend' and self.game.turn == 'black'

    def geometry(self):
        canvas = self.board_canvas
        width = max(canvas.winfo_width(), 400)
        height = max(canvas.winfo_height(), 400)
        size = max(320, min(width - 20, height - 20))
        cell = size / 8
        return (width - size)/2, (height - size)/2, cell

    def from_pixel(self, x, y):
        ox, oy, cell = self.geometry()
        file = int((x-ox)//cell)
        rank = int((y-oy)//cell)
        if not in_board(file, rank):
            return None
        if self.flipped():
            file, rank = 7-file, 7-rank
        return (file, rank)

    def pixel(self, square):
        ox, oy, cell = self.geometry()
        x, y = square
        if self.flipped():
            x, y = 7-x, 7-y
        return ox+x*cell, oy+y*cell, cell

    def render_board(self):
        if self.mode != 'game' or not self.board_canvas.winfo_exists():
            return
        c = self.board_canvas
        c.delete('all')
        ox, oy, cell = self.geometry()
        last = self.game.last_move
        legal = self.game.legal_moves(only_from=self.selected) if self.selected else []
        by_dest = {m.dst: m for m in legal}
        for y in range(8):
            for x in range(8):
                square = (x,y)
                left, top, _ = self.pixel(square)
                color = LIGHT_SQUARE if (x+y)%2 == 0 else DARK_SQUARE
                if last and square in (last.src, last.dst):
                    color = '#d3c47a' if (x+y)%2==0 else '#a59759'
                if square == self.selected:
                    color = '#f1e18e'
                king = self.game.get(square)
                if king and king.role == 'king' and self.game.in_check(king.color):
                    color = '#d7736a'
                c.create_rectangle(left, top, left+cell, top+cell, fill=color, outline=color)
        self.board_refs = []
        for square, piece in self.game.board.items():
            left, top, _ = self.pixel(square)
            size = round(cell*.86)
            chess = self.images.chess(piece.role, piece.color, size)
            if chess:
                c.create_image(left+cell/2, top+cell/2, image=chess)
                self.board_refs.append(chess)
            else:
                symbol = PIECE_GLYPH[piece.role]
                c.create_text(left+cell/2, top+cell/2, text=symbol, fill='#f7f4e6' if piece.color=='white' else '#171717',
                              font=('DejaVu Sans', max(21, round(cell*.73))))
            pokemon = self.images.pokemon(piece.display_species, piece.color, piece.species, round(cell*.53))
            if pokemon:
                c.create_image(left+4, top+cell-4, image=pokemon, anchor='sw')
                self.board_refs.append(pokemon)
            else:
                c.create_text(left+7, top+cell-8, anchor='sw', text=piece.species[:2].upper(), fill=GREEN,
                              font=('Helvetica', max(9, round(cell*.16)), 'bold'))
            c.create_text(left+cell-5, top+5, anchor='ne', text=ROLE_SYMBOL[piece.role],
                          font=('Helvetica', max(10, round(cell*.17)), 'bold'),
                          fill='#faf9f5' if piece.color=='black' else '#26231e')
            if piece.evolved:
                c.create_oval(left+4, top+4, left+11, top+11, fill='#f2cd48', outline='')
        for dst, move in by_dest.items():
            left, top, _ = self.pixel(dst)
            radius = cell*.14
            if self.game.get(dst) or move.kind in ('swap','en_passant'):
                inset = cell*.08
                c.create_oval(left+inset, top+inset, left+cell-inset, top+cell-inset,
                              outline='#3d7d41', width=max(2, int(cell*.075)))
            else:
                cx, cy = left+cell/2, top+cell/2
                c.create_oval(cx-radius, cy-radius, cx+radius, cy+radius,
                              fill='#568558', outline='')
        for y in range(8):
            for x in range(8):
                if x==0 or y==7:
                    real = (7-x,7-y) if self.flipped() else (x,y)
                    left,top,_ = self.pixel(real)
                    if x==0:
                        c.create_text(left+3,top+3,anchor='nw',text=str(8-real[1]),
                                      fill='#4a473d',font=('Helvetica',9,'bold'))
                    if y==7:
                        c.create_text(left+cell-3,top+cell-3,anchor='se',text='abcdefgh'[real[0]],
                                      fill='#4a473d',font=('Helvetica',9,'bold'))
        self.turn_label.config(text=f"{'White' if self.game.turn=='white' else 'Black'} to move")
        count = sum(p.evolved for p in self.game.board.values())
        self.info_label.config(text=self.game.result or f'{count} Pokémon powered up')
        self.history_box.config(state='normal')
        self.history_box.delete('1.0','end')
        for i, move in enumerate(self.game.move_names):
            self.history_box.insert('end', f'{i//2+1}{"." if i%2==0 else "..."} {move}\n')
        self.history_box.see('end')
        self.history_box.config(state='disabled')

    def on_press(self, e):
        if self.bot_busy or self.game.result or (self.opponent=='bot' and self.game.turn=='black'):
            return
        square = self.from_pixel(e.x, e.y)
        if square is None:
            self.selected = None
            self.render_board()
            return
        piece = self.game.get(square)
        self.drag_start = (square, e.x, e.y) if piece and piece.color == self.game.turn else None
        self.drag_active = False
        if self.selected is not None and square != self.selected:
            if self.try_destination(square):
                return
        if piece and piece.color == self.game.turn:
            self.selected = square
        else:
            self.selected = None
        self.render_board()

    def on_drag(self, e):
        if not self.drag_start:
            return
        square, x, y = self.drag_start
        if abs(e.x-x)+abs(e.y-y) >= 8:
            self.drag_active = True
        if self.drag_active:
            self.board_canvas.delete('dragghost')
            piece = self.game.get(square)
            if piece:
                image = self.images.chess(piece.role,piece.color,int(self.geometry()[2]*.8))
                if image:
                    self.board_canvas.create_image(e.x,e.y,image=image,tags='dragghost')
                    self.board_refs.append(image)
                else:
                    self.board_canvas.create_text(e.x,e.y,text=PIECE_GLYPH[piece.role],
                                                  font=('DejaVu Sans',36),tags='dragghost')

    def on_release(self, e):
        if not self.drag_start:
            return
        square = self.from_pixel(e.x,e.y)
        initial = self.drag_start[0]
        dragging = self.drag_active
        self.drag_start = None
        self.drag_active = False
        self.board_canvas.delete('dragghost')
        if dragging and square and square!=initial:
            self.selected = initial
            self.try_destination(square)
        self.render_board()

    def try_destination(self, square):
        valid = [m for m in self.game.legal_moves(only_from=self.selected) if m.dst==square]
        if not valid:
            return False
        move = valid[0]
        if move.kind == 'promotion':
            chosen = self.ask_promotion()
            if not chosen:
                return True
            move = Move(move.src,move.dst,move.kind,chosen)
        if self.game.make_move(move):
            self.selected = None
            self.render_board()
            self.show_result()
            self.maybe_bot()
        return True

    def ask_promotion(self):
        dialog = tk.Toplevel(self.root)
        dialog.title('Promote pawn')
        dialog.configure(bg=WINDOW_BG)
        dialog.transient(self.root)
        dialog.grab_set()
        value = tk.StringVar(value='')
        for role in ('queen','rook','bishop','knight'):
            self.button(dialog,role.title(),lambda r=role: (value.set(r),dialog.destroy())).pack(fill='x',padx=22,pady=4)
        self.root.wait_window(dialog)
        return value.get()

    def maybe_bot(self):
        if self.opponent != 'bot' or not self.game or self.game.result or self.game.turn!='black':
            return
        self.bot_busy = True
        self.bot_token += 1
        token = self.bot_token
        game = copy.deepcopy(self.game)
        difficulty = self.difficulty
        self.turn_label.config(text='Bot thinking...')
        def worker():
            try:
                result = choose_bot_move(game,difficulty)
            except Exception:
                result = None
            self.events.put(('bot',token,result))
        threading.Thread(target=worker,daemon=True).start()

    def poll_events(self):
        try:
            while True:
                action,*payload = self.events.get_nowait()
                if action == 'bot':
                    token,move = payload
                    if token==self.bot_token and self.mode=='game' and self.game and self.game.turn=='black':
                        self.bot_busy = False
                        if move:
                            self.game.make_move(move)
                        self.render_board()
                        self.show_result()
                elif action == 'download':
                    progress = payload[0]
                    self.download_busy = False
                    self.images.cache.clear()
                    self.status.set(progress.status)
                    if self.mode=='game':
                        self.render_board()
                    elif self.mode=='draft':
                        self.show_draft()
        except queue.Empty:
            pass
        self.root.after(125,self.poll_events)

    def show_result(self):
        if self.game.result:
            messagebox.showinfo('Game finished', self.game.result)

    def undo(self):
        self.bot_token += 1
        self.bot_busy = False
        if self.game:
            self.game.undo()
            if self.opponent=='bot' and self.game.turn=='black':
                self.game.undo()
        self.selected = None
        self.render_board()

    def restart(self):
        self.bot_token += 1
        self.bot_busy = False
        self.game.reset()
        self.selected = None
        self.render_board()
        self.maybe_bot()

    def claim_draw(self):
        if self.game.claim_draw():
            self.render_board()
            self.show_result()

    def begin_download(self):
        if self.download_busy:
            return
        if not sprites_missing() and not chess_pieces_missing():
            return
        self.download_busy = True
        def worker():
            result = install_sprites()
            self.events.put(('download',result))
        threading.Thread(target=worker,daemon=True).start()

    def run(self):
        self.root.mainloop()


def test_core():
    assert len(ROSTER['pawn']) == 32
    assert sum(map(len, ROSTER.values())) == 176
    d=TeamDraft()
    assert d.select('pawn','Caterpie')
    assert not d.select('pawn','Caterpie')
    assert d.randomize(random.Random(1))
    assert d.turn=='black'
    assert d.select('pawn','Caterpie')
    assert d.randomize(random.Random(2))
    assert d.done
    g=ChessGame(d.teams)
    assert len(g.legal_moves())==20
    assert g.make_move(Move((4,6),(4,4)))
    assert g.undo()
    assert len(g.legal_moves())==20
    for color in ('white','black'):
        assert all(len(d.teams[color][role])==SELECTION_PER_ROLE[role] for role in SELECTION_PER_ROLE)
    for level in BOT_DIFFICULTIES:
        game=ChessGame(d.teams)
        game.make_move(Move((4,6),(4,4)))
        m=choose_bot_move(game,level,random.Random(7))
        assert m in game.legal_moves()
    print('Tkinter Pokémon Chess engine tests passed.')


if __name__ == '__main__':
    if '--test' in sys.argv:
        test_core()
    elif '--verify-sprites' in sys.argv:
        print('Missing Pokémon PNGs:',len(sprites_missing()))
        print('Missing chess PNGs:',len(chess_pieces_missing()))
    elif '--download-sprites' in sys.argv:
        print(install_sprites().status)
    else:
        PokemonChessTk().run()