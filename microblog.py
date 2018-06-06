from app import create_app, db
from app.models import User, Country, Region, Brand, Type, Review

app = create_app('development')

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Country':Country,'Region':Region,'Brand':Brand,'Type':Type,'Review': Review}


app.run()
