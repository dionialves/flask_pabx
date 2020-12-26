from app import db


class Extension(db.Model):
    __tablename__ = "extension"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    extension = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, name, extension, password):
        self.name = name
        self.extension = extension
        self.password = password

    def __repr__(self):
        return "Extension %r" % self.name