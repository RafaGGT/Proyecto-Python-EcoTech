from modelo import bd
from modelo import usuario as us 

class Empleado(us.Usuario):
    def __init__(self, nombreDeUsuario, contrasena, rol, nombre, direccion, telefono, fechaInicio, salario):
        super().__init__(nombreDeUsuario, contrasena, rol)
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
        if not valor or valor.strip() == "":
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor

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
        
