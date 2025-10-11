CREATE database bdpython
use bdpython

CREATE TABLE Usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombreUsuario VARCHAR(50) NOT NULL UNIQUE,
    contrasena VARCHAR(250) NOT NULL,
    rol varchar(20)
);

CREATE TABLE Empleados (
    id INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(150),
    numeroTelefono VARCHAR(20),
    direccionCorreo VARCHAR(100),
    fechaInicioContrato DATE,
    salario INT,
    FOREIGN KEY (id) REFERENCES Usuario(id)
);

CREATE TABLE Administrador (
    id INT PRIMARY KEY,
    FOREIGN KEY (id) REFERENCES Empleados(id)
);

CREATE TABLE Gerente (
    id INT PRIMARY KEY,
    FOREIGN KEY (id) REFERENCES Empleados(id)
);

CREATE TABLE Departamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    idGerente INT UNIQUE,
    FOREIGN KEY (idGerente) REFERENCES Gerente(id)
);

ALTER TABLE Empleados
ADD COLUMN idDepartamento INT,
ADD FOREIGN KEY (idDepartamento) REFERENCES Departamentos(id);

CREATE TABLE Proyectos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fechaInicio DATE
);

CREATE TABLE Empleado_Proyecto (
    idEmpleado INT,
    idProyecto INT,
    PRIMARY KEY (idEmpleado, idProyecto),
    FOREIGN KEY (idEmpleado) REFERENCES Empleados(id),
    FOREIGN KEY (idProyecto) REFERENCES Proyectos(id)
);

CREATE TABLE RegistroHoras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    horasTrabajadas INT,
    fecha DATE,
    descripcionTareas TEXT,
    idEmpleado INT,
    idProyecto INT,
    FOREIGN KEY (idEmpleado) REFERENCES Empleados(id),
    FOREIGN KEY (idProyecto) REFERENCES Proyectos(id)
);

select * from usuario 
select * from empleados
select * from gerente
select * from administrador
SELECT nombreUsuario, contrasena, rol FROM Usuario 