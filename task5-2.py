import requests
import re
import collections
import concurrent.futures
import matplotlib.pyplot as plt

# Функція для завантаження тексту з URL
def fetch_text(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

# Функція Map для розбиття тексту на слова
def map_words(text):
    words = re.findall(r'\b\w+\b', text.lower())  # Приводимо до нижнього регістру
    return collections.Counter(words)

# Функція Reduce для об'єднання частот
def reduce_counts(counts_list):
    total_counts = collections.Counter()
    for counts in counts_list:
        total_counts.update(counts)
    return total_counts

# Візуалізація топ-10 найчастіше вживаних слів
def visualize_top_words(word_counts):
    top_words = word_counts.most_common(10)
    words, counts = zip(*top_words)
    
    plt.figure(figsize=(10, 5))
    plt.barh(words[::-1], counts[::-1], color='skyblue')
    plt.xlabel("Frequency")
    plt.ylabel("Words")
    plt.title("Top 10 Most Frequent Words")
    plt.show()

# Основна функція
def main():
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"  # Фіксований URL
    text = fetch_text(url)
    
    # Використання багатопотоковості для MapReduce
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(map_words, text)
        word_counts = future.result()
    
    # Візуалізація результатів
    visualize_top_words(word_counts)

if __name__ == "__main__":
    main()
