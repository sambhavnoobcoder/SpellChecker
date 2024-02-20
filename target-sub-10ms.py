import time
import re

def load_dictionary(file_path):
    with open(file_path, 'r') as file:
        return set(line.strip().lower() for line in file)

def edits1(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = {L + R[1:] for L, R in splits if R}
    transposes = {L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1}
    replaces = {L + c + R[1:] for L, R in splits for c in letters}
    inserts = {L + c + R for L, R in splits for c in letters}
    return set(deletes | transposes | replaces | inserts)

def build_candidates_dict(dictionary):
    candidates_dict = {}
    for word in dictionary:
        candidates = set()
        for edit in edits1(word):
            if edit in dictionary:
                candidates.add(edit)
        candidates_dict[word] = candidates
    return candidates_dict

def spell_check(word, candidates_dict, dictionary_freq):
    if word in dictionary_freq:
        return word
    if word in candidates_dict:
        return max(candidates_dict[word], key=lambda x: dictionary_freq.get(x, 1), default=word)
    return word

def spell_check_sentence(sentence, candidates_dict, dictionary_freq, word_pattern):
    return ' '.join(spell_check(word, candidates_dict, dictionary_freq) for word in word_pattern.findall(sentence.lower()))

def build_dictionary(file_path):
    with open(file_path, 'r') as file:
        words = re.findall(r'\b\w+\b', file.read().lower())
        return set(words)

def build_dictionary_freq(dictionary):
    return {word: 1 for word in dictionary}

def extract_unique_words(sentence):
    return set(re.findall(r'\b\w+\b', sentence.lower()))

dictionary = build_dictionary("words.txt")
dictionary_freq = build_dictionary_freq(dictionary)
candidates_dict = build_candidates_dict(dictionary)
word_pattern = re.compile(r'\b\w+\b')

start_time = time.time()

sentence = "Ths is a sentnce with some misspeled words."
corrected_sentence = spell_check_sentence(sentence, candidates_dict, dictionary_freq, word_pattern)

end_time = time.time()

response_time = (end_time - start_time) * 1000

print("Original Sentence:", sentence)
print("Corrected Sentence:", corrected_sentence)
print(f"Response Time: {response_time:.2f} milliseconds")

words_per_second = len(sentence.split()) / (end_time - start_time)
response_time_per_1000_words = (response_time / len(sentence.split())) * 1000

print(f"Response Time per 1000 Words: {response_time_per_1000_words:.2f} milliseconds")
