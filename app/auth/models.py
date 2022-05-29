from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db 

class User(UserMixin):
    def __init__(self, name ,email, password, is_admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def get_id(self):
        return self.email
    
    @classmethod # usuario para mantener en la sesion
    def get_by_email(self,email):
        print("sql:",'{}'.format(email))
        data = db.fetch_one('SELECT * FROM encuestado_prueba WHERE correo = (%s);',(str(email),))
        if data is None:
            return None
        else:
            return User(data[1],data[0],None,True) # ESTE True dsps tiene que salir es para que se tome como ADMIN

    def insert_user(self):
        db.execute('INSERT INTO encuestado_prueba(correo,nombre,hash_contraseña) VALUES(%s,%s,%s)',(self.email,self.name,self.password))

    def set_password(self,password):
        self.password =  generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def select_user(self,email): # este es para seleccionar un usuario
        user = db.fetch_one('SELECT * FROM encuestado_prueba WHERE correo = (%s);', (str(email),))
        print("user:",user)
        if user is not None:
            return User(user[1],user[0],user[2])
        return None

    def __repr__(self):
        return '<User {}>'.format(self.email)