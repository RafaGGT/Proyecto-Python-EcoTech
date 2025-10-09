from modelo.empleado import Empleado

class Administrador(Empleado):
    def __init__(self, nombreDeUsuario, contrasena, rol, nombre, direccion, telefono, fechaInicio, salario):
        super().__init__(nombreDeUsuario, contrasena, rol, nombre, direccion, telefono, fechaInicio, salario)

    def crearUsuario(self, conexion):
        super().crearUsuario(conexion)
        cursor = conexion.conexion.cursor()
        consulta = "INSERT INTO Administrador (id) VALUES (%s)"
        valores = (self.id,)
        cursor.execute(consulta, valores)
        conexion.conexion.commit()
        cursor.close()