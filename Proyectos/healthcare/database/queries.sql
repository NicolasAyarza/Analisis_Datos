-- psql -U postgres -d healthcare_analytics -f database/queries.sql para ejecutar todas las consultas

-- Pregunta 1: ¿Cuántos pacientes atiende la clínica?
SELECT COUNT(DISTINCT(nombre))
FROM pacientes;
/*
Respuesta: 
El total de pacientes diferentes que atiende la clinica es de 19.847.
El total con pacientes repetidos es de 20.000.
*/

-- pREGUNTA 2: ¿Cuáles son las especialidades con mayor demanda?
SELECT
	es.especialidad AS "Nombre especialidad",
	COUNT(ci.medico_id) AS "Total citas"
FROM citas ci 
JOIN medicos me 
    ON me.medico_id = ci.medico_id
JOIN especialidades es 
    ON es.especialidad_id = me.especialidad_id
GROUP BY es.especialidad
ORDER BY COUNT(ci.medico_id) DESC;
/*
Respuesta: 
El top 3 especialidades con mayor demanda son:
    1. Medicina General con 48.218 citas.
    2. Pediatría con 28.384 citas.
    3. Traumatología con 24.320 citas.
*/

-- Pregunta 3: ¿Cuál es el tiempo promedio de espera?
SELECT
	es.especialidad AS "Nombre Especialidad",
	TRUNC(AVG(tiempo_espera)) AS "Espera Promedio (minutos)"
FROM citas ci 
JOIN medicos me 
    ON me.medico_id = ci.medico_id
JOIN especialidades es 
    ON es.especialidad_id = me.especialidad_id
JOIN atenciones ate 
    ON ate.cita_id = ci.cita_id
GROUP BY es.especialidad
ORDER BY AVG(tiempo_espera) DESC
/*
Respuesta:
El top 3 con mayor tiempo de espera promedio son:
    1. Cardiología con 47 minutos.
    2. Traumatología con 44 minutos.
    3. Neurología con 39 minutos. 
*/

-- Pregunta 4: ¿Que medicos tienen mayor carga asistencial?
SELECT
	me.nombre AS "Nombre",
	COUNT(ci.cita_id) AS "Cantidad Citas Atendidas",
	es.especialidad,
	RANK() OVER (
		PARTITION BY es.especialidad 
		ORDER BY COUNT(ci.cita_id) DESC
	) AS "Ranking Especialidad"
FROM citas ci 
JOIN medicos me 
	ON me.medico_id = ci.medico_id
JOIN especialidades es 
	ON es.especialidad_id = me.especialidad_id
WHERE ci.estado = 'Atendida'
GROUP BY me.medico_id, me.nombre, es.especialidad
ORDER BY COUNT(ci.estado) DESC, "Ranking Especialidad";

/*
Respuesta: 
El medico Dr(a). Fabián Matías Cortés Leal es el que tiene la mayor carga con 4.329 siendo el top 1 en neurología
El medico Dr(a). Ricardo Romero Cubillos es el segundo con mayor carga con 4.231 siendo el top 2 de neurología
El mdeico Dr(a). Benjamín Herrera Bastías es el tercero con mayor carga con 3. 431 siendo el top 1 de endocrinología
*/

-- Pregunta 5: ¿Cuáles son los principales diagnósticos?
-- Dos formas de realizar la consulta con mismos resultados
SELECT
	di.diagnostico,
	COUNT(ate.atencion_id)	
FROM diagnosticos di
JOIN atenciones ate 
	ON di.atencion_id = ate.atencion_id
GROUP BY di.diagnostico
ORDER BY COUNT(ate.atencion_id) DESC;
------------------------------------------
SELECT
	diagnostico,
	COUNT(codigo_cie10)
FROM diagnosticos
GROUP BY diagnostico
ORDER BY COUNT(codigo_cie10) DESC
limit 5
/*
Respuesta: 
Los principales diagnosticos son: 
    1. Rinofaringitis aguda	con 12.365 casos
    2. Cefalea con 12.252 casos
    3. Diarrea funcional con 12.232 casos
*/

-- Pregunta 6: ¿Qué porcentaje de citas termina en inasistencia?
SELECT 
	(SUM(
		CASE 
			WHEN estado = 'No asistió' THEN 1
			Else 0
		END
	)/COUNT(*)) * 100.0 -- Algo falla el resultado siempre da 0
FROM citas

-- Pregunta 7: ¿Qué servicios generan mayores ingresos?
SELECT 
	se.servicio,
	SUM(ate.costo_atencion)
FROM atenciones ate
JOIN citas ci ON
	ci.cita_id = ate.cita_id
JOIN servicios se ON
	se.servicio_id = ci.servicio_id
GROUP BY se.servicio
ORDER BY SUM(ate.costo_atencion) DESC;

/*
Respuesta:
Los servicios que generan mayor ingreso son:
    1. Endoscopía con 579.518.000 de pesos
    2. Biopsia de Piel con 480.804.100 de pesos
    3. Ecocardiograma con 429.588.000 de pesos
*/