from typing import Optional
from book import Book
from enum import Enum
from updatable import Updatable
from job_status import JobStatus

class Customer:
    def __init__(self, surname: str, phone: Optional[str] = None, email: Optional[str] = None) -> None:
        if not surname:
            raise ValueError("Surname cannot be empty")
        if not phone and not email:
            raise ValueError("Phone or email must be specified")

        self._surname = surname
        self._phone = phone
        self._email = email

    @property
    def surname(self) -> str:
        return self._surname
    @property
    def phone(self) -> Optional[str]:
        return self._phone
    @property
    def email(self) -> Optional[str]:
        return self._email
    
    def has_phone(self) -> bool:
        return self._phone is not None
    
    def has_email(self) -> bool:
        return self._email is not None




class OrderUnit:
    def __init__(self, book: Book, num_copies: int, cost, markup) -> None:
        self._book = book
        self._num_copies = num_copies
        self._status = JobStatus.InProgress
        self._cost = cost
        self._markup = markup

    @property
    def book(self) -> Book:
        return self._book
    
    @property
    def num_copies(self) -> int:
        return self._num_copies
    @property
    def status(self) -> JobStatus:
        return self._status
    
    @property
    def cost(self) -> float:
        return self._cost
    
    @property
    def markup(self) -> float:
        return self._markup
    
    def complete(self) -> None:
        self._status = JobStatus.Completed
        
class Source(Enum):
    Store = 1
    Phone = 2
    Email = 3
    
    def __str__(self):
        translations = {
            Source.Store: "Магазин",
            Source.Phone: "Телефон",
            Source.Email: "Электронная почта"
        }
        return translations[self]

class Order(Updatable):
    def __init__(self, customer: Customer, order_units: list[OrderUnit], source: Source) -> None:
        self._customer = customer
        self._order_units = order_units
        self._source = source
        self._stauts = JobStatus.InProgress
    
    @property
    def customer(self) -> Customer:
        return self._customer
    
    @property
    def order_units(self) -> list[OrderUnit]:
        return self._order_units[:]
    
    @property
    def status(self) -> JobStatus:
        return self._stauts
    
    @property
    def source(self) -> Source:
        return self._source
    
    def complete(self) -> None:
        self._stauts = JobStatus.Completed
        for unit in self._order_units:
            if unit.status == JobStatus.InProgress:
                raise ValueError("All order units must be completed")
            
    def update(self) -> None:
        for unit in self._order_units:
            if unit.status == JobStatus.InProgress:
                return
        self.complete()
        