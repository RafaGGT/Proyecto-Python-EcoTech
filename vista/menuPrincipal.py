from modelo.bd import Conexion
from modelo.gerente import Gerente
from modelo.administrador import Administrador
from modelo.empleado import Empleado
from modelo.usuario import Usuario
import os
from datetime import date
import pwinput 

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
        print("0. Salir")
        self.obtenerOpcion()

    def menuInicio(self):
        os.system("cls")
        usuario_actual = self.usuario_actual
        conexion = self.conexion
        # Diccionario de roles y sus facultades
        poderes = {
                "Empleado": [
                    ("Modificar usuario", self.modificarUsuario),
                    ("Registro de tiempo", lambda: print("Funcionalidad en desarrollo...")),
                    ("Listar empleados", self.listarEmpleados),
                    ("Salir", self.salir)
                ],
                "Gerente": [
                    ("Modificar usuario", self.modificarUsuario), 
                    ("Registro de tiempo", lambda: print("Funcionalidad en desarrollo...")),                 
                    ("Agregar Proyecto", lambda: print("Funcionalidad en desarrollo...")),
                    ("Agregar Empleado a Proyecto", lambda: print("Funcionalidad en desarrollo...")),
                    ("Desasignar Empleado de Proyecto", lambda: print("Funcionalidad en desarrollo...")),
                    ("Asignar Empleado a departamento", lambda: print("Funcionalidad en desarrollo...")),
                    ("Desasignar Empleado de departamento", lambda: print("Funcionalidad en desarrollo...")),
                    ("Salir", self.salir)
                ],
                "Administrador": [
                    ("Contratar empleado", self.registrarUsuario),
                    ("Modificar usuario", self.modificarUsuario),
                    ("Agregar Departamento", lambda: print("Funcionalidad en desarrollo...")),  
                    ("Eliminar Departamento", lambda: print("Funcionalidad en desarrollo...")),
                    ("Registro de tiempo", lambda: print("Funcionalidad en desarrollo...")),
                    ("Generar Informe", lambda: print("Funcionalidad en desarrollo...")),
                    ("Salir", self.salir)
                ]
            }
        # Menu personalizado según el rol
        print(f"=== Bienvenido {usuario_actual.nombre} ===")
        if usuario_actual.rol in poderes:
            opciones = poderes[usuario_actual.rol]
            for i, (nombre, _) in enumerate(opciones, start=1):
                print(f"{i}) {nombre}")
            opcion = input("Seleccione una opción: ")
            opcion = int(opcion.strip())
            eleccion = poderes[usuario_actual.rol][opcion - 1][1]
            eleccion()

    def salir(self):
        print("Adios! 👋🏻")
        self.conexion.cerrar()

    def obtenerOpcion(self):
        opcion = input("Seleccione una opción: ")
        if opcion == '1':
            self.iniciarSesion()
        elif opcion == '0':
            self.salir()
        else:
            print("Opción inválida. Intente de nuevo.")
            input("Presione Enter para continuar...")
            self.mostrarMenu()


    def registrarUsuario(self):
        os.system("cls")
        print("=== Registro de Usuario ===")
        nombreDeUsuario = input("Nombre de usuario: ")
        nombreDeUsuario = nombreDeUsuario.strip()
        contrasena = pwinput.pwinput("Ingrese la contraseña: ", mask = "*")
        contrasena = contrasena.strip()
        nombre = input("Nombre completo: ")
        nombre = nombre.strip().title()
        fechaInicio = date.today().strftime("%Y-%m-%d")
        salario = input("Salario: ")
        salario = int(salario.strip())
        print("Seleccione un rol \n1) Empleado\n2) Gerente\n3) Administrador")
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

    def iniciarSesion(self):
        os.system("cls")
        print("=== Iniciar Sesión ===")
        nombreDeUsuario = input("Nombre de usuario: ")
        nombreDeUsuario = nombreDeUsuario.strip()
        contrasena = pwinput.pwinput("Ingrese la contraseña: ", mask = "*")
        contrasena = contrasena.strip()
        # Aquí se debería validar el usuario con la base de datos
        autenticar = Empleado(nombreDeUsuario, contrasena) 
        try:
            if autenticar.iniciarSesion(self.conexion):
                self.usuario_actual = autenticar
                print("Inicio de sesión exitoso.")
                input("Presione Enter para continuar...")
                self.menuInicio()
            else:
                print("Nombre de usuario o contraseña incorrectos.")
                input("Presione Enter para continuar...")
                self.mostrarMenu()
        except Exception as e:
            print(f"Error al iniciar sesión: {e}")
            input("Presione Enter para continuar...")
            self.mostrarMenu()
            
    def modificarUsuario(self):
        if not hasattr(self, "usuario_actual"):
            print("Debes iniciar sesión primero.")
            input("Presione Enter para continuar...")
            return

        usuario_actual = self.usuario_actual
        conexion = self.conexion

        while True:
            os.system("cls")
            print("=== Modificar Usuario ===")
            print(f"1) Nombre de usuario: {usuario_actual.nombreDeUsuario}")
            print(f"2) Contraseña: {'*' * 8}")
            print(f"3) Rol: {usuario_actual.rol}")
            print(f"4) Nombre: {usuario_actual.nombre}")
            print(f"5) Dirección: {usuario_actual.direccion}")
            print(f"6) Teléfono: {usuario_actual.telefono}")
            print(f"7) Fecha de inicio: {usuario_actual.fechaInicio}")
            print(f"8) Salario: {usuario_actual.salario}")
            print("0) Salir")

            opcion = input("Seleccione el campo a modificar: ")
            # y si creamos un diccionario que mapee la opción al atributo y tipo de dato
            if opcion == '1':
                nuevo_valor = input("Nuevo nombre de usuario: ").strip()
                usuario_actual.nombreDeUsuario = nuevo_valor
            elif opcion == '2':
                nuevo_valor = pwinput.pwinput("Nueva contraseña: ", mask = "*").strip()
                usuario_actual.contrasena = nuevo_valor
            elif opcion == '3':
                print("Seleccione un rol \n1) Empleado\n2) Gerente\n3) Administrador")
                rolInput = input("Seleccione un rol: ") 
                roles_clases = {
                    '1': "Empleado",
                    '2': "Gerente",
                    '3': "Administrador"
                }
                if rolInput in roles_clases:
                    usuario_actual.rol = roles_clases[rolInput]
                else:
                    print("Rol inválido. Intente de nuevo.")
                    input("Presione Enter para continuar...")
                    continue
            elif opcion == '4':
                nuevo_valor = input("Nuevo nombre completo: ").strip().title()
                usuario_actual.nombre = nuevo_valor
            elif opcion == '5':
                nuevo_valor = input("Nueva dirección: ").strip().title()
                usuario_actual.direccion = nuevo_valor
            elif opcion == '6':
                nuevo_valor = input("Nuevo teléfono: ").strip()
                usuario_actual.telefono = nuevo_valor
            elif opcion == '7':
                nuevo_valor = input("Nueva fecha de inicio (YYYY-MM-DD): ").strip()
                usuario_actual.fechaInicio = nuevo_valor
            elif opcion == '8':
                nuevo_valor = input("Nuevo salario: ").strip()
                usuario_actual.salario = int(nuevo_valor)
            elif opcion == '0':
                break
            else:
                print("Opción inválida. Intente de nuevo.")
                input("Presione Enter para continuar...")
                continue
            try:
                usuario_actual.modificarUsuario(conexion)
                print("Usuario modificado exitosamente.")
            except Exception as e:
                print(f"Error al modificar usuario: {e}")
            input("Presione Enter para continuar...")
            self.mostrarMenu()

    def listarEmpleados(self):
        os.system("cls")
        try:
            empleados = Empleado.listarEmpleados(self.conexion)
            print("=== Lista de Empleados ===")
            for emp in empleados:
                print(f"ID: {emp[0]}, Nombre: {emp[1]}")
        except Exception as e:
            print(f"Error al listar empleados: {e}")
        input("Presione Enter para continuar...")