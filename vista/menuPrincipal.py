from modelo.bd import Conexion
from modelo.gerente import Gerente
from modelo.administrador import Administrador
from modelo.empleado import Empleado
from modelo.reportehoras import RegistroHoras
from modelo.proyecto import Proyecto
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
        print("=== EcoTech Solutions ===")
        print("1. Iniciar Sesión")
        print("0. Salir")
        self.obtenerOpcion()

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

    def iniciarSesion(self):
        os.system("cls")
        print("=== Iniciar Sesión ===")
        nombreDeUsuario = input("Nombre de usuario: ")
        nombreDeUsuario = nombreDeUsuario.strip()
        contrasena = pwinput.pwinput("Ingrese la contraseña: ", mask = "*")
        contrasena = contrasena.strip()
        # Verificar credenciales al instanciar el objeto Empleado con el nombre de usuario y la contraseña
        autenticar = Empleado(nombreDeUsuario, contrasena) 
        try:
            if autenticar.iniciarSesion(self.conexion):
                # Guardar el usuario autenticado para uso posterior
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

    def menuInicio(self):
        os.system("cls")
        # Hacemos uso del atributo guardado del usuario autenticado
        usuario_actual = self.usuario_actual
        conexion = self.conexion
        # Diccionario de roles y sus facultades
        poderes = {
                "Empleado": [
                    ("Modificar usuario", self.modificarUsuario),
                    ("Registro de tiempo", self.generarReporte),
                    ("Listar Registros", self.listarReportes),
                    ("Modificar Registro", self.modificarReporte),           
                    ("Eliminar registro de tiempo", self.eliminarReporte),
                    ("Listar empleados", self.listarEmpleados),
                    ("Salir", self.salir)
                ],
                "Gerente": [
                    ("Modificar usuario", self.modificarUsuario), 
                    ("Registro de tiempo", self.generarReporte),
                    ("Listar Registros", self.listarReportes),
                    ("Modificar Registro", self.modificarReporte),           
                    ("Eliminar registro de tiempo", self.eliminarReporte),              
                    ("Agregar Proyecto", self.crearProyecto),
                    ("Listar Proyecto", self.listarProyecto),
                    ("Modificar proyecto", self.modificarProyecto),
                    ("Eliminar proyecto", self.eliminarProyecto),
                    ("Agregar Empleado a Proyecto", lambda: print("Funcionalidad en desarrollo...")),
                    ("Desasignar Empleado de Proyecto", lambda: print("Funcionalidad en desarrollo...")),
                    ("Asignar Empleado a departamento", lambda: print("Funcionalidad en desarrollo...")),
                    ("Desasignar Empleado de departamento", lambda: print("Funcionalidad en desarrollo...")),
                    ("Salir", self.salir)
                ],
                "Administrador": [
                    ("Contratar empleado", self.registrarUsuario),
                    ("Registro de tiempo", self.generarReporte),
                    ("Listar Registros", self.listarReportes),
                    ("Modificar Registro", self.modificarReporte),           
                    ("Eliminar registro de tiempo", self.eliminarReporte),
                    ("Modificar usuario", self.modificarUsuario),
                    ("Agregar Departamento", lambda: print("Funcionalidad en desarrollo...")),  
                    ("Eliminar Departamento", lambda: print("Funcionalidad en desarrollo...")),                    
                    ("Generar Informe", lambda: print("Funcionalidad en desarrollo...")),
                    ("Despedir Empleado", self.despedirEmpleados),
                    ("Salir", self.salir)
                ]
            }
        # Menu personalizado según el rol
        print(f"=== Bienvenido {usuario_actual.nombre} ===")
        if usuario_actual.rol in poderes:
            opciones = poderes[usuario_actual.rol]
            # Mostrar opciones disponibles según el rol
            for i, (nombre, _) in enumerate(opciones, start=1):
                print(f"{i}) {nombre}")
            opcion = input("Seleccione una opción: ")
            opcion = int(opcion.strip())
            eleccion = poderes[usuario_actual.rol][opcion - 1][1]()
        else: 
            self.despedido()

    def salir(self):
        print("Adios! 👋🏻")
        self.conexion.cerrar()

    def despedido(self):
        print("Haz sido removido de la empresa")

# ******************************************** Zona CRUD Usuarios ********************************************

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
        rolInput = input("Seleccione un rol \n1) Empleado\n2) Gerente\n3) Administrador \nSeleccione un rol: ") 
    # Diccionario que mapea la opción a (nombre del rol, clase correspondiente)
        roles_clases = {
            '1': ("Empleado", Empleado),
            '2': ("Gerente", Gerente),
            '3': ("Administrador", Administrador)
        }
        if rolInput in roles_clases:
            # Establecemos el rol y la clase con la tupla
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
        self.menuInicio()
            
    def modificarUsuario(self):
        # Hacemos uso del atributo guardado del usuario autenticado y la conexión
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
        self.menuInicio()

    def despedirEmpleados(self):
        os.system("cls")
# ******************************************** Zona CRUD Departamentos ********************************************
# ******************************************** Zona CRUD Proyectos ********************************************
    def crearProyecto(self):
        os.system("cls")
        nombre = print("Nombre del proyecto: ")
        nombre = nombre.strip().title()
        descripcion = print("Descripcion del proyecto: ")
        descripcion = descripcion.strip()
        fecha = input("Nueva fecha de inicio (YYYY-MM-DD): ")
        fecha = fecha.strip()
        nuevoProyecto = Proyecto(
            nombre = nombre,
            descripcion = descripcion,
            fecha = fecha
        )
        nuevoProyecto.crearProyecto(self.conexion)
        print("Proyecto registrado exitosamente.")
        self.menuInicio()

    def listarProyecto(self):
        os.system("cls")
        print("=== Lista de Proyectos ===\n")
        proyectos = Proyecto.listarProyectos(self.conexion)
        if not proyectos:
            print("No hay proyectos registrados.\n")
        else:
            for proyecto in proyectos:
                print(f"ID: {proyecto.id} \nNombre: {proyecto.nombre} \nFecha Inicio: {proyecto.fechaInicio} \nDescripción: {proyecto.descripcion}\n")
        input("\nPresione Enter para continuar...")
        self.menuInicio

    def modificarProyecto(self):
        os.system("cls")
        print("=== Modificar Proyecto ===\n")
        proyectos = Proyecto.listarProyectos(self.conexion)
        if not proyectos:
            print("No hay proyectos registrados.\n")
            input("Presione Enter para continuar...")
            self.menuInicio()
            return

        for p in proyectos:
            print(f"ID: {p[0]} | Nombre: {p[1]} | Fecha Inicio: {p[3]}")

        try:
            id_proyecto = int(input("\nIngrese el ID del proyecto que desea modificar: "))
        except ValueError:
            print("⚠️ ID inválido.")
            input("Presione Enter para continuar...")
            return self.menuInicio()

        nombre = input("Nuevo nombre (deje vacío para mantener): ").strip().title()
        descripcion = input("Nueva descripción (deje vacío para mantener): ").strip()
        fecha = input("Nueva fecha de inicio (YYYY-MM-DD, deje vacío para mantener): ").strip()   

        # Buscar el proyecto actual
        proyecto_actual = next((p for p in proyectos if p[0] == id_proyecto), None)
        if not proyecto_actual:
            print("⚠️ Proyecto no encontrado.")
            input("Presione Enter para continuar...")
            return self.menuInicio()

        nuevoProyecto = Proyecto(
            id=id_proyecto,
            nombre=nombre or proyecto_actual[1],
            descripcion=descripcion or proyecto_actual[2],
            fechaInicio=fecha or proyecto_actual[3]
        )

        nuevoProyecto.modificarProyecto(self.conexion)
        print("\n✅ Proyecto modificado exitosamente.")
        input("\nPresione Enter para continuar...")
        self.menuInicio()

    def eliminarProyecto(self):
        os.system("cls")
        print("=== Eliminar Proyecto ===\n")
        proyectos = Proyecto.listarProyectos(self.conexion)
        if not proyectos:
            print("No hay proyectos registrados.\n")
            input("Presione Enter para continuar...")
            self.menuInicio()
            return

        for p in proyectos:
            print(f"ID: {p[0]} | Nombre: {p[1]} | Fecha Inicio: {p[3]}")

        try:
            id_proyecto = int(input("\nIngrese el ID del proyecto que desea eliminar: "))
        except ValueError:
            print("⚠️ ID inválido.")
            input("Presione Enter para continuar...")
            return self.menuInicio()

        confirm = input("¿Está seguro que desea eliminar este proyecto? (s/n): ").strip().lower()
        if confirm == "s":
            Proyecto.eliminarProyecto(self.conexion, id_proyecto)
            print("\n✅ Proyecto eliminado exitosamente.")
        else:
            print("\nOperación cancelada.")

        input("\nPresione Enter para continuar...")
        self.menuInicio()
   

# ******************************************** Zona CRUD Reportes ********************************************
    def listarReportes(self):
        os.system("cls")
        try:
            reportes = RegistroHoras.obtener_reportes(self.conexion, self.usuario_actual.id)
            print("=== Lista de Reportes de Horas ===")
            if not reportes:
                print("No hay reportes registrados para este empleado.")
            else:
                for rep in reportes:
                    print(f"\nID: {rep[0]}\nHoras Trabajadas: {rep[1]}\nFecha: {rep[2]}\nDescripción: {rep[3]}\nID Proyecto: {rep[5]} \n")
        except Exception as e:
            print(f"Error al listar reportes: {e}")
        

    def generarReporte(self):
        os.system("cls")
        print("=== Registrar Reporte de Horas ===")
        try:
            horas = int(input("Ingrese cantidad de horas trabajadas: "))
            fecha = input("Ingrese fecha (YYYY-MM-DD): ")
            descripcion = input("Ingrese descripción de tareas realizadas: ")
            self.listarReportes()
            id_proyecto = input("Ingrese el id del proyecto")
            nuevo_reporte = RegistroHoras(
                horas_trabajadas=horas,
                fecha=fecha,
                descripcion_tareas=descripcion,
                id_empleado=self.usuario_actual.id,
                id_proyecto=id_proyecto
            )
            nuevo_reporte.registrar_horas(self.conexion)
            print("\n✅ Reporte registrado correctamente.")
        except Exception as e:
            print(f"Error al registrar reporte: {e}")
        input("Presione Enter para continuar...")
        self.menuInicio()

    def eliminarReporte(self):
        self.listarReportes()
        try:
            id_reporte = int(input("Ingrese el ID del reporte a eliminar: "))
            confirmar = input("¿Está seguro que desea eliminarlo? (s/n): ").lower()
            if confirmar == "s":
                RegistroHoras.eliminar_reporte(self.conexion, id_reporte)
                print("✅ Reporte eliminado correctamente.")
            else:
                print("Operación cancelada.")
        except Exception as e:
            print(f"Error al eliminar reporte: {e}")

    def modificarReporte(self):
        os.system("cls")
        print("=== Modificar Reporte de Horas ===\n")
        reportes = RegistroHoras.listarReportes(self.conexion, self.usuario_actual.id)

        if not reportes:
            print("No hay reportes registrados.\n")
            input("Presione Enter para continuar...")
            self.menuInicio()
            return

        for r in reportes:
            print(f"ID: {r[0]} | Fecha: {r[2]} | Horas: {r[1]} | Proyecto ID: {r[4]}")

        try:
            id_reporte = int(input("\nIngrese el ID del reporte que desea modificar: "))
        except ValueError:
            print("⚠️ ID inválido.")
            input("Presione Enter para continuar...")
            return self.menuInicio()

        # Buscar reporte actual
        reporte_actual = next((r for r in reportes if r[0] == id_reporte), None)
        if not reporte_actual:
            print("⚠️ Reporte no encontrado.")
            input("Presione Enter para continuar...")
            return self.menuInicio()

        # Nuevos datos
        horas = input(f"Nuevas horas trabajadas (actual: {reporte_actual[1]}): ").strip()
        fecha = input(f"Nueva fecha (actual: {reporte_actual[2]}) (YYYY-MM-DD): ").strip()
        descripcion = input(f"Nueva descripción (actual: {reporte_actual[3]}): ").strip()

        nuevo_reporte = RegistroHoras(
            id=id_reporte,
            horasTrabajadas=int(horas) if horas else reporte_actual[1],
            fecha=fecha if fecha else reporte_actual[2],
            descripcionTareas=descripcion if descripcion else reporte_actual[3],
            idEmpleado=self.usuario_actual.id,
            idProyecto=reporte_actual[4]
        )

        nuevo_reporte.modificarReporte(self.conexion)
        print("\n✅ Reporte modificado exitosamente.")
        input("\nPresione Enter para continuar...")
        self.menuInicio()
