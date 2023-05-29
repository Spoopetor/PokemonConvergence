import requests
import json
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

typecombos = []
typeabilities = {}
typemoves = {}
typemons = {}
idmons = {}

for t1 in types:
    typecombos.append((t1))
    typemons[(t1)] = []
    for t2 in types:
        if t1 != t2 and (t2, t1) not in typecombos:
            typecombos.append((t1, t2))
            typemons[(t1, t2)] = []


ids = [i for i in range(1, 1011)]

def getmon(id):
    pokemon = requests.get(pokeurl + f'pokemon/{id}').json()
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
    
def getmoves(pokemon):
    pass

print("Loading Pokemon!!!")
with ThreadPool() as pool:
    pool.map(getmon, ids)
print("Pokemon Loaded!!!")

