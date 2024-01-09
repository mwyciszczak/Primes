from pydantic import BaseModel

class ReturnedPrimesRequest(BaseModel):
    returned_primes: list
    bound: int