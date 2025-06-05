from collections import defaultdict
import math
import re


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zа-яё\s]', '', text)
    return text


def calculate_tf(text):
    words = preprocess_text(text).split()
    total_words = len(words)
    tf = defaultdict(int)

    for word in words:
        tf[word] += 1

    return {word: count / total_words for word, count in tf.items()}


def calculate_idf(text, corpus):
    words = set(preprocess_text(text).split())
    doc_freq = defaultdict(int)
    total_docs = len(corpus) + 1

    for doc in corpus:
        doc_words = set(preprocess_text(doc).split())
        for word in words:
            if word in doc_words:
                doc_freq[word] += 1

    return {word: math.log(total_docs / (doc_freq.get(word, 0) + 1) + 1)
            for word in words}
