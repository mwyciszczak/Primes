import requests, sympy

url = "http://localhost:8000/primes"

response = requests.get(url)
primes = response.json()

sorted(primes)
print(len(primes))
print(primes[-1])

primes_check = [x for x in primes if sympy.isprime(x)]
print(len(primes_check))
print(primes_check[-1])