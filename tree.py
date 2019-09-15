import time, os, re
from stat import *

'''
Future implementation

if filename/folder does not contain year information
    scan string/movie using internet and get year of release to improve success rate of files ready to move
'''

LIST_OF_DIRECTORIES_TO_SCAN = ['E:\Misc_Movies']
YEAR_REGEX = "(\d{4})"



def search_string_return_file_path(file_path, string):
    year_match = re.search(YEAR_REGEX, string)
    if year_match is not None:
        return [f'{file_path}/{string}', year_match.group()]
    return [None, None]


def scan_dir(directory = LIST_OF_DIRECTORIES_TO_SCAN[0]):
    root_folders_scanned = []
    name_new_dir = f'{LIST_OF_DIRECTORIES_TO_SCAN[0]}\sorted_year_movies'

    for root, dirs, files in os.walk(directory):
        # print(dirs)
        for dir in dirs:
            # if folder contains year move into new directory of year.
            path_string_found, year = search_string_return_file_path(root, dir)
            if path_string_found:
                new_dir_to_create = f'{name_new_dir}\{year}'
                create_folder_path(new_dir_to_create)

                # Move files to respective year folder
                identical = f'{name_new_dir}/{year}'
                if identical == path_string_found:
                    continue
                move_to_folder(new_dir_to_create, path_string_found)


            # if folder did not contain year information. Scan files and move to directory if year in string
            if name_new_dir in root:
                continue
            if root in root_folders_scanned:
                continue

            root_folders_scanned.append(root)
            for file in files:
                # print(file)
                path_string_found, year = search_string_return_file_path(root, file)
                if path_string_found:
                    new_dir_to_create = f'{name_new_dir}\{year}'
                    create_folder_path(new_dir_to_create)

                    # Move files to respective year folder
                    move_to_folder(new_dir_to_create, path_string_found)


def get_information_on_file(filepath):
    try:
        stats = os.stat(filepath)
    except IOError:
        print(f'Failed to get info on file {filepath}')
    else:
        # print(stats[ST_SIZE])
        # print(time.asctime(time.localtime(stats[ST_MTIME])))
        pass


def create_folder_path(path_folder_to_create):
    if not os.path.exists(path_folder_to_create):
        os.makedirs(path_folder_to_create)

def move_to_folder(folder_path, file_path):
    new_path = f'{folder_path}/{file_path.split("/")[-1]}'
    if new_path != file_path:
        print(f'New path = {new_path} : file_path = {file_path}')
        os.rename(file_path, new_path)
    # print(f'Path Already exist = {new_path}')


print(scan_dir())
