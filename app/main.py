from flask import Flask
from app.SpellChecker import SpellChecker
from Edit import EditType, Edit

app = Flask(__name__)

service = SpellChecker()

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/correction/<string:string>')
def correct_string(string):
    candidates = service.candidates(string.lower())
    candidates_words = [edit.edit.capitalize() for edit in candidates]
    return candidates_words[:3], 200