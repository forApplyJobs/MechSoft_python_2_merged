from Server.models import User
from Server import db
from Server import app

       
with app.app_context():
    db.create_all()
    user=User(firstname="bilka",lastname="bilkasoy",email="bilka@bilka.com")
    user2=User(firstname="bilka2",lastname="bilkasoy2",email="bilka2@bilka2.com")
    user3=User(firstname="bilka3",lastname="bilkasoy3",email="bilka3@bilka3.com")
    db.session.add_all([user,user2,user3])
    db.session.commit()

