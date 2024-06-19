from updatable import Updatable
from order import Order, OrderUnit, Customer, Source
from order_handler import OrderHandler
from book import Book, Genre
from book_appraiser import BookAppraiser
from abc import ABC
import random
import numpy as np

class OrderGenerator(Updatable, ABC):
    def __init__(self, order_handler: OrderHandler, customers: list[Customer], books: list[Book], book_appraiser: BookAppraiser) -> None:
        Updatable.__init__(self)
        ABC.__init__(self)
        
        self._order_handler = order_handler
        self._book_appraiser = book_appraiser
        self._customers = customers
        self._books = books
        
        def normalize(probs):
            return probs / np.sum(probs)
        
        self._probs = normalize([self._probability_of_book(book) for book in books])

        self._source = Source.Store
    
    def generate_order(self):
        order = self._generate_order()
        self._order_handler.add_order(order)
    
    def _generate_order(self) -> Order:
        customer = self._random_customer()
        order_units = self._generate_order_units()
        
        order = Order(customer, order_units, self._source)
        return order
    
    def _generate_order_units(self) -> list[OrderUnit]:
        books = [self._random_book() for _ in range(random.randint(1, 3))]
        num_of_books = [random.randint(1, 3) for _ in range(len(books))]
        costs = [self._book_appraiser.cost(book) for book in books]
        markups = [self._book_appraiser.markup(book) for book in books]
        
        order_units = [OrderUnit(book, num, cost, markup) for book, num, cost, markup in zip(books, num_of_books, costs, markups)]
        
        return order_units
    
    def _random_customer(self) -> Customer:
        return random.choice(self._customers)
    
    def _random_book(self) -> Book:
        return np.random.choice(self._books, p=self._probs)
    
    def _probability_of_book(self, book: Book) -> float:
        genre_prob = {
            Genre.Biography: 0.1,
            Genre.Drama: 0.2,
            Genre.Mystery: 0.15,
            Genre.Romance: 0.1,
            Genre.SciFi: 0.15,
            Genre.Horror: 0.1,
            Genre.Fantasy: 0.2,
            Genre.HistoricalFiction: 0.1,
            Genre.NonFiction: 0.05,
            Genre.Poetry: 0.05,
            Genre.Thriller: 0.1
        }
        
        return 1 + genre_prob[book.genre] + self._probability_of_year(book.year_of_publishing)
    
    def _probability_of_year(self, year: int) -> float:
        if year > 2000:
            return 0.5
        if year > 1950:
            return 0.3
        if year > 1900:
            return 0.15
        return 0.0
    
    def update(self):
        self.generate_order()
    
class Store(OrderGenerator):
    def __init__(self, order_handler: OrderHandler, customers: list[Customer], books: list[Book], book_appraiser: BookAppraiser) -> None:
        super().__init__(order_handler, customers, books, book_appraiser)
        self._source = Source.Store

class Phone(OrderGenerator):
    def __init__(self, order_handler: OrderHandler, customers: list[Customer], books: list[Book], book_appraiser: BookAppraiser) -> None:
        super().__init__(order_handler, customers, books, book_appraiser)
        if any(customer.phone is None for customer in customers):
            raise ValueError("Phone number is required for phone orders")
        self._source = Source.Phone
        
class Email(OrderGenerator):
    def __init__(self, order_handler: OrderHandler, customers: list[Customer], books: list[Book], book_appraiser: BookAppraiser) -> None:
        super().__init__(order_handler, customers, books, book_appraiser)
        if any(customer.email is None for customer in customers):
            raise ValueError("Email is required for email orders")
        self._source = Source.Email
        
class RandomSource:
    def __init__(self, order_handler: OrderHandler, customers: list[Customer], books: list[Book], book_appraiser: BookAppraiser) -> None:
        self._order_handler = order_handler
        self._customers = customers
        self._books = books
        self._book_appraiser = book_appraiser
        
        self._generators = [
            Store(self._order_handler, self._customers, self._books, self._book_appraiser),
            Phone(self._order_handler, list(filter(lambda x: x.has_phone(), self._customers)), self._books, self._book_appraiser),
            Email(self._order_handler, list(filter(lambda x: x.has_email(), self._customers)), self._books, self._book_appraiser)
        ]
        
    def generate_order(self):
        random.choice(self._generators).generate_order()
    
    def update(self):
        for i in range(random.randint(1, 3)):
            self.generate_order()
