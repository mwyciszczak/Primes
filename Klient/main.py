import requests, sympy

url_bound = "http://localhost:8000/bound"
url_primes = "http://localhost:8000/returned"

while True:
    bound_value = requests.get(url_bound).json()
    print("Szukam liczb pierwszych w zakresie {}:{}".format(bound_value, bound_value+100))
    primes = []
    for number in range(bound_value, bound_value+101):
        if sympy.isprime(number):
            primes.append(number)
    print("Znaleziono liczby: {}".format(primes))
    data = {"returned_primes": primes, "bound": int(bound_value)}
    response = requests.post(url_primes, json=data)
    print("Kod odpowiedzi: {}".format(response.status_code))
    print(response.json())