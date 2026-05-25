from flask import Flask

app = Flask(__name__)

from routes.chat import *

if __name__ == '__main__':

    app.run(debug=True)