from flask import Flask
from .routes import blue
from .config import DevelopmentConfig
from .factory import create_app

app = create_app(__name__, blue, DevelopmentConfig)

def main():
    app.run(debug=False, host='0.0.0.0', port=9888)

if __name__ == "__main__":
    main()


    
