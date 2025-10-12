from modelo import bd


class RegistroHoras:
    def __init__(self, id=None, horas_trabajadas=None, fecha=None, descripcion_tareas=None, id_empleado=None, id_proyecto=None):
        self.id = id
        self.horas_trabajadas = horas_trabajadas
        self.fecha = fecha
        self.descripcion_tareas = descripcion_tareas
        self.id_empleado = id_empleado
        self.id_proyecto = id_proyecto

    @staticmethod
    def obtener_reportes(conexion, id):
        cursor = conexion.conexion.cursor()
        consulta = "SELECT * FROM ReporteHoras WHERE idEmpleado=%s"
        cursor.execute(consulta)
        empleados = cursor.fetchall()
        fila = cursor.fetchone()
        cursor.close()
        
    # Métodos opcionales de utilidad:
    def registrar_horas(self, conexion):
        cursor = conexion.conexion.cursor()
        consulta = """
            INSERT INTO ReporteHoras (horasTrabajadas, fecha, descripcionTareas, idEmpleado, idProyecto)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (self.horas_trabajadas, self.fecha, self.descripcion_tareas, self.id_empleado, self.id_proyecto)
        cursor.execute(consulta, valores)
        conexion.conexion.commit()
        self.id = cursor.lastrowid
        cursor.close()
