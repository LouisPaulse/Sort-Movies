import os
import re
from api import OMBdApi


class Directory:
    def __init__(self, list_directories=None, api_key=None):
        list_directories = os.path.abspath(list_directories)  # returns / as \
        self.LIST_OF_DIRECTORIES_TO_SCAN = list_directories
        self.YEAR_REGEX = '(\d{4})'
        self.api_key = api_key

    def search_string_return_file_path(self, file_path, string):
        year_match = re.search(self.YEAR_REGEX, string)
        if year_match is not None:
            return [f'{file_path}/{string}', year_match.group(), string]
        return [None, None, string]

    @staticmethod
    def create_folder_path(path_folder_to_create):
        if not os.path.exists(path_folder_to_create):
            os.makedirs(path_folder_to_create)

    @staticmethod
    def move_to_folder(folder_path, file_path):
        new_path = f'{folder_path}/{file_path.split("/")[-1]}'
        if new_path != file_path:
            print(f'New path = {new_path} : file_path = {file_path}')
            try:
                os.rename(file_path, new_path)
            except FileExistsError as e:
                print(e)
        else:
            print(f'Path already exists = {new_path}')

    def create_and_move_to_year_folder(self, folder_to_move, destination_folder, year):
        new_dir_to_create = f'{destination_folder}\{year}'
        try:
            self.create_folder_path(new_dir_to_create)
        except FileExistsError as e:
            print(e)
        # Move to respective year folder
        identical = f'{destination_folder}/{year}'
        if identical != folder_to_move:
            self.move_to_folder(new_dir_to_create, folder_to_move)

    def scan_dir(self):
        root_folders_scanned = []
        name_new_dir = f'{self.LIST_OF_DIRECTORIES_TO_SCAN}\sorted_year_movies'

        for root, dirs, files in os.walk(self.LIST_OF_DIRECTORIES_TO_SCAN):
            for cur_dir in dirs:
                if name_new_dir in root:  # not to scan sorted folder
                    continue
                if root in root_folders_scanned:
                    continue

                # First scans folders in directory.
                # if folder contains year, move into new directory of year.
                path_string_found, year, movie_string = self.search_string_return_file_path(root, cur_dir)
                if path_string_found:
                    self.create_and_move_to_year_folder(path_string_found, name_new_dir, year)

                # if folder did not contain year information. Scan files and move to directory if year in string
                print(f'Now scanning: {root}')
                for file in files:
                    path_string_found, year, string = self.search_string_return_file_path(root, file)
                    movie_location = f'{root}/{string}'
                    cleaned_string = string[:-4]  # Strip format and .

                    if path_string_found:
                        path_string_found = path_string_found[:-4]
                        movie_folder_location = f'{root}\{cleaned_string}'
                        try:
                            self.create_folder_path(movie_folder_location)
                        except FileExistsError as e:
                            print(e)

                        self.move_to_folder(movie_folder_location, movie_location)
                        self.create_and_move_to_year_folder(path_string_found, name_new_dir, year)
                    else:
                        # Movies not in folders are placed in one containing its name and year

                        # Attempt to find movie information from api
                        movie_api = Movie(api_key=self.api_key)
                        movie_details = movie_api.get_movie_information(cleaned_string)
                        if movie_details is None:
                            print(f'Information not found for movie: {cleaned_string}')
                            continue

                        title, year, poster = movie_details

                        movie_folder_location = f'{root}\{title} ({year})'
                        try:
                            self.create_folder_path(movie_folder_location)
                        except FileExistsError as e:
                            print(e)

                        self.move_to_folder(movie_folder_location, movie_location)

                        self.create_and_move_to_year_folder(movie_folder_location, name_new_dir, year)
            root_folders_scanned.append(root)


class Movie:
    def __init__(self, api_key):
        self.ombd_api = OMBdApi(api_key)

    def search_movie_online(self, movie_name):
        response = self.ombd_api.search_by_title(movie_name)
        return response

    def get_movie_information(self, movie_title):
        response = self.search_movie_online(movie_title)
        if response['Response'] == 'False':
            print(response['Error'])
            return None

        title = response['Title'].replace(':', '')
        year = response['Year']
        poster = response['Poster']  # Poster link with image
        print(f'Title: {title} \n Year: {year} \n Poster: {poster}')

        return [title, year, poster]


if __name__ == "__main__":
    api_key = input('Enter OMBd API key \n')
    directory_movies = input('Enter Directory path to scan eg. C:/Movies/ \n')
    directory_destination = input('Enter Directory path to place sorted movies folders \n')

    working_directory = Directory(list_directories=directory_movies, api_key=api_key)
    working_directory.scan_dir()
