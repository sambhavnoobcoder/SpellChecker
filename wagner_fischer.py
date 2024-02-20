import time
import re


def load_dictionary(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]


def wagner_fischer(s1, s2):
    len_s1, len_s2 = len(s1), len(s2)
    if len_s1 > len_s2:
        s1, s2 = s2, s1
        len_s1, len_s2 = len_s2, len_s1

    current_row = range(len_s1 + 1)
    for i in range(1, len_s2 + 1):
        previous_row, current_row = current_row, [i] + [0] * len_s1
        for j in range(1, len_s1 + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if s1[j - 1] != s2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[len_s1]


def spell_check(word, dictionary):
    suggestions = []

    for correct_word in dictionary:
        distance = wagner_fischer(word, correct_word)
        suggestions.append((correct_word, distance))

    suggestions.sort(key=lambda x: x[1])
    return suggestions[0][0]  # return the closest correct word


def spell_check_sentence(sentence, dictionary):
    # Tokenize the sentence into words
    words = re.findall(r'\b\w+\b', sentence)

    corrected_sentence = []
    for word in words:
        if word.lower() not in dictionary:  # Check if the word is misspelled
            corrected_word = spell_check(word.lower(), dictionary)
            corrected_sentence.append(corrected_word)
        else:
            corrected_sentence.append(word)

    return ' '.join(corrected_sentence)


# Example Usage
dictionary = load_dictionary("words.txt")
sentence = "Ths is a sentnce with some misspeled words."

start_time = time.time()
corrected_sentence = spell_check_sentence(sentence, dictionary)
end_time = time.time()

response_time = (end_time - start_time) * 1000  # in milliseconds

print("Original Sentence:", sentence)
print("Corrected Sentence:", corrected_sentence)
print(f"Response Time: {response_time:.2f} milliseconds")

words_per_second = len(sentence.split()) / (end_time - start_time)
response_time_per_1000_words = (response_time / len(sentence.split())) * 1000

print(f"Response Time per 1000 Words: {response_time_per_1000_words:.2f} milliseconds")
