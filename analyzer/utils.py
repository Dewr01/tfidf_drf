from collections import defaultdict
import math
import re


def preprocess_text(text):
    """Convert to lowercase and remove non-alphabetic characters"""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text


def calculate_tf(text):
    """Calculate Term Frequency for words in text"""
    processed_text = preprocess_text(text)
    words = processed_text.split()

    tf = defaultdict(int)
    total_words = len(words)

    for word in words:
        tf[word] += 1

    # Normalize TF by total word count
    tf = {word: count / total_words for word, count in tf.items()}

    return tf


def calculate_idf(uploaded_text, corpus_texts):
    """Calculate Inverse Document Frequency for words"""
    uploaded_words = set(preprocess_text(uploaded_text).split())

    # Count in how many documents each word appears
    doc_freq = defaultdict(int)
    total_docs = len(corpus_texts) + 1  # +1 for the uploaded file

    for corpus_text in corpus_texts:
        corpus_words = set(preprocess_text(corpus_text).split())

        for word in uploaded_words:
            if word in corpus_words:
                doc_freq[word] += 1

    # Calculate IDF
    idf = {}
    for word in uploaded_words:
        # +1 in numerator and denominator to avoid division by zero
        idf[word] = math.log((total_docs + 1) / (doc_freq.get(word, 0) + 1)) + 1

    return idf
