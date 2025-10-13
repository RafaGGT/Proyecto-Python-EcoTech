
class Proyecto:
    def __init__(self, id=None, nombre=None, descripcion=None, fechaInicio=None):
        self._id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fechaInicio = fechaInicio

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        self._id = valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = valor

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        self._descripcion = valor

    @property
    def fechaInicio(self):
        return self._fechaInicio

    @fechaInicio.setter
    def fechaInicio(self, valor):
        self._fechaInicio = valor
    
    def crearProyecto(self, conexion):
        cursor = conexion.conexion.cursor()
        consulta = """
        INSERT INTO Proyectos (nombre, descripcion, fechaInicio)
        VALUES (%s, %s, %s)
        """
        valores = (self.nombre, self.descripcion, self.fechaInicio)
        cursor.execute(consulta, valores)
        conexion.commit()
    
    @staticmethod
    def listarProyectos(self, conexion):
        cursor = conexion.cursor()
        consulta = "SELECT id, nombre, descripcion, fechaInicio FROM Proyectos"
        cursor.execute(consulta)
        resultado = cursor.fetchall()
        cursor.close()
        