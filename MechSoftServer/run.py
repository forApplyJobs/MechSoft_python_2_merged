from Server.models import User
from Server import app
import Server.routes as routes

app.run(debug=True)


# from Server import db
# app.app_context().push()
# db.session.add(User(firstname="bilka2",lastname="bilka2surname",email="bilka2@bilka2.com"))
# db.session.commit()
