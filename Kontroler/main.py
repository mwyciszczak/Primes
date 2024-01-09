from fastapi import FastAPI, Depends, BackgroundTasks
from schemas import ReturnedPrimesRequest
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import datetime


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def scheduled_task(db: Session = Depends(get_db)):
    time_since = datetime.datetime.now() - datetime.timedelta(minutes=61) # XDXDDDDDDDDDD
    records_to_move = db.query(models.BoundCurrent).filter(models.BoundCurrent.created_at < time_since).all()
    if not records_to_move:
        print("Nie ma co przerzucać")
    else:
        for record in records_to_move:
            bound_orphan_record = models.BoundOrphan(bound_orphan=record.bound_current)
            db.add(bound_orphan_record)
            db.delete(record)
        db.commit()
        print("Przeniesiono jakies rekordy")


# Zwraca znalezione liczby pierwsze
@app.get("/primes")
def primes(db: Session = Depends(get_db)):
    primes_db_object = db.query(models.Primes)
    primes_py_list = [x.prime_value for x in primes_db_object]
    return primes_py_list


# Zwraca granicę od której należy zacząć przeszukiwanie
@app.get("/bound")
def bound(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(scheduled_task, db)
    # Przypadek 1, istnieją porzucone wartości 
    bound_value = db.query(models.BoundOrphan).first() #Puste zwróci None
    if bound_value is not None: # Czemu nie działa samo if bound_value, skoro ma wartość
        bound_value_int = bound_value.bound_orphan
        db.delete(bound_value)
        bound_current = models.BoundCurrent(bound_current=bound_value_int)
        db.add(bound_current)
        db.commit()
        return bound_value_int
    
    # Przypadek 2, nie istnieją porzucone wartości
    bound_value = db.query(models.Bound).first() # Jak zwróci None to mamy problem
    bound_value_int = bound_value.bound_value
    bound_value.bound_value += 100
    bound_current = models.BoundCurrent(bound_current=bound_value_int)
    db.add(bound_current)
    db.commit()
    return bound_value_int


# Post request wrzucający znalezione liczby pierwsze do tablicy ze znalezionymi liczbami pierwszymi
@app.post("/returned")
def returned(returned_primes: ReturnedPrimesRequest, db: Session = Depends(get_db)):
    for prime in returned_primes.returned_primes:
        temp_prime = models.Primes(prime_value=prime)
        db.add(temp_prime)
        db.commit()
    bound_value = returned_primes.bound
    entry_to_delete = db.query(models.BoundCurrent).filter(models.BoundCurrent.bound_current == bound_value).first()
    db.delete(entry_to_delete)
    db.commit()
        
        
    return "Liczby zostaly przyjete"
