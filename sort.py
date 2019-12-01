import time, os, re
from stat import *

'''
Future implementation

if filename/folder does not contain year information
    scan string/movie using internet and get year of release to improve success rate of files ready to move
'''


class Directory:
    def __init__(self, list_directories=None):
        if list_directories is None:
            list_directories = 'D:/Louis/Movies'
        list_directories = os.path.abspath(list_directories)  # returns / as \
        self.LIST_OF_DIRECTORIES_TO_SCAN = list_directories
        self.YEAR_REGEX = '(\d{4})'

    def search_string_return_file_path(self, file_path, string):
        year_match = re.search(self.YEAR_REGEX, string)
        if year_match is not None:
            return [f'{file_path}/{string}', year_match.group()]
        return [None, None]

    @staticmethod
    def create_folder_path(path_folder_to_create):
        if not os.path.exists(path_folder_to_create):
            os.makedirs(path_folder_to_create)

    @staticmethod
    def move_to_folder(folder_path, file_path):
        new_path = f'{folder_path}/{file_path.split("/")[-1]}'
        if new_path != file_path:
            print(f'New path = {new_path} : file_path = {file_path}')
            os.rename(file_path, new_path)
        else:
            print(f'Path Already exist = {new_path}')

    def scan_dir(self):
        root_folders_scanned = []
        name_new_dir = f'{self.LIST_OF_DIRECTORIES_TO_SCAN}\sorted_year_movies'

        for root, dirs, files in os.walk(self.LIST_OF_DIRECTORIES_TO_SCAN):
            for cur_dir in dirs:
                # First scans folders in directory.
                # if folder contains year move into new directory of year.
                path_string_found, year = self.search_string_return_file_path(root, cur_dir)
                if path_string_found:
                    new_dir_to_create = f'{name_new_dir}\{year}'
                    try:
                        self.create_folder_path(new_dir_to_create)
                    except FileExistsError as e:
                        print(e)
                    # Move files to respective year folder
                    identical = f'{name_new_dir}/{year}'
                    if identical == path_string_found:
                        continue
                    self.move_to_folder(new_dir_to_create, path_string_found)

                # if folder did not contain year information. Scan files and move to directory if year in string
                if name_new_dir in root:
                    continue
                if root in root_folders_scanned:
                    continue

                root_folders_scanned.append(root)
                for file in files:
                    path_string_found, year = self.search_string_return_file_path(root, file)
                    if path_string_found:
                        new_dir_to_create = f'{name_new_dir}\{year}'
                        try:
                            self.create_folder_path(new_dir_to_create)
                        except FileExistsError as e:
                            print(e)
                        # Move files to respective year folder
                        self.move_to_folder(new_dir_to_create, path_string_found)


class Movie:
    def get_information_on_file(self, filepath):
        try:
            stats = os.stat(filepath)
        except IOError:
            print(f'Failed to get info on file {filepath}')
        else:
            # print(stats[ST_SIZE])
            # print(time.asctime(time.localtime(stats[ST_MTIME])))
            pass


if __name__ == "__main__":
    directory_movies = input('Enter Directory path to scan eg. C:/Movies/ \n')
    directory_destination = input('Enter Directory path to place sorted movies folders \n')

    working_directory = Directory(list_directories=directory_movies)
    working_directory.scan_dir()

