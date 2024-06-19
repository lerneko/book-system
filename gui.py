import tkinter as tk
from tkinter import ttk
from model import Model, BookView

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GUI:
    def __init__(self, model: Model):
        self.model = model
        self.update_data = [model.update]
        self.update_graphs = []
        
        self.root = tk.Tk()
        self.root.title("Управление книжным магазином")
        self.root.geometry("1200x800")
        
        # Верхняя панель с кнопками и счетчиком дней
        self.create_top_panel()

        # Вкладки
        self._create_tabs()
        
        
        self.root.mainloop()

    def update(self, days=1):
        for _ in range(days):
            for update_func in self.update_data:
                update_func()
            self.days_label.config(text=f"Дни: {self.model._days}")
        
        for update_graph in self.update_graphs:
            update_graph()
    
    def create_top_panel(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        # Кнопки в верхней левой части
        #button1 = tk.Button(top_frame, text="▶")
        #button2 = tk.Button(top_frame, text="⏸")
        
        
        button1 = tk.Button(top_frame, text="1 день", command=self.update)
        button2 = tk.Button(top_frame, text="3 дня", command=lambda: self.update(3))
        button3 = tk.Button(top_frame, text="10 дней", command=lambda: self.update(10))
        button1.pack(side=tk.LEFT, padx=5)
        button2.pack(side=tk.LEFT, padx=5)
        button3.pack(side=tk.LEFT, padx=5)

        # Счетчик дней в верхней правой части
        days_counter_frame = tk.Frame(top_frame)
        days_counter_frame.pack(side=tk.RIGHT, padx=10)
        
        self.days_label = tk.Label(days_counter_frame, text="Дни: 0")
        self.days_label.pack()

    def _create_tabs(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill='both')
        

        # Создаем фреймы для вкладок
        assortment_tab = self._assortment_tab(notebook)
        orders_tab = self._orders_tab(notebook)
        requests_tab = self._requests_tab(notebook)
        genre_tab = self._genre_tab(notebook)
        statistics_tab = self._statistics_tab(notebook)
        graphs_tab = self._graphs_tab(notebook)

        # Добавляем фреймы как вкладки
        notebook.add(assortment_tab, text='Ассортимент')
        notebook.add(orders_tab, text='Заказы')
        notebook.add(requests_tab, text='Заявки в издательство')
        notebook.add(genre_tab, text='Статистика продаж по жанрам')
        notebook.add(statistics_tab, text='Статистика')
        notebook.add(graphs_tab, text='Графики')
    
    def _assortment_tab(self, notebook):
        frame = ttk.Frame(notebook)
        frame.pack(expand=True, fill='both')
        
        tree = ttk.Treeview(frame, columns=BookView.columns(), show='headings')
        tree.pack(expand=True, fill='both')
        
        def sort(col, reverse):
            # получаем все значения столбцов в виде отдельного списка
            
            l = [(tree.set(k, col), k) for k in tree.get_children("")]
            if col in BookView.num_columns():
                l = [(float(x[0]), x[1]) for x in l]
            # сортируем список
            l.sort(reverse=reverse)
            # переупорядочиваем значения в отсортированном порядке
            for index,  (_, k) in enumerate(l):
                tree.move(k, "", index)
            # в следующий раз выполняем сортировку в обратном порядке
            tree.heading(col, command=lambda: sort(col, not reverse))
        
        for i in range(len(BookView.columns())):
            tree.heading(BookView.columns()[i], text=BookView.headers()[i], command=lambda i=i: sort(BookView.columns()[i], False))
            tree.column(BookView.columns()[i], width=BookView.widths()[i])
            
        for book in self.model.book_views():
            tree.insert('', 'end', values=book.values())
            
        def update_treeview():
            # Get current items in the treeview
            current_items = tree.get_children()

            # Get new data
            new_data = self.model.book_views()

            # Update existing items
            for item_id, new_values in zip(current_items, new_data):
                tree.item(item_id, values=new_values.values())

            # If there are more new data than current items, insert the remaining data
            if len(new_data) > len(current_items):
                for extra_data in new_data[len(current_items):]:
                    tree.insert('', 'end', values=extra_data.values())
                    
        self.update_data.append(update_treeview)
        
        return frame
    
    def _orders_tab(self, notebook):
        frame = ttk.Frame(notebook)
        frame.pack(expand=True, fill='both')
        
        tree = ttk.Treeview(frame, columns=('customer', 'book', 'num_copies', 'status'), show='headings')
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        
        tree.configure(yscrollcommand=scrollbar.set)
        tree.tag_configure('bold', font=('',0,'bold'))
        
        tree.pack(expand=True, fill='both')
        
        for col, header in zip(('customer', 'book', 'num_copies', 'status'), ('Клиент', '', 'Источник', 'Статус')):
            tree.heading(col, text=header)
            tree.column(col, width=100)
            
        def update_treeview():
            data = self.model.orders()
            for item in tree.get_children():
                tree.delete(item)
                
            for order in data:
                tree.insert('', 'end', values=(order.customer.surname, '', order.source, order.status), tags=('bold',))
                tree.insert('', 'end', values=('Контакты: ', '', '' if order.customer.phone is None else order.customer.phone,
                                               '' if order.customer.email is None else order.customer.email))
                #tree.insert('', 'end', values=('', '', '', ''))
                tree.insert('', 'end', values=('', 'Книги', 'Кол-во', 'Статус'))
                for order_unit in order.order_units:
                    tree.insert('', 'end', values=('', order_unit.book.title, order_unit.num_copies, order_unit.status))
                    
                tree.insert('', 'end', values=('', '', '', ''))
            
        self.update_data.append(update_treeview)
        
        return frame
    
    def _requests_tab(self, notebook):
        frame = ttk.Frame(notebook)
        frame.pack(expand=True, fill='both')
        
        tree = ttk.Treeview(frame, columns=('publisher', 'book', 'num_copies', 'status', 'wait_time'), show='headings')
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        
        tree.configure(yscrollcommand=scrollbar.set)
        tree.tag_configure('bold', font=('',0,'bold'))
        
        tree.pack(expand=True, fill='both')

        def sort(col, reverse):
            # получаем все значения столбцов в виде отдельного списка
            l = [(tree.set(k, col), k) for k in tree.get_children("")]
            if col in ('num_copies', 'wait_time'):
                l = [(int(x[0]), x[1]) for x in l]
            # сортируем список
            l.sort(reverse=reverse)
            # переупорядочиваем значения в отсортированном порядке
            for index,  (_, k) in enumerate(l):
                tree.move(k, "", index)
            # в следующий раз выполняем сортировку в обратном порядке
            tree.heading(col, command=lambda: sort(col, not reverse))
        
        for col, header in zip(('publisher', 'book', 'num_copies', 'status', 'wait_time'), ('Издательство', 'Книга', 'Кол-во', 'Статус', 'Дни ожидания')):
            tree.heading(col, text=header, command=lambda col=col: sort(col, False))
            tree.column(col, width=100)
            
        def update_treeview():
            requests = self.model.requests()
            for item in tree.get_children():
                tree.delete(item)
              
            for request in requests:
                tree.insert('', 'end', values=(request.publisher.name, request.book.title, 
                                               request.num_copies, request.status,
                                               '' if request.is_completed() else request.waiting_time))
                
        self.update_data.append(update_treeview)
        
        return frame
    
    def _genre_tab(self, notebook):
        frame = ttk.Frame(notebook)
        frame.pack(expand=True, fill='both')
        
        tree = ttk.Treeview(frame, columns=('genre', 'num_sold'), show='headings')
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(expand=True, fill='both')
        
        def sort(col, reverse):
            # получаем все значения столбцов в виде отдельного списка
            
            l = [(tree.set(k, col), k) for k in tree.get_children("")]
            if col == 'num_sold':
                l = [(float(x[0]), x[1]) for x in l]
            # сортируем список
            l.sort(reverse=reverse)
            # переупорядочиваем значения в отсортированном порядке
            for index,  (_, k) in enumerate(l):
                tree.move(k, "", index)
            # в следующий раз выполняем сортировку в обратном порядке
            tree.heading(col, command=lambda: sort(col, not reverse))
        
        for col, header in zip(('genre', 'num_sold'), ('Жанр', 'Продано книг')):
            tree.heading(col, text=header, command=lambda col=col: sort(col, False))
            tree.column(col, width=100)
            
        def update_treeview():
            for item in tree.get_children():
                tree.delete(item)
                
            for genre, num_sold in self.model.genre_stats():
                tree.insert('', 'end', values=(genre, num_sold))
        
        update_treeview()
        
        self.update_data.append(update_treeview)
        
        return frame
    
    def _statistics_tab(self, notebook):
        frame = ttk.Frame(notebook)
        frame.pack(expand=True, fill='both')
        
        tree = ttk.Treeview(frame, columns=('title', 'num'), show='headings')
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(expand=True, fill='both')
        
        for col, header in zip(('title', 'num'), ('Показатель', 'Значение')):
            tree.heading(col, text=header)
            tree.column(col, width=100)
            
        def update_treeview():
            for item in tree.get_children():
                tree.delete(item)
                
            num_of_sold_books = sum(book.num_sold for book in self.model.book_views())
            num_of_stored_books = sum(book.num_stored for book in self.model.book_views())
            num_of_orders = len(self.model.orders())
            num_of_requests = len(self.model.requests())
            revenue = sum((book.cost + book.cost * book.markup) * book.num_sold for book in self.model.book_views())
            expenses = float(sum(book.cost * book.num_sold for book in self.model.book_views()))
            profit = revenue - expenses
            
            values = [
                ('Продано книг', num_of_sold_books),
                ('Хранится книг', num_of_stored_books),
                ('Заказов', num_of_orders),
                ('Заявок в издательства', num_of_requests),
                ('Доход', revenue),
                ('Расходы', expenses),
                ('Прибыль', profit)
            ]
            
            for i in values:
                tree.insert('', 'end', values=i)
        
        update_treeview()
        
        self.update_data.append(update_treeview)
        
        return frame
    
    def _graphs_tab(self, root_notebook):
        notebook = ttk.Notebook(root_notebook)
        notebook.pack(expand=True, fill='both')

        def new_graph(name, x_label, y_label, data_x, data_y):
            frame = ttk.Frame(notebook)
            frame.pack(expand=True, fill='both')
            
            fig = plt.figure(figsize=(4, 4), dpi=100)
            ax = fig.add_subplot(111)
            
            # Создаем график
            ax.plot(days, orders, color='b')
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.set_title(name)

            # Встраиваем фигуру в tkinter Frame
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            
            def update_graph():
                ax.clear()
                ax.plot(data_x, data_y, color='b')
                ax.set_xlabel(x_label)
                ax.set_ylabel(y_label)
                ax.set_title(name)
                canvas.draw()
            
            self.update_graphs.append(update_graph)

            notebook.add(frame, text=name)


        days = [0]
        orders = [0]
        requests = [0]
        books_stored = [sum(book.num_stored for book in self.model.book_views())]

        def update_days():
            days.append(len(days) + 1)
        def update_orders():
            orders.append(len(self.model.orders()) - sum(orders))
        def update_requests():
            requests.append(len(self.model.requests()) - sum(requests))
        def update_books_stores():
            books_stored.append(sum(book.num_stored for book in self.model.book_views()))

        self.update_data.extend([
            update_days,
            update_orders,
            update_requests,
            update_books_stores,
            ])

        new_graph('Кол-во заказов по дням', 'Дни', 'Заказы', days, orders)
        new_graph('Кол-во заявок в издательства по дням', 'Дни', 'Заявки', days, requests)
        new_graph('Кол-во книг на складе по дням', 'Дни', 'Книги', days, books_stored)

        frame = ttk.Frame(notebook)
        frame.pack(expand=True, fill='both')
        
        fig = plt.figure(figsize=(4, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Создаем график
        book_names = [book.title[:8] + '.' for book in self.model.book_views()]
        book_ratings = [book.rating for book in self.model.book_views()]

        ax.bar(book_names, book_ratings, color='b')

        # Встраиваем фигуру в tkinter Frame
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        def update():
            nonlocal book_ratings
            book_ratings = [book.rating for book in self.model.book_views()]
        
        def update_graph():
            ax.clear()
            ax.bar(book_names, book_ratings, color='b')
            canvas.draw()
        
        self.update_data.append(update)
        self.update_graphs.append(update_graph)

        notebook.add(frame, text='Рейтинг книг')
        notebook.pack(expand=True, fill='both')

        return notebook