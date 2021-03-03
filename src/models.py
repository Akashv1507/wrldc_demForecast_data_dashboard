from flask_login import login_manager
from src.appDb import getDbFromApp, getLoginManager
from flask_login import UserMixin


db = getDbFromApp()
login_manager = getLoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# userMixin for methods isAuthenticated() and 3 other methods
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    # how it show when you do User.query.all()
    def __repr__(self):
         return f"User('{self.username}', '{self.email}')"