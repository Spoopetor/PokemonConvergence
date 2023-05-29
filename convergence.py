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

nonos = ['gmax', 'etnernamax', 'mega', 'build', 'mode', 'noice']

typecombos = []
typeabilities = {}
typemoves = {}
typemons = {}
idmons = {}
idtype = {}

for t1 in types:
    typecombos.append((t1))
    typemons[(t1)] = []
    for t2 in types:
        if t1 != t2 and (t2, t1) not in typecombos:
            typecombos.append((t1, t2))
            typemons[(t1, t2)] = []


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
    print(f"\t LOADED: {id: 4.0f} - {pokemon.get('name')} == {types}")

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
    
def getmoves(pokemon):
    pass

print("Loading Pokemon!!!")
with ThreadPool() as pool:
    pool.map(getmon, ids)
print("Pokemon Loaded!!!")
time.sleep(.4)

print("Loading Regional Forms!!!")
with ThreadPool() as rpool:
    rpool.map(getmon, extraids)
print("Regional Forms Loaded!!!")

