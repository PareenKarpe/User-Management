from flask import Flask
app = Flask(__name__)


@app.route('/j777777')
def hello():
    return "Hello World7777!"

if __name__ == '__main__':
    app.run()
