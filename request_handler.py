from publisher import Publisher, Request
#from book_manager import BookManager
from book import Book

class RequestHandler:
    def __init__(self, publishers: list[Publisher]):
        self._publishers = {publisher.name: publisher for publisher in publishers}

        self._in_process_requests = []
        self._done_requests = []
        
    def set_book_manager(self, book_manager):
        self._book_manager = book_manager

    def add_request(self, book: Book, num_copies: int):
        publisher_name = book.publisher
        if publisher_name not in self._publishers:
            raise ValueError("Publisher not found")
        
        publisher = self._publishers[publisher_name]
        request = publisher.request(self, book, num_copies)
        self._in_process_requests.append(request)

    def recieve_request(self, request: Request):
        self._book_manager.receive_requested_book(request.book, request.num_copies)
        self._in_process_requests.remove(request)
        self._done_requests.append(request)
        
        
    @property
    def in_process_requests(self):
        return self._in_process_requests[::-1]
    
    @property
    def done_requests(self):
        return self._done_requests[::-1]
    
    @property
    def all_requests(self):
        return self._in_process_requests + self._done_requests