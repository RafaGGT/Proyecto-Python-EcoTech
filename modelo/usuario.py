import bcrypt

class Usuario:
    def __init__(self, nombreDeUsuario, contrasena, rol=None):
        self._id = None 
        self.nombreDeUsuario = nombreDeUsuario
        self.contrasena = contrasena
        self.rol = rol

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        self._id = valor
    
    @property
    def nombreDeUsuario(self):
        return self._nombreDeUsuario
    
    @nombreDeUsuario.setter
    def nombreDeUsuario(self, valor):
        if not valor or valor.strip() == "":
            raise ValueError("El nombre de usuario no puede estar vacío.")
        self._nombreDeUsuario = valor
    
    @property
    def contrasena(self):
        return self._contrasena
    
    @contrasena.setter
    def contrasena(self, valor):
        if not valor or valor.strip() == "":
            raise ValueError("La contraseña no puede estar vacía.")
        self._contrasena = valor

    @property
    def rol(self):
        return self._rol
    
    @rol.setter
    def rol(self, valor):
        self._rol = valor
    
    def crearUsuario(self, conexion):
        cursor = conexion.conexion.cursor()
        hash_contrasena = bcrypt.hashpw(
            self.contrasena.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8') 
        consulta = "INSERT INTO Usuario (nombreUsuario, contrasena, rol) VALUES (%s, %s, %s)"
        valores = (self.nombreDeUsuario, hash_contrasena, self.rol)
        cursor.execute(consulta, valores)
        conexion.conexion.commit()
        self.id = cursor.lastrowid  # guarda el id generado
        cursor.close()

    def iniciarSesion(self, conexion):
        cursor = conexion.conexion.cursor()
        consulta = "SELECT id, nombreUsuario, contrasena, rol FROM Usuario WHERE nombreUsuario = %s"
        valores = (self.nombreDeUsuario,)
        cursor.execute(consulta, valores)
        usuario = cursor.fetchone()
        cursor.close()
        if usuario:
            id_db, nombre_db, hash_db, rol_db = usuario
        # Verificar la contraseña con bcrypt
            if bcrypt.checkpw(self.contrasena.encode('utf-8'), hash_db.encode('utf-8')):
                self.id = id_db
                self.nombreDeUsuario = nombre_db
                self.rol = rol_db
                return True
            else:
                print("Contraseña incorrecta.")
                return False
        else:
            print("Usuario no encontrado.")
            return False

    def modificarUsuario(self, conexion, nuevo_nombreUsuario=None, nueva_contrasena=None, nuevo_rol=None):
        cursor = conexion.conexion.cursor()
        if nuevo_nombreUsuario:
            self.nombreDeUsuario = nuevo_nombreUsuario
        if nueva_contrasena:
            self.contrasena = nueva_contrasena
            hash_contrasena = bcrypt.hashpw(self.contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        else:
            cursor.execute("SELECT contrasena FROM Usuario WHERE id=%s", (self.id,))
            hash_contrasena = cursor.fetchone()[0]

        if nuevo_rol:
            self.rol = nuevo_rol
        consulta = "UPDATE Usuario SET nombreUsuario=%s, contrasena=%s, rol=%s WHERE id=%s"
        valores = (self.nombreDeUsuario, hash_contrasena, self.rol, self.id)
        cursor.execute(consulta, valores)
        conexion.conexion.commit()
        cursor.close()
        return True
