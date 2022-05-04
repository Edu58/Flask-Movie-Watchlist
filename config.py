import os


class Config:
    """
    General configuration parent class
    """
    MOVIE_API_BASE_URL = 'https://api.themoviedb.org/3/movie/{}?api_key={}'
    MOVIE_API_KEY = os.environ.get('MOVIE_API_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://ed:ed@localhost/watchlist'
    UPLOADED_PHOTOS_DEST = 'app/static/photos'
    MAIL_SERVER = 'smtp.google.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    Mail_password = os.environ.get("MAIL_PASSWORD")


class ProdConfig(Config):
    """
    Production configuration child class
     Args:
        Config: The parent configuration class with General configuration settings
    """
    DEBUG = False


class DevConfig(Config):
    """
    Development configuration child class
     Args:
        Config: The parent configuration class with General configuration settings
    """
    DEBUG = True


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://ed:ed@localhost/watchlist_test'
    TESTING = True


config_options = {
    'development': DevConfig,
    'production': ProdConfig,
    'testing': TestConfig
}
