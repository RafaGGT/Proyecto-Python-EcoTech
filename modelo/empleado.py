from modelo import bd
from modelo import usuario as us 

class Empleado(us.Usuario):
    def __init__(self, nombreDeUsuario=None, contrasena=None, rol=None,
             nombre=None, direccion=None, telefono=None, fechaInicio=None, salario=None):
        super().__init__(nombreDeUsuario, contrasena, rol)
        # Inicializa atributos internos (evita el AttributeError)
        self._nombre = None
        self._direccion = None
        self._telefono = None
        self._fechaInicio = None
        self._salario = None

        # Luego usa los setters normalmente
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.fechaInicio = fechaInicio
        self.salario = salario

    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor  # <-- CORRECTO

    @property
    def direccion(self):
        return self._direccion
    
    @direccion.setter
    def direccion(self, valor):
        self._direccion = valor

    @property
    def telefono(self):
        return self._telefono
    
    @telefono.setter
    def telefono(self, valor):
        self._telefono = valor

    @property
    def fechaInicio(self):
        return self._fechaInicio

    @fechaInicio.setter
    def fechaInicio(self, valor):
        self._fechaInicio = valor

    @property
    def salario(self):
        return self._salario
    
    @salario.setter
    def salario(self, valor):
        self._salario = valor

    def crearUsuario(self, conexion):
        # Primero registra como Usuario
        super().crearUsuario(conexion)
        # Luego registra los datos de Empleado
        cursor = conexion.conexion.cursor()
        consulta = """
            INSERT INTO Empleados (id, nombre, direccion, numeroTelefono, fechaInicioContrato, salario)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (self.id, self.nombre, self.direccion, self.telefono, self.fechaInicio, self.salario)
        cursor.execute(consulta, valores)
        conexion.conexion.commit()
        cursor.close()

    def iniciarSesion(self, conexion):
        if super().iniciarSesion(conexion):
            cursor = conexion.conexion.cursor()
            consulta = "SELECT nombre, direccion, numeroTelefono, fechaInicioContrato, salario FROM Empleados WHERE id=%s"
            cursor.execute(consulta, (self.id,))
            resultado = cursor.fetchone()
            if resultado:
                self.nombre, self.direccion, self.telefono, self.fechaInicio, self.salario = resultado
                cursor.close()
                return True
            cursor.close()
        return False   

# --- Modelo: Empleado (hereda de Usuario) ---
    def modificarUsuario(self, conexion, nuevo_nombreUsuario=None, nueva_contrasena=None, nuevo_rol=None,
                        nuevo_nombre=None, nueva_direccion=None, nuevo_telefono=None, nueva_fechaInicio=None, nuevo_salario=None):
        # Primero modifica los campos del usuario base
        super().modificarUsuario(conexion, nuevo_nombreUsuario, nueva_contrasena, nuevo_rol)
        # Luego modifica los campos propios de Empleado
        cursor = conexion.conexion.cursor()
        if nuevo_nombre:
            self.nombre = nuevo_nombre
        if nueva_direccion:
            self.direccion = nueva_direccion
        if nuevo_telefono:
            self.telefono = nuevo_telefono
        if nueva_fechaInicio:
            self.fechaInicio = nueva_fechaInicio
        if nuevo_salario:
            self.salario = nuevo_salario
        consulta = """
            UPDATE Empleados
            SET nombre=%s, direccion=%s, numeroTelefono=%s, fechaInicioContrato=%s, salario=%s
            WHERE id=%s
        """
        valores = (self.nombre, self.direccion, self.telefono, self.fechaInicio, self.salario, self.id)
        cursor.execute(consulta, valores)
        conexion.conexion.commit()
        cursor.close()
        return True
