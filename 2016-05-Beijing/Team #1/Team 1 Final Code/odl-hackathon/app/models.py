from . import db


class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), unique=True)
    vdc_id = db.Column(db.Integer, nullable=False)
    check_in_mac_addr = db.Column(db.VARCHAR(255), nullable=True)

    def __init__(self, user_name, vdc_id):
        self.user_name = user_name
        self.vdc_id = vdc_id

    def __repr__(self):
        return '<Account %r>' % self.user_name