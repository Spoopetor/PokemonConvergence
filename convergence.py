import requests
import json
import time
from itertools import permutations
from tqdm import tqdm
from multiprocessing.pool import ThreadPool

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

nonos = ['gmax', 'eternamax', 'mega', 'build', 'mode', 'noice']

typecombos = []
typeabilities = {}
typemoves = {}
typemons = {}
idmons = {}
idtype = {}
movemons = {}
abmons = {}

for t1 in types:
    typecombos.append((t1))
    typemons[(t1)] = []
    typemoves[(t1)] = []
    typeabilities[(t1)] = []
    for t2 in types:
        if t1 != t2 and (t2, t1) not in typecombos:
            typecombos.append((t1, t2))
            typemons[(t1, t2)] = []
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
        return(types)
    elif tuple(reversed(types)) in typecombos:
        typemons[tuple(reversed(types))].append(pokemon)
        return(tuple(reversed(types)))
    elif types[0] in typecombos:
        typemons[types[0]].append(pokemon)
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
print(f"Pokemon Loaded in{time.perf_counter() - start: .3f}s !!!")
time.sleep(.4)

start = time.perf_counter()
print("Loading Regional Forms !!!")
with ThreadPool() as rpool:
    rpool.map(getmon, extraids)
print(f"Regional Forms Loaded in{time.perf_counter() - start: .3f}s !!!")
