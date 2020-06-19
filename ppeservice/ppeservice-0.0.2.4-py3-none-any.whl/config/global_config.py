class DevelopmentConfig(): 
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1/User"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MIGRATE = True

class ProductionConfig(): 
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1/User"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MIGRATE = False