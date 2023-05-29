import requests
import time
from multiprocessing.pool import ThreadPool
from nonos import nonos

pokeurl = "https://pokeapi.co/api/v2/"

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
    try:
        spriteUrl = pokemon.get('sprites').get('front_default')

        spriteImg = requests.get(spriteUrl).content
        with open(f"./assets/pokesprites/{pokemon.get('name')}.png", 'wb') as picwrite:
            picwrite.write(spriteImg)
        
        print(f"\t SPRITE LOADED:{id: 5.0f} || {pokemon.get('name'):^27} ||")
    except:
        print(f"\t\tFailed to get {pokemon.get('name')}")


start = time.perf_counter()
print("Downloading Pokemon Sprites!!!")
with ThreadPool() as pool:
    pool.map(getmon, ids)
print(f"Pokemon Sprites Loaded In{time.perf_counter() - start: .3f}s !!!")
time.sleep(.4)

start = time.perf_counter()
print("Downloading Regional Form Sprites !!!")
with ThreadPool() as rpool:
    rpool.map(getmon, extraids)
print(f"Regional Form Sprites Loaded In{time.perf_counter() - start: .3f}s !!!")