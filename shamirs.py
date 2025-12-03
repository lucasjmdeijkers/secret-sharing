import random
from random import randrange, seed

SECRET = 10
THRESHOLD = 3

secret_coord = tuple([0,SECRET])

print(secret_coord)

#TODO: Use security safe pseudo-RNG from module 'secrets'

random.seed()

coefficients = []

for i in range(0,THRESHOLD):
    coefficients.append(random.randrange(1, 10))

print(coefficients)

print(f'{coefficients[0]}x^2 + {coefficients[1]}x + {coefficients[2]}')









