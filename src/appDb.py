from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = None
login_manager = None

def initDb(app):
    """initialize connection string
    Args:
        app ([type]):  app from flask  
    """
    global db
    global login_manager
    db = SQLAlchemy(app)
    login_manager = LoginManager(app)

    return {'db': db, 'login_manager':login_manager}
    
def getDbFromApp():
    
    global db
    return db

def getLoginManager():
    
    global login_manager
    return login_manager

