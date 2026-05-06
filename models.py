from flask_login import UserMixin

# Fake DB
users_db = {}
#User class for authentication
class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.password = password