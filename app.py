from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/correction/<string:string>')
def correct_string(string):
    return string, 200