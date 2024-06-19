from book import Book
from order import Order, OrderUnit
#from publisher import Publisher
from request_handler import RequestHandler

class BookRecord:
    def __init__(self, num_copies: int):
        self._num_copies = num_copies
        self._num_copies_sold = 0
        self._num_ordered = 0
        self._num_waiting = 0
    
    @property
    def num_copies(self):
        return self._num_copies

    @num_copies.setter
    def num_copies(self, value):
        self._num_copies = value

    @property
    def num_copies_sold(self):
        return self._num_copies_sold

    @num_copies_sold.setter
    def num_copies_sold(self, value):
        self._num_copies_sold = value
        
    @property
    def num_ordered(self):
        return self._num_ordered
    
    @num_ordered.setter
    def num_ordered(self, value):
        self._num_ordered = value
        
    @property
    def num_waiting(self):
        return self._num_waiting
    
    @num_waiting.setter
    def num_waiting(self, value):
        self._num_waiting = value
        
    def sold(self, num_copies: int):
        self._num_copies -= num_copies
        self._num_copies_sold += num_copies
    

class BookManager:
    def __init__(self, books: list[Book], request_handler: RequestHandler):
        default_num_copies = 20
        self._records = {book: BookRecord(default_num_copies) for book in books}
        self._request_handler = request_handler
        
        self._pending_orders = {}
        
        self._min_stock = 5
        self._num_of_books_to_request = 10
        
    def _order_unit(self, order_unit: OrderUnit):
        book = order_unit.book
        
        if self._records[book].num_copies < order_unit.num_copies:
            self._records[book].num_waiting += order_unit.num_copies
            if book not in self._pending_orders:
                self._pending_orders[book] = [order_unit]
            else:
                self._pending_orders[book].append(order_unit)
                
            self._request_book(book, order_unit.num_copies)
        else:
            self._records[book].sold(order_unit.num_copies)
            order_unit.complete()
            
        if self._records[book].num_copies < self._min_stock and book not in self._pending_orders:
            self._request_book_default(book)
            
    def order(self, order: Order):
        for order_unit in order.order_units:
            self._order_unit(order_unit)
        
    def _request_book_default(self, book: Book):
        self._request_book(book, self._num_of_books_to_request)

    def _request_book(self, book: Book, num_copies: int):
        self._request_handler.add_request(book, num_copies)
        self._records[book].num_ordered += num_copies
        
    def receive_requested_book(self, book: Book, num_copies: int):
        record = self._records[book]
        record.num_copies += num_copies
        if book in self._pending_orders:
            for order in self._pending_orders[book]:
                if order.book == book:
                    if order.num_copies > record.num_copies:
                        self._request_book_default(book)
                        return
                    
                    self._records[book].num_waiting -= order.num_copies
                    record.sold(order.num_copies)
                    order.complete()
                    self._pending_orders[book].remove(order)
        #books[book].num_ordered -= num_copies
        
    def book_rating(self, book: Book) -> float:
        max_sold = max([record.num_copies_sold for record in self._records.values()])
        
        if max_sold == 0:
            return 0.0
        
        record = self._records[book]
        
        return round(record.num_copies_sold / max_sold * 10, 2)
    
    def book_sold(self, book: Book) -> int:
        return self._records[book].num_copies_sold
    
    def book_stored(self, book: Book) -> int:
        return self._records[book].num_copies