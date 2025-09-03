import pytest
from main import BooksCollector

class TestBooksCollector:

    # --- add_new_book ---
    @pytest.mark.parametrize("name", ["А", "Б" * 40])  # 1 и 40 символов — допустимо
    def test_add_new_book_accepts_length_bounds(self, collector, name):
        collector.add_new_book(name)
        assert name in collector.get_books_genre()
        assert collector.get_books_genre()[name] == ""

    @pytest.mark.parametrize("name", ["", "В" * 41])   # 0 и 41 — нельзя
    def test_add_new_book_rejects_empty_and_too_long(self, collector, name):
        collector.add_new_book(name)
        assert name not in collector.get_books_genre()

    def test_add_new_book_no_duplicates(self, collector):
        collector.add_new_book("Книга")
        collector.add_new_book("Книга")
        assert list(collector.get_books_genre().keys()).count("Книга") == 1

    # --- set_book_genre / get_book_genre ---
    @pytest.mark.parametrize("genre", ["Фантастика", "Ужасы", "Детективы", "Мультфильмы", "Комедии"])
    def test_set_book_genre_valid_values(self, collector, genre):
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", genre)
        assert collector.get_book_genre("Книга") == genre

    @pytest.mark.parametrize("bad_genre", ["Роман", "Драма", ""])
    def test_set_book_genre_ignores_invalid_and_keeps_empty(self, collector, bad_genre):
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", bad_genre)
        assert collector.get_book_genre("Книга") == ""  # жанр не поменялся

    def test_set_book_genre_does_not_create_new_book(self, collector):
        collector.set_book_genre("Несуществующая", "Комедии")
        assert "Несуществующая" not in collector.get_books_genre()

    def test_get_book_genre_unknown_returns_none(self, collector):
        assert collector.get_book_genre("Нет такой") is None

    # --- get_books_with_specific_genre / get_books_genre ---
    def test_get_books_with_specific_genre_returns_correct_list(self, collector):
        collector.add_new_book("B1"); collector.set_book_genre("B1", "Комедии")
        collector.add_new_book("B2"); collector.set_book_genre("B2", "Комедии")
        collector.add_new_book("B3"); collector.set_book_genre("B3", "Фантастика")
        assert sorted(collector.get_books_with_specific_genre("Комедии")) == ["B1", "B2"]

    def test_get_books_with_specific_genre_invalid_returns_empty(self, collector):
        collector.add_new_book("B1"); collector.set_book_genre("B1", "Комедии")
        assert collector.get_books_with_specific_genre("Роман") == []

    def test_get_books_genre_returns_current_state(self, collector):
        collector.add_new_book("B1")
        collector.add_new_book("B2"); collector.set_book_genre("B2", "Фантастика")
        assert collector.get_books_genre() == {"B1": "", "B2": "Фантастика"}

    # --- get_books_for_children + favorites набор методов ---
    def test_children_and_favorites_flow(self, collector):
        # книги с возрастным рейтингом не попадают в "детям"
        collector.add_new_book("Страшилки"); collector.set_book_genre("Страшилки", "Ужасы")
        collector.add_new_book("Дело");       collector.set_book_genre("Дело", "Детективы")
        # безопасные жанры попадают
        collector.add_new_book("Мультик");    collector.set_book_genre("Мультик", "Мультфильмы")
        collector.add_new_book("Веселье");    collector.set_book_genre("Веселье", "Комедии")
        assert sorted(collector.get_books_for_children()) == ["Веселье", "Мультик"]

        # favorites: можно добавить только существующую и без дублей
        collector.add_book_in_favorites("Веселье")
        collector.add_book_in_favorites("Веселье")     # повтор игнорируется
        collector.add_book_in_favorites("Нет такой")   # не добавится
        assert collector.get_list_of_favorites_books() == ["Веселье"]

        # удаление работает тихо
        collector.delete_book_from_favorites("Веселье")
        collector.delete_book_from_favorites("Веселье")  # повтор — без ошибки
        assert collector.get_list_of_favorites_books() == []

    def test_get_book_genre_returns_set_genre(self, collector):
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Фантастика")
        assert collector.get_book_genre("Книга") == "Фантастика"

    def test_add_book_in_favorites_adds_book_once(self, collector):
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        collector.add_book_in_favorites("Книга")  # повтор игнорируется
        assert collector.get_list_of_favorites_books() == ["Книга"]

    def test_delete_book_from_favorites_removes_book(self, collector):
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        collector.delete_book_from_favorites("Книга")
        assert collector.get_list_of_favorites_books() == []

    def test_get_list_of_favorites_books_returns_current_list(self, collector):
        collector.add_new_book("К1")
        collector.add_new_book("К2")
        collector.add_book_in_favorites("К1")
        collector.add_book_in_favorites("К2")
        assert collector.get_list_of_favorites_books() == ["К1", "К2"]

