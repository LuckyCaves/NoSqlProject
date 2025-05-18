# Health Data Integration Platform
## Proyecto de Bases de Datos no Relacionales

---

## Resumen del Proyecto

Plataforma de integración de datos médicos utilizando tres bases de datos NoSQL:
- **Dgraph** (Grafos)
- **MongoDB** (Documentos)
- **Cassandra** (Columnar)

Cada base de datos optimizada para diferentes aspectos del sistema de salud.

---

## Dgraph: Modelo de Grafos

Ideal para representar relaciones complejas entre entidades médicas.

### Casos de uso principales:
- Relaciones médico-paciente
- Historial médico de pacientes
- Recomendación de médicos según especialidad
- Recomendación de tratamientos basados en diagnósticos similares
- Detección de interacciones medicamentosas
- Relaciones familiares y predisposiciones genéticas

---

## Dgraph: Modelo de Datos

### Nodos principales:
- Patient
- Doctor
- Specialty
- Consultation
- Diagnosis
- Treatment
- Medication
- SideEffect
- Disease

### Relaciones clave:
- attends_to / has_patient (Doctor ↔ Patient)
- has_consultation (Patient → Consultation)
- resulted_in_diagnosis (Consultation → Diagnosis)
- prescribed_treatment (Diagnosis → Treatment)
- family_relation (Patient → Patient)

---

## MongoDB: Modelo de Documentos

Ideal para almacenar registros médicos estructurados con datos anidados.

### Casos de uso principales:
- Registros completos de pacientes
- Resultados de laboratorio
- Historial de prescripciones
- Plantillas de formularios médicos
- Registro de alergias

---

## MongoDB: Colecciones

### Colección patients:
```json
{
  "patient_id": "000001",
  "full_name": "Nombre Paciente",
  "dob": "1990-01-01",
  "gender": "M",
  "medical_history": "...",
  "emergency_contact": {
    "name": "Contacto Emergencia",
    "phone": "1234567890",
    "relationship": "Familiar"
  },
  "lab_results": [...],
  "prescriptions": [...],
  "forms_filled": [...],
  "allergies": [...]
}
```
---

## MongoDB: Consultas Principales

### Historial de prescripciones en un rango de fechas:
```javascript
db.patients.aggregate([
  { $match: { patient_id: "000001" } },
  {
    $project: {
      prescriptions: {
        $filter: {
          input: "$prescriptions",
          as: "presc",
          cond: {
            $and: [
              { $gte: ["$$presc.date_prescribed", ISODate("2025-03-01")] },
              { $lte: ["$$presc.date_prescribed", ISODate("2025-04-01")] }
            ]
          }
        }
      }
    }
  }
])
```

---

## Cassandra: Modelo Columnar

Ideal para escribir datos de alta velocidad y distribuidos.

### Casos de uso principales:
- Gestión de citas médicas
- Seguimiento de signos vitales en tiempo real
- Gestión de usuarios y cuentas
- Sistema de alertas médicas

---

## Cassandra: Tablas Principales

### Diseño orientado a consultas específicas:
- patients (PK: patient_id)
- doctors (PK: doctor_id)
- accounts (PK: account_id)
- appointments_by_patient (PK: patient_id, CK: appointment_id)
- appointments_by_doctor (PK: doctor_id, CK: appointment_id)
- vital_signs_by_account_date (PK: account_id, CK: vital_sign_id)
- alerts_by_account_date (PK: account_id, CK: date, alert_id)

---

## Cassandra: Optimizaciones

### Estructura de claves:
- **Partition Keys simples**: Localización eficiente de registros
- **Partition Keys compuestas**: Para relaciones específicas
- **Clustering Keys con TIMEUUID**: Ordenamiento cronológico natural
- **Clustering jerárquico**: Para consultas específicas por tipo

---

## Comparativa de Bases de Datos

| Base de Datos | Fortaleza Principal | Aplicación en el Sistema |
|---------------|---------------------|--------------------------|
| **Dgraph**    | Relaciones complejas | Red de conocimiento médico |
| **MongoDB**   | Documentos flexibles | Historiales médicos completos |
| **Cassandra** | Escritura de alta velocidad | Datos en tiempo real y citas |

---

## Conclusión

El sistema aprovecha las fortalezas de cada base de datos NoSQL:

- **Dgraph**: Excelente para mostrar conexiones entre entidades médicas y recomendaciones basadas en relaciones.
- **MongoDB**: Ideal para almacenar registros médicos completos con estructura flexible.
- **Cassandra**: Óptima para datos en tiempo real, citas y alertas con alta disponibilidad.

La integración de estas tres bases de datos permite crear una plataforma robusta y escalable para el sector salud.