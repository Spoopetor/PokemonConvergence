import requests
import json
import time
from itertools import permutations
from tqdm import tqdm
from multiprocessing.pool import ThreadPool
from nonos import nonos
import pandas as pd
import openpyxl

pokeurl = "https://pokeapi.co/api/v2/"

types = [
    'normal',
    'fire',
    'water',
    'grass',
    'electric',
    'ice',
    'fighting',
    'poison',
    'ground',
    'flying',
    'psychic',
    'bug',
    'rock',
    'ghost',
    'dark',
    'dragon',
    'steel',
    'fairy'
    ]

typecombos = []
typeabilities = {}
typemoves = {}
typemons = {}
typemonnames = {}
idmons = {}
idtype = {}
movemons = {}
abmons = {}

for t1 in types:
    typecombos.append((t1))
    typemons[(t1)] = []
    typemonnames[(t1)] = []
    typemoves[(t1)] = []
    typeabilities[(t1)] = []
    for t2 in types:
        if t1 != t2 and (t2, t1) not in typecombos:
            typecombos.append((t1, t2))
            typemons[(t1, t2)] = []
            typemonnames[(t1, t2)] = []
            typemoves[(t1, t2)] = []
            typeabilities[(t1, t2)] = []


ids = [i for i in range(1, 1011)]
extraids = []

def getmon(id):
    pokemon = requests.get(pokeurl + f'pokemon/{id}').json()
    if id <= 9999:
        rforms = requests.get(pokeurl + f'pokemon-species/{id}').json().get('varieties')
        if len(rforms) != 1:
            for i in range(1, len(rforms)):
                extraids.append(int(rforms[i].get('pokemon').get('url').split('/')[6]))
    for n in nonos:
        if n in pokemon.get('name'):
            return

    idmons[id] = pokemon
    types = montype(pokemon)
    if type(types) is not tuple:
        types = (types)
    idtype[id] = types
    moves = loadmoves(pokemon, types)
    abilities = loadabilities(pokemon, types)
    print(f"\t LOADED:{id: 5.0f} || {pokemon.get('name'):^27} || {len(moves):>3} moves || {len(abilities):>2} abilities || {types}")

def montype(pokemon):
    types = tuple([i.get('type').get('name') for i in pokemon.get('types')])
    if types in typecombos:
        typemons[types].append(pokemon)
        typemonnames[types].append(pokemon.get('name'))
        return(types)
    elif tuple(reversed(types)) in typecombos:
        typemons[tuple(reversed(types))].append(pokemon)
        typemonnames[tuple(reversed(types))].append(pokemon.get('name'))
        return(tuple(reversed(types)))
    elif types[0] in typecombos:
        typemons[types[0]].append(pokemon)
        typemonnames[types[0]].append(pokemon.get('name'))
        return (types[0])
    
def loadmoves(pokemon, types):
    moves = ([i.get('move').get('name') for i in pokemon.get('moves')])
    for m in moves:
        if m not in movemons.keys():
            movemons[m] = []
        movemons[m].append(pokemon.get('name'))
        if m not in typemoves.get(types):
            typemoves[types].append(m)
    return moves

def loadabilities(pokemon, types):
    abilities = ([i.get('ability').get('name') for i in pokemon.get('abilities')])
    for a in abilities:
        if a not in abmons.keys():
            abmons[a] = []
        abmons[a].append(pokemon.get('name'))
        if a not in typeabilities.get(types):
            typeabilities[types].append(a)
    return abilities
    
start = time.perf_counter()
print("Loading Pokemon !!!")
with ThreadPool() as pool:
    pool.map(getmon, ids)
print(f"Pokemon Loaded In{time.perf_counter() - start: .3f}s !!!")
time.sleep(.4)

start = time.perf_counter()
print("Loading Regional Forms !!!")
with ThreadPool() as rpool:
    rpool.map(getmon, extraids)
print(f"Regional Forms Loaded In{time.perf_counter() - start: .3f}s !!!")

for v in typemoves.values():
    v.sort()
for v in typeabilities.values():
    v.sort()
for v in typemonnames.values():
    v.sort()

start = time.perf_counter()
print("Creating Datasheets !!!")
movedf = pd.DataFrame.from_dict(typemoves, orient='index')
movedf.transpose().to_excel('TypeMoves.xlsx', sheet_name='Type Moves')
abildf = pd.DataFrame.from_dict(typeabilities, orient='index')
abildf.transpose().to_excel('TypeAbilities.xlsx', sheet_name='Type Abilities')
pokedf = pd.DataFrame.from_dict(typemonnames, orient='index')
pokedf.transpose().to_excel('TypePokemon.xlsx', sheet_name='Type Pokemon')
print(f"Datasheets Created In{time.perf_counter() - start: .3f}s !!!")

