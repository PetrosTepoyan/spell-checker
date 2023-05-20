from flask import Flask
from core.SpellChecker import SpellChecker
from core.constants import keyboard_letters
from core.NGramModel import NGramModel

flask_app = Flask(__name__)

# ngram_model_armenian = NGramModel("am")
# print("NGramModel armenian ready")
ngram_model_english = NGramModel("en")
print("NGramModel english ready")

# service_armenian = SpellChecker("am")
# print("SpellChecker armenian ready")
service_english = SpellChecker("en")
print("SpellChecker english ready")

letters_armenian = set(keyboard_letters["am"])
letters_english = set(keyboard_letters["en"])

@flask_app.route('/')
def hello_world():
    return 'Hello world!'

@flask_app.route('/correction/<string:string>')
def correct_string(string):
    
    string = string.replace("_", " ")
    
    if string[0] in letters_armenian:
        service = service_armenian
        model = ngram_model_armenian
    else:
        service = service_english
        model = ngram_model_english
        
    last_word = string.split(" ")[-1]
    
    candidates = list(service.candidates(last_word.lower()))
    candidates.sort(key = lambda edit: edit.probability(), reverse = True)
    candidates_words = [edit.edit for edit in candidates]
    print(candidates_words)
    if len(string.split(" ")) > 2:
        candidates_words_probabilities = model.get_probabilities(string, candidates_words)
        candidates_words.sort(key = candidates_words_probabilities.get, reverse = True)
        print(candidates_words_probabilities)
        
    candidates_words = [word.capitalize() for word in candidates_words]
    
    return candidates_words[:3], 200