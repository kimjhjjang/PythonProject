import pathlib
import csv
import logging


def make_path_recursive(path_name):
    pathlib.Path(path_name).mkdir(parents=True, exist_ok=True)


def write_list_to_csv(file_path, data):

    path = pathlib.Path(file_path)
    
    # 디렉토리가 없을 경우 디렉토리 생성
    directory = path.parent
    make_path_recursive(directory)

    try:
        with open(file_path, mode='w', newline='\n', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        logging.info(f"CSV file has been successfully created: {file_path}")
    except Exception as e:
        logging.fatal(f"Error occurred while generating the CSV file: {e}")
