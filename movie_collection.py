from typing import Dict, List, Optional, Iterator


class Movie:
    def __init__(self, title: str, director: str, year: int, genre: str) -> None:
        self.title = title
        self.director = director
        self.year = year
        self.genre = genre

    def __str__(self) -> str:
        return f"{self.title} ({self.year}) - {self.director} [{self.genre}]"


class MovieIterator:
    def __init__(self, movies: Dict[str, Movie]) -> None:
        self._movies = list(movies.values())
        self._index = 0

    def __iter__(self) -> "MovieIterator":
        return self

    def __next__(self) -> Movie:
        if self._index < len(self._movies):
            movie = self._movies[self._index]
            self._index += 1
            return movie
        else:
            raise StopIteration


class MovieCollection:
    def __init__(self) -> None:
        self.movies: Dict[str, Movie] = {}
        self.collections: Dict[str, List[str]] = {}

    def add_movie(self, movie: Movie) -> None:
        self.movies[movie.title] = movie

    def remove_movie(self, title: str) -> None:
        if title in self.movies:
            del self.movies[title]
            for collection in self.collections.values():
                if title in collection:
                    collection.remove(title)

    def add_to_collection(self, collection_name: str, title: str) -> None:
        if title in self.movies:
            if collection_name not in self.collections:
                self.collections[collection_name] = []
            if title not in self.collections[collection_name]:
                self.collections[collection_name].append(title)

    def remove_from_collection(self, collection_name: str, title: str) -> None:
        if collection_name in self.collections:
            if title in self.collections[collection_name]:
                self.collections[collection_name].remove(title)

    def search_movies(
        self,
        title: Optional[str] = None,
        director: Optional[str] = None,
        year: Optional[int] = None,
        genre: Optional[str] = None,
    ) -> List[Movie]:
        results = []
        for movie in self.movies.values():
            if (
                (title is None or title.lower() in movie.title.lower())
                and (director is None or director.lower() in movie.director.lower())
                and (year is None or movie.year == year)
                and (genre is None or genre.lower() in movie.genre.lower())
            ):
                results.append(movie)
        return results

    def __iter__(self) -> Iterator[Movie]:
        return MovieIterator(self.movies)


if __name__ == "__main__":
    collection = MovieCollection()

    collection.add_movie(Movie("Dune: Part Two", "Denis Villeneuve", 2024, "Sci-Fi"))
    collection.add_movie(Movie("Oppenheimer", "Christopher Nolan", 2023, "Biography"))
    collection.add_movie(Movie("Poor Things", "Yorgos Lanthimos", 2023, "Drama"))
    collection.add_movie(Movie("Spider-Man: No Way Home", "Jon Watts", 2021, "Action"))

    collection.add_to_collection("Favorites", "Dune: Part Two")
    collection.add_to_collection("Awards", "Poor Things")

    print("\nРезультаты поиска по жанру Drama:")
    for movie in collection.search_movies(genre="Drama"):
        print(movie)

    print("\nВсе фильмы:")
    for movie in collection:
        print(movie)

    collection.remove_movie("Spider-Man: No Way Home")
    print("\nПосле удаления Spider-Man:")
    for movie in collection:
        print(movie)

