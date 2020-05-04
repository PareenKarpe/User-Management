from flask import Flask
import logging
import statsd




app = Flask(__name__)

logging.basicConfig(filename='demo2.log', level=logging.DEBUG)


@app.route('/')
def hello_world():

    app.logger.info('Processing default request1')
    return 'Hello World!'
def h():
    print("jjjjjj")


@app.route('/h7')
def hello_world7():

    h()
    return 'Hello World7!'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)