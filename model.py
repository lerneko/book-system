from book import Book
from book_appraiser import BookAppraiser
from order import Customer, Order
from publisher import Publisher, Request
from order_handler import OrderHandler
from request_handler import RequestHandler
from book_manager import BookManager
from order_generator import RandomSource
from updatable import Updatable

class BookView:
    def __init__(self, book: Book, book_manager: BookManager, book_appraiser: BookAppraiser):
        self._book = book
        self._book_manager = book_manager
        self._book_appraiser = book_appraiser
        
    @property
    def title(self):
        return self._book.title
    
    @property
    def author(self):
        return self._book.author
    
    @property
    def genre(self):
        return self._book.genre.rus()
    
    @property
    def publisher(self):
        return self._book.publisher
    
    @property
    def year_of_publishing(self):
        return self._book.year_of_publishing
    
    @property
    def num_pages(self):
        return self._book.num_pages
    
    @property
    def num_stored(self):
        return self._book_manager.book_stored(self._book)
    
    @property
    def num_sold(self):
        return self._book_manager.book_sold(self._book)
    
    @property
    def cost(self):
        return self._book_appraiser.cost(self._book)
    
    @property
    def markup(self):
        return self._book_appraiser.markup(self._book)
    
    @property
    def rating(self):
        return self._book_manager.book_rating(self._book)
    
    @staticmethod
    def columns():
        return ('title', 'num_stored', 'num_sold', 'cost', 'markup', 'price', 'rating', 'author', 'genre', 'publisher', 'year_of_publishing', 'num_pages')
    
    @staticmethod
    def num_columns():
        return ('num_stored', 'num_sold', 'cost', 'markup', 'year_of_publishing', 'num_pages', 'price', 'rating')
    
    @staticmethod
    def not_num_columns():
        return ('title', 'author', 'genre', 'publisher')
    
    @staticmethod
    def headers():
        return ('Название', 'Хранится', 'Продано', 'Себетоимость, р.', 'Наценка, %', 'Цена, р.', 'Рейтинг', 'Автор', 'Жанр', 'Издательство', 'Год издания', 'Кол-во стр.')
    
    @staticmethod
    def widths():
        return (100, 5, 5, 5, 5, 5, 5, 20, 20, 20, 20, 20)
    
    def values(self):
        return (self.title, self.num_stored, self.num_sold, self.cost,
                str(self.markup * 100), self.cost + self.cost * self.markup, self.rating, self.author, self.genre, self.publisher,
                self.year_of_publishing, self.num_pages)


class Model(Updatable):
    def __init__(self, customers: list[Customer], books: list[Book], costs_and_markups: dict[Book, tuple[float, float]]):
        self._customers = customers
        self._books = books
        
        publisher_names = list(set(book.publisher for book in books))
        self._publishers = [Publisher(name, list(filter(lambda x: x.publisher == name, self._books))) for name in publisher_names]
        
        self._request_handler = RequestHandler(self._publishers)
        self._book_manager = BookManager(self._books, request_handler=self._request_handler)
        self._request_handler.set_book_manager(self._book_manager)
        self._order_handler = OrderHandler(self._book_manager)
        
        self._book_appraiser = BookAppraiser(self._books, costs_and_markups)
        
        self._rand_source = RandomSource(self._order_handler, self._customers, self._books, self._book_appraiser)
        
        self._updatable: list[Updatable] = [self._rand_source, self._order_handler]
        self._updatable.extend(self._publishers)
        
        self._days = 0
        
    def update(self):
        for updatable in self._updatable:
            updatable.update()
        self._days += 1
            
    def book_views(self) -> list[BookView]:
        return [BookView(book, self._book_manager, self._book_appraiser) for book in self._books]
    
    def orders(self) -> list[Order]:
        return self._order_handler.all_orders
    
    def requests(self) -> list[Request]:
        return self._request_handler.all_requests
            
    def genre_stats(self) -> list[tuple[str, int]]:
        genre_stats = {}
        for book in self._books:
            genre = book.genre.rus()
            if genre not in genre_stats:
                genre_stats[genre] = 0
            genre_stats[genre] += self._book_manager.book_sold(book)
        return genre_stats.items()