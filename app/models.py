from app import db, login_manager
from flask_login import UserMixin
from app import bcrypt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    valor = db.Column(db.Integer,nullable=False,default=5000)
    itens = db.relationship('Items',backref='dono_user',lazy=True)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    @property
    def formataValor(self):
        if len(str(self.valor)) >= 4:
            return f"R$ {str(self.valor)[:-3]},  {str(self.valor)[-3:]}"
        else:
            return f"R$ {self.valor}"
    
    @property
    def passwordcrip(self):
        return self.passwordcrip

    @passwordcrip.setter
    def passwordcrip(self,password_txt):
        self.password_hash = bcrypt.generate_password_hash(password_txt).decode('utf-8')

    def check_password(self,password_rcript):
        return bcrypt.check_password_hash(self.password_hash,password_rcript)


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    preco = db.Column(db.String(64), index=True)
    cod_barra = db.Column(db.String(128), index=True, unique=True)
    description = db.Column(db.String(128))
    dono = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item: {self.name}'