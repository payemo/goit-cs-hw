from multiprocessing import Process, Queue
from pathlib import Path
from collections import defaultdict
import time

def search_keywords_in_files(file_paths, keywords, queue):
    results = defaultdict(list)

    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                for keyword in keywords:
                    if keyword in content:
                        results[keyword].append(str(file_path))
        except Exception as ex:
            print(f"Error reading file {file_path}: {ex}")
    queue.put(results)

def main_multiprocessing(file_paths, keywords):
    num_processes = min(4, len(file_paths))
    processes = []
    queue = Queue()
    chunk_size = len(file_paths)

    start_time = time.time()
    for i in range(num_processes):
        start = i * chunk_size
        end = None if i == num_processes - 1 else (i + 1) * chunk_size
        process = Process(target=search_keywords_in_files,
                          args=(file_paths[start:end], keywords, queue))
        processes.append(process)
        process.start()

    results = defaultdict(list)
    for process in processes:
        process.join()

    while not queue.empty():
        partial_results = queue.get()
        for keyword, files in partial_results.items():
            results[keyword].extend(files)
    
    end_time = time.time()
    print(f"Multiprocessing execution time: {end_time - start_time:.2f} seconds")
    return dict(results)

if __name__ == '__main__':
    folder_path = input("Enter the folder path containing text files: ").strip()
    keywords = input("Enter keywords separated by commas: ").strip().split(',')
    file_paths = list(Path(folder_path).glob("*.txt"))
    results = main_multiprocessing(file_paths, keywords)
    print(results)