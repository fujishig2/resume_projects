
from tiles3 import tiles, IHT

maxSize = 4
iht = IHT(maxSize)
weights = [0]*maxSize
numTilings = 8
stepSize = 0.1/numTilings

def mytiles(x, y):
    scaleFactor = 10.0/(3-1)
    return tiles(iht, numTilings, [x*scaleFactor,y*scaleFactor])

def learn(x, y, z):
    tiles = mytiles(x, y)
    estimate = 0
    for tile in tiles:
        estimate += weights[tile]                  #form estimate
    error = z - estimate
    for tile in tiles:
        weights[tile] += stepSize * error          #learn weights

def test(x, y):
    tiles = mytiles(x, y)
    estimate = 0
    for tile in tiles:
        estimate += weights[tile]
    return estimate

