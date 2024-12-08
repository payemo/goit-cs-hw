import requests
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import string
import matplotlib.pyplot as plt

def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status() # Check errors
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    
def map_function(word):
    return word, 1

def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

def map_reduce(text):
    text = remove_punctuation(text)
    words = text.split()

    # Map phase
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Shuffle phase
    shuffled_values = shuffle_function(mapped_values)

    # Reduction phase
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

def visualize_top_words(word_count, top_n):
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:top_n]

    words, count = zip(*sorted_words)

    plt.barh(words, count, color='skyblue')
    plt.xlabel("Frequency")
    plt.ylabel("Words")
    plt.title("Top {} Most Frequent Words".format(top_n))
    plt.gca().invert_yaxis()
    plt.show()

if __name__ == '__main__':
    parser = ArgumentParser(description="Analyze word frequencies in a text from a URL using MapReduce.")
    parser.add_argument("--url", type=str, required=True, help="Text file's URL.")
    parser.add_argument("--top_n", type=int, default=10, help="Number of top frequent words to display.")

    args = parser.parse_args()

    text = get_text(args.url)

    if text:
        word_count = map_reduce(text)
        visualize_top_words(word_count, args.top_n)
    else:
        print("Unable to fetch a content.")
