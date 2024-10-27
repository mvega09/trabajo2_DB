from fastapi import APIRouter, HTTPException
from app.models import PatientCreate, Patient, DoctorCreate, Doctor, ExamenCreate, Examen, ImagenCreate, Imagen, Dianosticos, Diagnostico, Reportes, Reporte
from app.database import get_db_connection
from typing import List
from datetime import date

router = APIRouter()

@router.post("/Patients/", response_model=List[Patient])
def create_patients_bulk(pacientes: List[PatientCreate]):
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
def create_doctors_bulk(doctores: List[DoctorCreate]):
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

@router.post("/Images/{id_examen}/", response_model=List[Imagen])
def create_images_bulk(id_examen: int, images: List[ImagenCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM examenes WHERE id = %s", (id_examen,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Examen no encontrado")
        
        created_image_path = []
        for image in images:
            query = """
            INSERT INTO imagenes (id_examen, ruta_imagen, tipo_imagen)
            VALUES (%s, %s, %s)
            """
            values = (id_examen, image.ruta_imagen, image.tipo_imagen)
            
            cursor.execute(query, values)
            image_id = cursor.lastrowid
            created_image_path.append(Imagen(id=image_id, id_examen=id_examen, **image.dict()))
        
        conn.commit()
        return created_image_path
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()

@router.get("/Images/", response_model=list[Imagen])
def list_exams():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = "SELECT * FROM imagenes"
        cursor.execute(query)
        images = cursor.fetchall()
        return [Imagen(**image) for image in images]
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
@router.post("/Diagnostics/{id_examen}/", response_model=List[Diagnostico])
def create_diagnostic_bulk(id_examen: int, diagnostics: List[Dianosticos]):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM examenes WHERE id = %s", (id_examen,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Examen no encontrado")
        
        created_diagnostics_path = []
        for diagnostic in diagnostics:
            query = """
            INSERT INTO diagnosticos (id_examen, descripcion, fecha)
            VALUES (%s, %s, %s)
            """
            values = (id_examen, diagnostic.descripcion, diagnostic.fecha)
            
            cursor.execute(query, values)
            diagnostic_id = cursor.lastrowid
            created_diagnostics_path.append(Diagnostico(id=diagnostic_id, id_examen=id_examen, **diagnostic.dict()))
        
        conn.commit()
        return created_diagnostics_path
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()

@router.get("/Diagnostics/", response_model=list[Diagnostico])
def list_Diagnostic():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = "SELECT * FROM diagnosticos"
        cursor.execute(query)
        diagnostics = cursor.fetchall()
        return [Diagnostico(**diagnostic) for diagnostic in diagnostics]
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    

@router.post("/Reports/{id_diagnostico}/{id_medico}/", response_model=List[Reporte])
def create_report_bulk(id_diagnostico: int, id_medico: int, reports: List[Reportes]):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM diagnosticos WHERE id = %s", (id_diagnostico,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Diagnostico no encontrado")
        
        cursor.execute("SELECT * FROM medicos WHERE id = %s", (id_medico,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Médico no encontrado")
        
        created_report_path = []
        for report in reports:
            query = """
            INSERT INTO reportes (id_diagnostico, id_medico, informe, fecha)
            VALUES (%s, %s, %s, %s)
            """
            values = (id_diagnostico, id_medico, report.informe, report.fecha)
            
            cursor.execute(query, values)
            report_id = cursor.lastrowid
            created_report_path.append(Reporte(id=report_id, id_diagnostico=id_diagnostico, id_medico=id_medico, **report.dict()))
        
        conn.commit()
        return created_report_path
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()

@router.get("/Reports/", response_model=list[Reporte])
def list_Reports():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = "SELECT * FROM reportes"
        cursor.execute(query)
        reports = cursor.fetchall()
        return [Reporte(**report) for report in reports]
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/Reports/", response_model=list[Reporte])
def list_reports():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = "SELECT * FROM reportes"
        cursor.execute(query)
        reports = cursor.fetchall()
        return [Examen(**report) for report in reports]
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

#1
@router.get("/examenes/paciente/{id_paciente}")
def get_examenes_paciente(id_paciente: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
        SELECT e.id, e.fecha, e.tipo, m.nombre AS medico_nombre, m.apellido AS medico_apellido
        FROM Examenes e
        INNER JOIN Medicos m ON e.id_medico = m.id
        WHERE e.id_paciente = %s
        """
        cursor.execute(query, (id_paciente,)) 
        result = cursor.fetchall()
        return result

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al realizar la consulta")

    finally:
        cursor.close()
        conn.close()

#2
@router.get("/examenes/medico/{id_medico}")
def get_examenes_doctor(id_medico: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """SELECT COUNT(*) AS total_examenes FROM Examenes WHERE id_medico = %s
        """
        cursor.execute(query, (id_medico,)) 
        result = cursor.fetchall()
        return result

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al realizar la consulta")

    finally:
        cursor.close()
        conn.close()

#3
@router.get("/examenes/medico/promedio/{id_medico}")
def get_examenes_doctor_count(id_medico: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """SELECT m.id AS id_medico, m.nombre, m.apellido, COUNT(e.id) / COUNT(DISTINCT e.fecha) AS promedio_examenes
        FROM Examenes e
        INNER JOIN Medicos m ON e.id_medico = m.id
        WHERE m.id = %s
        GROUP BY m.id, m.nombre, m.apellido;
        """
        cursor.execute(query, (id_medico,)) 
        result = cursor.fetchall()
        return result

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al realizar la consulta")

    finally:
        cursor.close()
        conn.close()

#4
@router.get("/pacientes/medico/{id_medico}/lista/atendidos")
def get_examenes_paciente_reciente(id_medico: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """SELECT DISTINCT p.id, p.nombre, p.apellido
        FROM Pacientes p
        INNER JOIN Examenes e ON p.id = e.id_paciente
        WHERE e.id_medico = %s;
        """
        cursor.execute(query, (id_medico,)) 
        result = cursor.fetchall()  # Cambiado a fetchall para obtener todos los resultados
        if not result:  # Cambiado para verificar si el resultado está vacío
            raise HTTPException(status_code=404, detail="No se encontraron exámenes para el paciente")
        return result

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al realizar la consulta")

    finally:
        cursor.close()
        conn.close()
