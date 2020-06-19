from flask import Flask
from .routes import blue
from .config import DevelopmentConfig, ProductionConfig
from .factory import create_app

app, migrate, manager = create_app(appname=__name__, blueprint=blue, config=ProductionConfig)

def main():
    if app.config["MIGRATE"] == True:
        manager.run()
    else:
        app.run(debug=False, host='0.0.0.0', port=9888)


if __name__ == "__main__":
    main()
