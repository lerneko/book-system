from order import Order
from job_status import JobStatus
from updatable import Updatable
import book_manager

class OrderHandler(Updatable):
    def __init__(self, book_manager: book_manager.BookManager):
        self._orders_in_progress = []
        self._orders_completed = []
        
        self._book_manager = book_manager
        
    def add_order(self, order: Order):
        self._orders_in_progress.append(order)
        self._book_manager.order(order)
        
    def update(self):
        for order in self._orders_in_progress:
            order.update()
            if order.status == JobStatus.Completed:
                self._orders_in_progress.remove(order)
                self._orders_completed.append(order)
        
    @property
    def orders_in_progress(self):
        return self._orders_in_progress[::-1]
    
    @property
    def orders_completed(self):
        return self._orders_completed[::-1]
    
    @property
    def all_orders(self):
        return self._orders_in_progress + self._orders_completed