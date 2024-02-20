import time
import re
from collections import Counter

def load_dictionary(file_path):
    with open(file_path, 'r') as file:
        return set(line.strip().lower() for line in file)

def edits1(word):
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def known(words, dictionary):
    return set(w for w in words if w in dictionary)

def spell_check(word, dictionary):
    candidates = (known([word], dictionary) or known(edits1(word), dictionary) or [word])
    return max(candidates, key=dictionary.get)

def spell_check_sentence(sentence, dictionary):
    words = re.findall(r'\b\w+\b', sentence.lower())
    corrected_sentence = []
    for word in words:
        if word not in dictionary:
            corrected_word = spell_check(word, dictionary)
            corrected_sentence.append(corrected_word)
        else:
            corrected_sentence.append(word)
    return ' '.join(corrected_sentence)

def build_dictionary(file_path):
    with open(file_path, 'r') as file:
        words = re.findall(r'\b\w+\b', file.read().lower())
        return Counter(words)

dictionary = build_dictionary("words.txt")
sentence = "Ths is a sentnce with some misspeled words."

start_time = time.time()
corrected_sentence = spell_check_sentence(sentence, dictionary)
end_time = time.time()

response_time = (end_time - start_time) * 1000

print("Original Sentence:", sentence)
print("Corrected Sentence:", corrected_sentence)
print(f"Response Time: {response_time:.2f} milliseconds")

words_per_second = len(sentence.split()) / (end_time - start_time)
response_time_per_1000_words = (response_time / len(sentence.split())) * 1000

print(f"Response Time per 1000 Words: {response_time_per_1000_words:.2f} milliseconds")
