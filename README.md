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
