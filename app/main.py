from flask import Flask
from core.SpellChecker import SpellChecker
from core.constants import keyboard_letters
from core.Edit import EditType, Edit

app = Flask(__name__)

service_armenian = SpellChecker("am")
service_english = SpellChecker("en")

letters_armenian = set(keyboard_letters["am"])
letters_english = set(keyboard_letters["en"])

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/correction/<string:string>')
def correct_string(string):
    
    if string in letters_armenian:
        service = service_armenian
    else:
        service = service_english
        
    candidates = service.candidates(string.lower())
    candidates_words = [edit.edit.capitalize() for edit in candidates]
    return candidates_words[:3], 200