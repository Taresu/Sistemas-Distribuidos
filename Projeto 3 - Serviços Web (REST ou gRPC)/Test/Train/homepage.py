from flask import Flask

app = Flask(__name__)

def homepage():
    return 'Essa é a HomePage'

app.run()