from book import Book
from job_status import JobStatus
from random import randint
from updatable import Updatable

class Request(Updatable):
    def __init__(self, requester, publisher, book: Book, num_copies: int, waiting_time: int):
        self._requester = requester
        self._publisher = publisher
        self._book = book
        self._num_copies = num_copies
        self._waiting_time = waiting_time
        
    @property
    def publisher(self):
        return self._publisher
        
    @property
    def requester(self):
        return self._requester
        
    @property
    def book(self):
        return self._book

    @property
    def num_copies(self):
        return self._num_copies

    @property
    def waiting_time(self):
        return self._waiting_time
    
    @property
    def status(self):
        if self.is_completed():
            return JobStatus.Completed
        return JobStatus.InProgress
    
    def is_completed(self):
        return self._waiting_time == 0
    
    def update(self):
        self._waiting_time -= 1
        
    

class Publisher(Updatable):
    def __init__(self, name: str, books: list[Book]):
        self._name = name
        self._books = books
        
        
        self._requests: list[Request] = []
        
    @property
    def name(self) -> str:
        return self._name
    
    def request(self, requester, book: Book, num_copies: int) -> Request:
        if book not in self._books:
            raise ValueError(f"Publisher {self.name} does not publish '{book.title}' book")
        
        days = randint(1, 5)
        
        request = Request(requester, self, book, num_copies, days)
        
        self._requests.append(request)
        
        return request
    
    def update(self):
        for request in self._requests:
            request.update()
            if request.is_completed():
                request.requester.recieve_request(request)
                self._requests.remove(request)