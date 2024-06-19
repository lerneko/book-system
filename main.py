from model import Model
from order import Customer
from book import Book, Genre
from gui import GUI

def main():
    customers = [
        Customer("Иван Иванов", "+7 (123) 456-7890"),
        Customer("Мария Смирнова", "+7 (098) 765-4321"),
        Customer("Дмитрий Сидоров", "+7 (111) 111-1111"),
        Customer("Ольга Петрова", email="elena.petrova@example.com"),
        Customer("Екатерина Сидорова", email="dmitriy.sidorov@example.com"),
        Customer("Петрова Елена", "+7 (999) 999-9999", email="petrova.elena@example.com"),
        Customer("Сидоров Дмитрий", "+7 (111) 111-1111", email="sidorov.dmitriy@example.com"),
    ]
    
    books = [
        Book("Война и мир", "Лев Толстой", Genre.Romance, "Классика на века", 1864, 1225),
        Book("Преступление и наказание", "Федор Достоевский", Genre.Mystery, "Классика на века", 1866, 331),
        Book("Мастер и Маргарита", "Михаил Булгаков", Genre.Fantasy, "Азбука", 1966, 384),
        Book("1984", "Джордж Оруэлл", Genre.SciFi, "Азбука", 1949, 328),
        Book("Анна Каренина", "Лев Толстой", Genre.Romance, "Классика на века", 1877, 964),
        Book("Капитал", "Карл Маркс", Genre.NonFiction, "Экономика нашего времени", 1867, 1152),
        Book("Богатство народов", "Адам Смит", Genre.NonFiction, "Экономика нашего времени", 1776, 1248),
        Book("Властелин колец", "Дж. Р. Р. Толкиен", Genre.Fantasy, "Азбука", 1954, 1200),
        Book("Мертвые души", "Николай Гоголь", Genre.HistoricalFiction, "Классика на века", 1842, 352),
        Book("Семь ночей под небом", "Алексей Иванов", Genre.Romance, "Новее некуда", 2021, 320),
        Book("Герванд из Рыбии", "Иванов Алексей", Genre.Fantasy, "Новее некуда", 2023, 423),
    ]
    
    costs_and_markups = {
        books[0]: (500, 0.5),
        books[1]: (300, 0.6),
        books[2]: (400, 0.7),
        books[3]: (350, 0.8),
        books[4]: (450, 0.9),
        books[5]: (550, 0.5),
        books[6]: (650, 0.6),
        books[7]: (750, 0.7),
        books[8]: (850, 0.8),
        books[9]: (950, 1.5),
        books[10]: (1050, 1.2),
    }
    
    model = Model(customers, books, costs_and_markups)
    
    gui = GUI(model)

if __name__ == "__main__":
    main()