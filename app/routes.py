from fastapi import APIRouter, HTTPException
from app.models import PatientCreate, Patient, DoctorCreate, Doctor, ExamenCreate, Examen
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

@router.post("/Doctors/", response_model=List[Doctor])
def create_doctor(doctores: List[DoctorCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO medicos (nombre, apellido, especialidad)
        VALUES (%s, %s, %s)
        """

        values = [(doctor.nombre, doctor.apellido, doctor.especialidad) for doctor in doctores]
        cursor.executemany(query, values)
        conn.commit()
        first_inserted_id = cursor.lastrowid
        created_doctors = [
            Doctor(id=first_inserted_id + idx, **doctor.dict())
            for idx, doctor in enumerate(doctores)]
        return created_doctors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error al procesar la solicitud: {str(e)}")
    finally:
        cursor.close()
        conn.close()

@router.get("/Doctors/", response_model=list[Doctor])
def list_doctors():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = "SELECT * FROM medicos"
        cursor.execute(query)
        doctors = cursor.fetchall()
        return [Doctor(**doctor) for doctor in doctors]
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/Exams/{id_paciente}/{id_medico}/", response_model=List[Examen])
def create_examenes_bulk(id_paciente: int, id_medico: int, examenes: List[ExamenCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM pacientes WHERE id = %s", (id_paciente,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Paciente no encontrado")
        
        cursor.execute("SELECT * FROM medicos WHERE id = %s", (id_medico,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Médico no encontrado")
        
        created_examenes = []
        for examen in examenes:
            query = """
            INSERT INTO examenes (id_paciente, id_medico, fecha, tipo)
            VALUES (%s, %s, %s, %s)
            """
            values = (id_paciente, id_medico, examen.fecha, examen.tipo)
            
            cursor.execute(query, values)
            examen_id = cursor.lastrowid
            created_examenes.append(Examen(id=examen_id, id_paciente=id_paciente, id_medico=id_medico, **examen.dict()))
        
        conn.commit()
        return created_examenes
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()

@router.get("/Exams/", response_model=list[Examen])
def list_exams():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = "SELECT * FROM examenes"
        cursor.execute(query)
        exams = cursor.fetchall()
        return [Examen(**exam) for exam in exams]
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()