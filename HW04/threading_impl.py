import threading
from pathlib import Path
from collections import defaultdict
import time

from utils import boyer_moore_search

BUFFER_SIZE = 1024 * 1024 # 1MB buffer

def search_keywords_in_files(file_paths, keywords, result_dict, lock):
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                while True:
                    content = file.read(BUFFER_SIZE)
                    if not content:
                        break

                    for keyword in keywords:
                        if boyer_moore_search(content, keyword):
                            with lock:
                                result_dict[keyword].append(str(file_path))
                            break # No need to check other keywords for this file
        except Exception as ex:
            print(f"Error reading file {file_path}: {ex}")

def main_threading(file_paths, keywords):
    num_threads = min(4, len(file_paths))
    threads = []
    results = defaultdict(list)
    lock = threading.Lock()

    # Split file evenly
    chunk_size = (len(file_paths) + num_threads - 1) // num_threads

    start_time = time.time()
    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size if (i + 1) * chunk_size < len(file_paths) else len(file_paths)
        thread = threading.Thread(target=search_keywords_in_files,
                                  args=(file_paths[start:end], keywords, results, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Threading execution time: {end_time - start_time:.2f} seconds")
    return dict(results)

if __name__ == '__main__':
    folder_path = input("Enter the folder path containing text file: ").strip()
    keywords = input("Enter keywords separated by commas: ").strip().split(',')
    file_paths = list(Path(folder_path).glob("*.txt"))
    results = main_threading(file_paths, keywords)
    print(results)