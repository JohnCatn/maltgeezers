import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = os.environ.get('ADMINS')
    POSTS_PER_PAGE = int(os.environ.get('POSTS_PER_PAGE') or 25)

    # Flask-User settings
    USER_APP_NAME = os.environ.get('USER_APP_NAME')      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True        # Enable email authentication
    USER_ENABLE_USERNAME = True    # Disable username authentication
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = os.environ.get('USER_EMAIL_SENDER_EMAIL')
    USER_ENABLE_CONFIRM_EMAIL = False

    #GA Tracking
    ENABLE_GA = os.environ.get('ENABLE_GA')
    GA_TRACKING_CODE = os.environ.get('GA_TRACKING_CODE')

    #Twitter
    TWITTER_CONSUMER_KEY        = os.environ.get('TWITTER_CONSUMER_KEY')
    TWITTER_CONSUMER_SECRET     = os.environ.get('TWITTER_CONSUMER_SECRET')
    TWITTER_ACCESS_TOKEN        = os.environ.get('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

    #facebook
    FB_APP_ID = os.environ.get('FB_APP_ID')
    FB_APP_SECRET = os.environ.get('FB_APP_SECRET')
