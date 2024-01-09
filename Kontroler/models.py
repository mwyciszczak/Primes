from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from database import Base


# Tabela przechowująca liczby pierwsze
class Primes(Base):
    __tablename__ = 'primes'

    id = Column(Integer, primary_key=True, index=True)
    prime_value = Column(Integer)


# Tabela przechowująca jedną wartość z zakresem dolnym
class Bound(Base):
    __tablename__ = 'bound'

    id = Column(Integer, primary_key=True, index=True)#Zaczynamy od zera
    bound_value = Column(Integer)


# Tabela która przechowuje obecnie mielone zakresy
class BoundCurrent(Base):
    __tablename__ = 'bound_current'

    id = Column(Integer, primary_key=True, index=True)
    bound_current = Column(Integer)
    created_at = Column(DateTime, default=func.now())


# Tabela która przechowuje porzucone zakresy
class BoundOrphan(Base):
    __tablename__ = 'bound_orphan'

    id = Column(Integer, primary_key=True, index=True)
    bound_orphan = Column(Integer)




