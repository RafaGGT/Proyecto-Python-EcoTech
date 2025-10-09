from modelo import bd

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
        consulta = "INSERT INTO Usuario (nombreUsuario, contrasena, rol) VALUES (%s, %s, %s)"
        valores = (self.nombreDeUsuario, self.contrasena, self.rol)
        cursor.execute(consulta, valores)
        conexion.conexion.commit()
        self.id = cursor.lastrowid  # guarda el id generado
        cursor.close()

    def iniciarSesion(self, conexion):
        cursor = conexion.conexion.cursor()
        consulta = "SELECT nombreUsuario, contrasena, rol FROM Usuario WHERE nombreUsuario = %s AND contrasena = %s"
        valores = (self.nombreDeUsuario, self.contrasena)
        cursor.execute(consulta, valores)
        usuario = cursor.fetchone()  # ✅ Leer resultado
        cursor.close()
        if usuario:
            self.id = usuario[0]
            self.rol = usuario[2]
            return True 
        else:
            return False  