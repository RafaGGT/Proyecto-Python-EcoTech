import mysql.connector

class Conexion:
    def __init__(self, user, password, database, host = "localhost", port = 3306):
        self.conexion = mysql.connector.connect(
            user = user,
            password = password,
            database = database,
            host = host,
            port = port
        )

    def cerrar(self):
        self.conexion.close()

    