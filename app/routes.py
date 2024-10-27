from fastapi import APIRouter, HTTPException
from app.models import PatientCreate, Patient
from app.database import get_db_connection
from typing import List

router = APIRouter()

@router.post("/Patients/", response_model=List[Patient])
def create_patients(pacientes: List[PatientCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO pacientes (nombre, apellido, fecha_nacimiento, genero)
        VALUES (%s, %s, %s, %s)
        """

        values = [(paciente.nombre, paciente.apellido, paciente.fecha_nacimiento, paciente.genero) for paciente in pacientes]
        cursor.executemany(query, values)
        conn.commit()
        patient_ids = cursor.lastrowid  
        created_patients = []
        for idx, paciente in enumerate(pacientes):
            created_patients.append(Patient(id=patient_ids + idx, **paciente.dict()))
        
        return created_patients
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Ocurrió un error al procesar la solicitud.")
    finally:
        cursor.close()
        conn.close()



@router.get("/Patients/", response_model=list[Patient])
def list_patients():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = "SELECT * FROM pacientes"
        cursor.execute(query)
        patients = cursor.fetchall()
        return [Patient(**paciente) for paciente in patients]
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

