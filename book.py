import enum

class Genre(enum.Enum):
    Fantasy = 1
    SciFi = 2
    Mystery = 3
    Romance = 4
    Thriller = 5
    Horror = 6
    HistoricalFiction = 7
    NonFiction = 8
    Biography = 9
    Poetry = 10
    Drama = 11

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def rus(self):
        translation = {
            Genre.Fantasy: "Фэнтези",
            Genre.SciFi: "Научная фантастика",
            Genre.Mystery: "Мистика",
            Genre.Romance: "Романтика",
            Genre.Thriller: "Триллер",
            Genre.Horror: "Ужасы",
            Genre.HistoricalFiction: "Историческая проза",
            Genre.NonFiction: "Документальная литература",
            Genre.Biography: "Биография",
            Genre.Poetry: "Поэзия",
            Genre.Drama: "Драма"
        }
        return translation[self]

class Book:
    def __init__(self, title: str, author: str, genre: Genre, publisher: str, year_of_publishing: int, num_pages: int):
        self._title = title
        self._author = author
        self._publisher = publisher
        self._num_pages = num_pages
        self._year_of_publishing = year_of_publishing
        self._genre = genre

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def publisher(self):
        return self._publisher

    @property
    def num_pages(self):
        return self._num_pages
    
    @property
    def year_of_publishing(self):
        return self._year_of_publishing
    
    @property
    def genre(self):
        return self._genre

