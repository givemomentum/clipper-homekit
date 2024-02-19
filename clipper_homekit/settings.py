import os


file_current_path = os.path.abspath(__file__)
file_dir_path = os.path.dirname(file_current_path)
BASE_DIR = os.path.dirname(file_dir_path)
print(BASE_DIR)
