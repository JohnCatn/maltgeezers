Based on blog at https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

## Update Database
The database is controlled by the models and the flask-sqlalchemy and flask-migrate libraries, to update perform the following
* Update models.py to add a new Class for new tables or edit columns in existing classes/tables
* in a command prompt run
flask db migrate -m "change comment"
* If this is OK then apply the change to the Database
flask db upgrade
If you make a mistake then use "flask db downgrade" to roll back

## Deployment to Dreamhost
https://mattcarrier.com/flask-dreamhost-setup/


## Useful info
https://pythonhosted.org/Flask-Bootstrap/basic-usage.html

##Env config
Place a file called .env in the root of your project directory populated as below to set up environmnet variable:
'''
SECRET_KEY = 'you-will-never-guess'
DATABASE_URL = 'SQL ALCHEMEY Database connection string'
MAIL_SERVER = 'YOUR_MAIL_SERVER'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USERNAME = 'YOUR_MAIL_USERNAME'
MAIL_PASSWORD = 'YOUR_MAIL_PASSWORD'
ADMINS = ['admin@maltgeezers.org']
POSTS_PER_PAGE = 25
ENVIRONMENT = 'development' # Need to set this manually as needed before .env loads


# Flask-User settings
    USER_APP_NAME = 'YOUR_APPNAME'
    USER_ENABLE_EMAIL = True  
    USER_ENABLE_USERNAME = True
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = 'noreply@maltgeezers.org'
    USER_ENABLE_CONFIRM_EMAIL = False

#GA
  ENABLE_GA = True
  GA_TRACKING_CODE = "UA-121303615-1"

#TWITTER
TWITTER_CONSUMER_KEY        = 'YOUR_CONSUMER_KEY'
TWITTER_CONSUMER_SECRET     = 'YOUR_TWITTER_CONSUMER_SECRET'
TWITTER_ACCESS_TOKEN        = 'YOur_TWITTER_ACCESS_TOKEN'
TWITTER_ACCESS_TOKEN_SECRET = 'YOUR_TWITTER_ACCESS_TOKEN_SECRET'

#Facebook
FB_APP_ID = 'YOUR_FB_APP_ID'
FB_APP_SECRET = 'YOUR_FB_APP_SECRET'

'''
