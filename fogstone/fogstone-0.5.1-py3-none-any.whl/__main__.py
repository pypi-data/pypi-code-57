import os

from fogstone.app import create_app

host = os.getenv('HOST', "127.0.0.1")
port = os.getenv('PORT', "5000")
debug = 'DEBUG' in os.environ

app = create_app()


def run():
    app.run(debug=debug, host=host, port=int(port))


if __name__ == '__main__':
    run()
