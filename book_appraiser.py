from book import Book
from updatable import Updatable

class BookAppraiser(Updatable):
    def __init__(self, books: list[Book], costs_and_markups: dict[Book, tuple[float, float]]):
        self._books = books
        self._costs = {book: cost for book, (cost, _) in costs_and_markups.items()}
        self._markups = {book: markup for book, (_, markup) in costs_and_markups.items()}
        
        self._time = 0

    def cost(self, book: Book):
        return self._costs[book]
    
    def markup(self, book: Book):
        return self._markups[book]
    
    def update(self):
        if self._time % 2 and self._time < 30:
            
            new_books = filter(lambda x: x.year > 2010, self._books)
            
            for book in new_books:
                self._markups[book] /= 1.01
                
        self._time += 1