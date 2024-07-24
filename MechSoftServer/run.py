from Server.models import User
from Server import app
import Server.routes as routes
from sqlalchemy_utils import database_exists
from Server import db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
app.run()



    