# EJEMPLOS COMPLETOS DE ENDPOINTS - Guardian Zero 2 API

## 1. USUARIOS

### Obtener todos los usuarios
```
GET http://localhost:8000/v1/usuarios/
```

### Crear un usuario
```
POST http://localhost:8000/v1/usuarios/
Content-Type: application/json

{
  "Nombre": "Carlos López",
  "Email": "carlos@guardianmail.com",
  "Telefono": "555-0100",
  "Direccion": "Avenida Central 456",
  "Contraseña": "Pass@2024",
  "Rol": "Especialista"
}
```

### Obtener usuario por ID
```
GET http://localhost:8000/v1/usuarios/1
```

### Actualizar usuario
```
PUT http://localhost:8000/v1/usuarios/1
Content-Type: application/json

{
  "Nombre": "Carlos Manuel López",
  "Telefono": "555-0101",
  "Rol": "Administrador"
}
```

### Eliminar usuario
```
DELETE http://localhost:8000/v1/usuarios/1
```

---

## 2. ZONAS AFECTADAS

### Crear zona afectada
```
POST http://localhost:8000/v1/zonas-afectadas/
Content-Type: application/json

{
  "Nombre_Zona": "Sector Noreste",
  "Coordenadas": "10.4826,-77.0342",
  "Tipo_Zona": "Urbana",
  "Poblacion_Afectada": 8500,
  "Nivel_Gravedad": "Critico",
  "Impacto_Medio": "Inundación por desbordamiento de río"
}
```

### Actualizar zona
```
PUT http://localhost:8000/v1/zonas-afectadas/1
Content-Type: application/json

{
  "Nivel_Gravedad": "Moderado",
  "Poblacion_Afectada": 6000
}
```

---

## 3. RECURSOS

### Crear recurso (Viveres)
```
POST http://localhost:8000/v1/recursos/
Content-Type: application/json

{
  "Nombre_Recurso": "Kit de Alimentos Secos",
  "Categoria": "Viveres",
  "Cantidad_Disponible": 100,
  "Ubicacion_Almacen": "Almacén Central - Pasillo A"
}
```

### Crear recurso (Médico)
```
POST http://localhost:8000/v1/recursos/
Content-Type: application/json

{
  "Nombre_Recurso": "Botiquín de Primeros Auxilios",
  "Categoria": "Medico",
  "Cantidad_Disponible": 50,
  "Ubicacion_Almacen": "Almacén Central - Pasillo C"
}
```

### Crear recurso (Transporte)
```
POST http://localhost:8000/v1/recursos/
Content-Type: application/json

{
  "Nombre_Recurso": "Ambulancia",
  "Categoria": "Transporte",
  "Cantidad_Disponible": 5,
  "Ubicacion_Almacen": "Patio de Estacionamiento"
}
```

### Obtener todos los recursos
```
GET http://localhost:8000/v1/recursos/
```

### Actualizar cantidad disponible
```
PUT http://localhost:8000/v1/recursos/1
Content-Type: application/json

{
  "Cantidad_Disponible": 75
}
```

---

## 4. REPORTES

### Crear reporte de emergencia
```
POST http://localhost:8000/v1/reportes/
Content-Type: application/json

{
  "Lugar": "Calle Principal entre 5ta y 6ta Ave",
  "ID_Voluntario": 1,
  "ID_Zona_Afectada": 1,
  "Estatus": "Pendiente",
  "Prioridad": "Alta",
  "Descripcion_Emergencia": "Persona atrapada bajo escombros. Requiere rescate inmediato."
}
```

### Actualizar estado de reporte
```
PUT http://localhost:8000/v1/reportes/1
Content-Type: application/json

{
  "Estatus": "En Proceso",
  "Prioridad": "Critica"
}
```

### Obtener reportes
```
GET http://localhost:8000/v1/reportes/
GET http://localhost:8000/v1/reportes/1
```

---

## 5. VOLUNTARIOS

### Crear voluntario
```
POST http://localhost:8000/v1/voluntarios/
Content-Type: application/json

{
  "ID_Usuario": 1,
  "Nivel_Experiencia": "Intermedio",
  "Estatus": "Activo",
  "Horario_disponibilidad": "Lunes a Viernes 8:00-17:00, Fin de semana 9:00-18:00"
}
```

### Cambiar estado de voluntario
```
PUT http://localhost:8000/v1/voluntarios/1
Content-Type: application/json

{
  "Estatus": "En Mision"
}
```

### Obtener voluntarios
```
GET http://localhost:8000/v1/voluntarios/
GET http://localhost:8000/v1/voluntarios/1
```

---

## 6. ALERTAS

### Crear alerta de evacuación
```
POST http://localhost:8000/v1/alertas/
Content-Type: application/json

{
  "Titulo": "Evacuación del Sector Noreste",
  "Mensaje": "Se ha emitido orden de evacuación inmediata para el Sector Noreste debido a riesgo de derrumbes. Dirigirse a puntos de reunión designados.",
  "Nivel_Alerta": "Evacuacion",
  "ID_Emisor": 1
}
```

### Crear alerta informativa
```
POST http://localhost:8000/v1/alertas/
Content-Type: application/json

{
  "Titulo": "Centro de Acopio Habilitado",
  "Mensaje": "Se ha habilitado centro de acopio en el Parque Central para recibir donaciones de alimentos y medicinas.",
  "Nivel_Alerta": "Informativa",
  "ID_Emisor": 1
}
```

### Crear alerta de precaución
```
POST http://localhost:8000/v1/alertas/
Content-Type: application/json

{
  "Titulo": "Precaución en Carreteras",
  "Mensaje": "Carreteras principales presentan daños. Transitar con precaución y llevar provisiones.",
  "Nivel_Alerta": "Precaucion",
  "ID_Emisor": 2
}
```

### Obtener alertas
```
GET http://localhost:8000/v1/alertas/
GET http://localhost:8000/v1/alertas/1
```

---

## 7. BLOG

### Crear entrada de blog
```
POST http://localhost:8000/v1/blog/
Content-Type: application/json

{
  "Titulo": "Recomendaciones de Seguridad",
  "Descripcion": "Guía completa de preparación ante desastres naturales"
}
```

### Obtener blogs
```
GET http://localhost:8000/v1/blog/
GET http://localhost:8000/v1/blog/1
```

### Actualizar blog
```
PUT http://localhost:8000/v1/blog/1
Content-Type: application/json

{
  "Titulo": "Recomendaciones de Seguridad 2024",
  "Descripcion": "Guía actualizada de preparación ante desastres naturales"
}
```

---

## 8. ASIGNACIONES DE RECURSOS

### Asignar recursos a un reporte (Importante: Controla Inventario)
```
POST http://localhost:8000/v1/asignaciones/
Content-Type: application/json

{
  "ID_Reporte": 1,
  "ID_Recurso": 2,
  "Cantidad_Asignada": 10
}
```

Respuesta:
```json
{
  "status": "201",
  "mensaje": "Asignación creada correctamente",
  "data": {
    "ID": 1,
    "ID_Reporte": 1,
    "ID_Recurso": 2,
    "Cantidad_Asignada": 10,
    "Fecha_Entrega": "2024-03-27T10:30:00"
  }
}
```

### Obtener asignaciones
```
GET http://localhost:8000/v1/asignaciones/
GET http://localhost:8000/v1/asignaciones/1
```

### Devolver recursos (elimina asignación)
```
DELETE http://localhost:8000/v1/asignaciones/1
```

---

## FLUJO TÍPICO DE EMERGENCIA

1. **Crear Zona Afectada** (si no existe)
   ```
   POST /v1/zonas-afectadas/
   ```

2. **Crear Reporte de Emergencia**
   ```
   POST /v1/reportes/
   ```

3. **Asignar Voluntario**
   ```
   POST /v1/voluntarios/
   (si no existe) O PUT /v1/voluntarios/{id} para cambiar estatus
   ```

4. **Asignar Recursos**
   ```
   POST /v1/asignaciones/
   ```

5. **Emitir Alerta Pública** (si es necesario)
   ```
   POST /v1/alertas/
   ```

6. **Actualizar Estado del Reporte**
   ```
   PUT /v1/reportes/{id}
   ```

7. **Devolver/Reasignar Recursos**
   ```
   DELETE /v1/asignaciones/{id}
   O nuevo POST /v1/asignaciones/
   ```

---

## CÓDIGOS DE RESPUESTA

- **200 OK**: Solicitud exitosa
- **201 Created**: Recurso creado exitosamente
- **400 Bad Request**: Datos inválidos o cantidad insuficiente
- **404 Not Found**: Recurso no encontrado
- **500 Internal Server Error**: Error del servidor

## NOTAS IMPORTANTES

- El campo `Cantidad_Disponible` en recursos se decrementa automáticamente al crear asignaciones
- Se valida la disponibilidad de recursos antes de asignar
- Los campos opcionales se pueden omitir en PUT
- Las relaciones se mantienen automáticamente por SQLAlchemy
