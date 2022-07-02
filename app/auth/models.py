from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db 

class User(UserMixin):
    def __init__(self, name ,email, password, id = None,is_admin=False):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def get_id(self):
        return self.email
    
    @classmethod # usuario para mantener en la sesion
    def get_by_email(self,email):
        data = db.fetch_one('SELECT * FROM usuario WHERE correo = (%s);',(str(email),))
        print(data)
        is_admin = False
        if data is None:
            return None
        else:
            data_administrador = db.fetch_one('SELECT * FROM administrador WHERE id_usuario = (%s);',(str(data[0]),))
            if data_administrador is not None:
                is_admin = True
            #return User(data[1],data[0],None,is_admin) # ESTE True dsps tiene que salir es para que se tome como ADMIN
            return User(name = data[1],email  = data[0],password = None,id = data[0],is_admin = is_admin)
    
    @classmethod
    def select_user(self,email): # este es para seleccionar un usuario
        user = db.fetch_one('SELECT * FROM usuario WHERE correo = (%s);', (str(email),)) # verifica si existe el usuario
        if user is not None:

            data = db.fetch_one('SELECT * FROM administrador WHERE id_usuario = (%s);',(str(user[0]),)) # data administrador
            is_admin = True
            if data is None:                                                                            # si no es administrador
                data = db.fetch_one('SELECT * FROM encuestado WHERE id_usuario = (%s);',(str(user[0]),))# data encuestado
                is_admin = False

            return User(name = user[1],email = user[2], password = data[1], id = user[0] ,is_admin = is_admin)
        return None

    def insert_user(self):
        email_from_db = db.fetch_one('SELECT * FROM mails WHERE correo = (%s);',(str(self.email),))
        if email_from_db is None:
            db.execute('INSERT INTO mails(correo,suscrito) VALUES(%s,%s)',(str(self.email),False))
        
        #db.execute('INSERT INTO encuestado_prueba(correo,nombre,hash_contraseña) VALUES(%s,%s,%s)',(self.email,self.name,self.password))

        id_user = db.execute_returning('INSERT INTO usuario(id_usuario,nombre,correo) VALUES(DEFAULT,%s,%s) RETURNING id_usuario',(self.name,self.email))
        self.id = id_user[0]
        db.execute('INSERT INTO encuestado(id_usuario,hash_password) VALUES(%s,%s)',(id_user[0],self.password))
        #db.execute('INSERT INTO administrador(id_usuario,hash_password) VALUES(%s,%s)',(id_user[0],self.password))

    def set_password(self,password):
        self.password =  generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.id)