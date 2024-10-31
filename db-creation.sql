CREATE DATABASE IF NOT EXISTS ImagenesDiagnosticas;
USE ImagenesDiagnosticas;


CREATE TABLE Pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    genero ENUM('Masculino', 'Femenino') NOT NULL
);

CREATE TABLE Medicos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100) NOT NULL
);

CREATE TABLE Examenes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NOT NULL,
    id_medico INT NOT NULL,
    fecha DATE NOT NULL,
    tipo VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_paciente) REFERENCES Pacientes(id) ON DELETE CASCADE,
    FOREIGN KEY (id_medico) REFERENCES Medicos(id) ON DELETE CASCADE
);


CREATE TABLE Imagenes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_examen INT NOT NULL,
    ruta_imagen VARCHAR(255) NOT NULL,
    tipo_imagen ENUM('DICOM') NOT NULL DEFAULT 'DICOM',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_examen) REFERENCES Examenes(id) ON DELETE CASCADE
);

CREATE TABLE Diagnosticos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_examen INT NOT NULL,
    descripcion TEXT NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (id_examen) REFERENCES Examenes(id) ON DELETE CASCADE
);

CREATE TABLE Reportes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_diagnostico INT NOT NULL,
    id_medico INT NOT NULL,
    informe TEXT NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (id_diagnostico) REFERENCES Diagnosticos(id) ON DELETE CASCADE,
    FOREIGN KEY (id_medico) REFERENCES Medicos(id) ON DELETE CASCADE
);
