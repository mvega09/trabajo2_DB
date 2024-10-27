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

