class RegistroHoras:
    def __init__(self, id=None, horas_trabajadas=None, fecha=None, descripcion_tareas=None, id_empleado=None, id_proyecto=None):
        self.id = id
        self.horas_trabajadas = horas_trabajadas
        self.fecha = fecha
        self.descripcion_tareas = descripcion_tareas
        self.id_empleado = id_empleado
        self.id_proyecto = id_proyecto

    @staticmethod
    def obtener_reportes(conexion, id_empleado):
        cursor = conexion.conexion.cursor()
        consulta = """
            SELECT id, horasTrabajadas, fecha, descripcionTareas, idEmpleado, idProyecto
            FROM RegistroHoras
            WHERE idEmpleado = %s
        """
        cursor.execute(consulta, (id_empleado,))
        reportes = cursor.fetchall()
        cursor.close()
        return reportes
        
    def registrar_horas(self, conexion):
        cursor = conexion.conexion.cursor()
        consulta = """
            INSERT INTO RegistroHoras (horasTrabajadas, fecha, descripcionTareas, idEmpleado, idProyecto)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (self.horas_trabajadas, self.fecha, self.descripcion_tareas, self.id_empleado, self.id_proyecto)
        cursor.execute(consulta, valores)
        conexion.conexion.commit()
        self.id = cursor.lastrowid
        cursor.close()

    def eliminar_reporte(conexion, id_reporte):
        cursor = conexion.conexion.cursor()
        consulta = "DELETE FROM RegistroHoras WHERE id = %s"
        cursor.execute(consulta, (id_reporte,))
        conexion.conexion.commit()
        cursor.close()

    def modificarReporte(self, conexion):
        cursor = conexion.conexion.cursor()
        consulta = """
        UPDATE RegistroHoras
        SET horasTrabajadas = %s,
            fecha = %s,
            descripcionTareas = %s
        WHERE id = %s
        """
        valores = (self.horasTrabajadas, self.fecha, self.descripcionTareas, self.id)
        cursor.execute(consulta, valores)
        conexion.conexion.commit()
        cursor.close()
        return True