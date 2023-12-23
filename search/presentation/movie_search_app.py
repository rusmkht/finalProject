import os
from datetime import datetime
import requests
from search.api.imdb_api import IMDbAPI
from search.data.search_file_handler import SearchFileHandler


class MovieSearchApp:
    def __init__(self, api_key, username_hash, key):
        self.imdb_api = IMDbAPI(api_key)
        self.search_log_file = os.path.join(username_hash, 'search_log.json')
        self.favorite_movies_file = os.path.join(username_hash, 'favorite_movies.json')
        self.file_handler = SearchFileHandler(key)
        self.file_handler.create_directory(os.path.dirname(self.search_log_file))
        self.file_handler.create_directory(os.path.dirname(self.favorite_movies_file))

    def run(self):
        while True:
            self.display_menu()
            choice = input('Enter the number of your choice: ')

            if choice == '1':
                self.search_movie()
            elif choice == '2':
                self.view_search_log()
            elif choice == '3':
                self.view_favorite_movies()
            elif choice == '4':
                print("Logging out. Goodbye!")
                break
            else:
                print("Invalid choice. Please choose a valid option.")

    def display_menu(self):
        print('Choose action from below')
        print('1. Search a movie')
        print('2. View my search history')
        print('3. View my favorite movies')
        print('4. Log out')

    def search_movie(self):
        name = input("Enter a movie or TV show title to search (or 'exit' to quit): ").strip()

        if name.lower() == 'exit':
            print("Exiting the movie search app. Goodbye!")
            return

        try:
            query = {"title": name, "limit": "20", "sortArg": "moviemeter,asc"}
            search_result = self.imdb_api.search_movies(query)

            if 'results' in search_result:
                self.display_search_result(search_result['results'])
                self.log_search(name)  # Log the search
            else:
                print("No results found.")

        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def display_search_result(self, results):
        print("\nSearch Results:")
        for i, result in enumerate(results, start=1):
            title = result.get('title', 'N/A')
            year = result.get('year', 'N/A')
            print(f"{i}. Movie: {title}, Year: {year}")

        selected_movie_index = input(
            "Enter the number of the movie to add to your favorite movies (or 'back' to go back): ")
        if selected_movie_index.lower() != 'back':
            try:
                selected_movie = results[int(selected_movie_index) - 1]
                self.add_to_favorite_movies(selected_movie)
            except (ValueError, IndexError) as e:
                print(f"Error: {e}. Please enter a valid number.")

    def add_to_favorite_movies(self, movie):
        new_favorite_movie = {
            'title': movie.get('title', 'N/A'),
            'year': movie.get('year', 'N/A'),
            'id': movie.get('id', 'N/A')
            # Add more details as needed
        }

        self.file_handler.write_json(self.favorite_movies_file, new_favorite_movie)

        print(f"{new_favorite_movie['title']} added to favorite movies!")

    def log_search(self, search_query):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {search_query}\n"
        self.file_handler.write_json(self.search_log_file, log_entry)

    def view_search_log(self):
        search_log = self.file_handler.read_json(self.search_log_file)

        if search_log:
            print("\nSearch Log:")
            for i, entry in enumerate(search_log, start=1):
                print(f"{i}. {entry.strip()}")
        else:
            print("Search log is empty.")

    def view_favorite_movies(self):
        favorite_movies = self.file_handler.read_json(self.favorite_movies_file)

        if favorite_movies:
            print("\nFavorite Movies:")
            for i, movie in enumerate(favorite_movies, start=1):
                print(f"{i}. {movie['title']} ({movie['year']})")
        else:
            print("No favorite movies yet.")
