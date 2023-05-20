import nltk
from nltk.util import ngrams

class NGramModel:
    
    def __init__(self, language: str, override_file = None):
        if override_file:
            file_to_open = override_file
        else:
            file_to_open = f'texts/big_{language}.txt'
            
        with open(file_to_open, "r") as file:
            corpus = file.read()
            
        tokenized_text = nltk.word_tokenize(corpus)
        self.trigrams = list(ngrams(tokenized_text, 3))
        
    def predict_next_word(self, sentence, possible_words):
        
        probabilities = self.get_probabilities(sentence, possible_words)
        
        return max(probabilities, key=probabilities.get)
    
    def get_probabilities(self, sentence, possible_words):
        tokenized_sentence = nltk.word_tokenize(sentence)
        w1, w2 = tokenized_sentence[-2:]  # Get the last two words from the sentence

        probabilities = {word: 0 for word in possible_words}
        for trigram in self.trigrams:
            if trigram[:2] == (w1, w2) and trigram[2] in possible_words:
                word = trigram[2]
                probabilities[word] = probabilities.get(word, 0) + 1

        total_count = sum(probabilities.values())
        probabilities = {word: count / (total_count + 1) for word, count in probabilities.items()}

        return probabilities

