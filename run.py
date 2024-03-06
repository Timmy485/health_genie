from os import environ
from app import app

DEBUG = environ.get("DEBUG", "True")
HOST = environ.get("HOST", "0.0.0.0")
PORT = int(environ.get("PORT", 5000))


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)