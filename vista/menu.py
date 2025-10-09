from modelo.bd import Conexion
from modelo.gerente import Gerente
from modelo.administrador import Administrador
from modelo.empleado import Empleado
from modelo.usuario import Usuario
import os
from datetime import date

class Menu:
    def __init__(self):
        self.conexion = Conexion(
            user = "root",
            password = "root",
            database = "bdpython",
            host = "localhost",
            port = 3306
        )

    def mostrarMenu(self):
        os.system("cls")
        print("=== Menú Principal ===")
        print("1. Iniciar Sesión")
        print("2. Registrar Usuario")
        print("0. Salir")
        self.obtenerOpcion()

    def salir(self):
        print("Adios! 👋🏻")
        self.conexion.cerrar()

    def obtenerOpcion(self):
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            self.iniciarSesion()
        elif opcion == '2':
            self.registrarUsuario()
        elif opcion == '0':
            self.salir()

    def registrarUsuario(self):
        os.system("cls")
        print("=== Registro de Usuario ===")
        nombreDeUsuario = input("Nombre de usuario: ")
        nombreDeUsuario = nombreDeUsuario.strip()
        contrasena = input("Contraseña: ")
        contrasena = contrasena.strip()
        nombre = input("Nombre completo: ")
        nombre = nombre.strip().title()
        fechaInicio = date.today().strftime("%Y-%m-%d")
        salario = input("Salario: ")
        salario = int(salario.strip())
        print("Seleccione un rol \n1) Empleado\n2) Gerente\n3)Administrador")
        rolInput = input("Seleccione un rol: ") 
    # Diccionario que mapea la opción a (nombre del rol, clase correspondiente)
        roles_clases = {
            '1': ("Empleado", Empleado),
            '2': ("Gerente", Gerente),
            '3': ("Administrador", Administrador)
        }

        if rolInput in roles_clases:
            rol, Clase = roles_clases[rolInput]
            nuevoEmpleado = Clase(
                nombreDeUsuario=nombreDeUsuario,
                contrasena=contrasena,
                rol=rol,
                nombre=nombre,
                direccion="",
                telefono="",
                fechaInicio=fechaInicio,
                salario=salario
            )
            try:
                nuevoEmpleado.crearUsuario(self.conexion)
                print("Usuario registrado exitosamente.")
            except Exception as e:
                print(f"Error al registrar usuario: {e}")
        else:
            print("Rol inválido. Intente de nuevo.")

        input("Presione Enter para continuar...")
        self.mostrarMenu()



    def iniciarSesion(self):
        os.system("cls")
        print("=== Iniciar Sesión ===")
        nombreDeUsuario = input("Nombre de usuario: ")
        contrasena = input("Contraseña: ")
        # Aquí se debería validar el usuario con la base de datos
        autenticar = Usuario(nombreDeUsuario, contrasena) 
        try:
            if autenticar.iniciarSesion(self.conexion):
                print("Inicio de sesión exitoso.")
            else:
                print("Nombre de usuario o contraseña incorrectos.")
                input("Presione Enter para continuar...")
        except Exception as e:
            print(f"Error al iniciar sesión: {e}")
            input("Presione Enter para continuar...")
            self.mostrarMenu()

        
        