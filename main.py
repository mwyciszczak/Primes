from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

bound_value = 10

class ReturnedPrimesRequest(BaseModel):
    returned_primes: list


@app.get("/primes")
def primes():
    with open('primes.txt') as file:
        primes = file.readlines()
    found_primes = [int(x.rstrip()) for x in primes]
    return found_primes


@app.get("/bound")
def bound():
    with open('bound.txt') as file:
        bound_value = int(file.readline().rstrip())
    return bound_value


@app.post("/returned")
def returned(returned_primes: ReturnedPrimesRequest):
    with open('primes.txt', 'a') as file:
        for x in returned_primes.returned_primes:
            file.write('{}\n'.format(x))
    
    with open('primes.txt') as file:
        primes = file.readlines()
    found_primes = [int(x.rstrip()) for x in primes]
    return found_primes 