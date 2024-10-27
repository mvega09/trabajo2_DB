from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import Optional
from enum import Enum
from datetime import datetime

class Gender(str, Enum):
    masculino = "Masculino"
    femenino = "Femenino"

class PatientCreate(BaseModel):
    nombre: str = Field(..., description="Nombre del paciente (campo requerido)")
    apellido: str = Field(..., description="Apellido del paciente (campo requerido)")
    fecha_nacimiento: date
    genero: Gender = Field(..., description="Escribir Masculino o Femenino (campo requerido)")

class Patient(PatientCreate):
    id: int

class DoctorCreate(BaseModel):
    nombre: str = Field(..., description="Nombre del paciente (campo requerido)")
    apellido: str = Field(..., description="Apellido del paciente (campo requerido)")
    especialidad: str = Field(..., description="Especialidad del medico(campo requerido)")

class Doctor(DoctorCreate):
    id: int

class ExamenCreate(BaseModel):
    fecha: date
    tipo: str = Field(..., description="Tipo de examen (ej: Radiografía, Tomografía, Resonancia, Ecografia, etc.)")

class Examen(ExamenCreate):
    id: int
    id_paciente: int
    id_medico: int

class ImagenCreate(BaseModel):
    ruta_imagen: str = Field(..., description="Ruta de la imagen (campo requerido)")
    tipo_imagen: str = Field(default='DICOM', description="Tipo de imagen, por defecto DICOM")

class Imagen(ImagenCreate):
    id: int
    id_examen: int
    fecha_creacion: datetime = Field(default_factory=datetime.now, description="Fecha de creación de la imagen")