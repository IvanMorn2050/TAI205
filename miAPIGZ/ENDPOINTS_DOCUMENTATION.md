# Guardian Zero 2 API - Endpoints Documentation

## Estructura del Proyecto

```
app/
├── data/
│   ├── db.py                 # Configuración de BD (MySQL)
│   ├── guardian_models.py    # Modelos SQLAlchemy (15 tablas)
│   ├── usuario.py            # Modelo anterior
│   └── database.py           # BD ficticia anterior
├── models/
│   ├── usuarios.py           # Anterior
│   └── guardian_schemas.py   # Modelos Pydantic para validación
├── routers/
│   ├── usuarios.py           # Anterior
│   ├── varios.py             # Anterior
│   ├── guardians_usuarios.py
│   ├── guardians_zonas.py
│   ├── guardians_recursos.py
│   ├── guardians_reportes.py
│   ├── guardians_voluntarios.py
│   ├── guardians_alertas.py
│   ├── guardians_blog.py
│   └── guardians_asignaciones.py
├── security/
│   └── auth.py
└── main.py                   # Punto de entrada
```

## Endpoints por Entidad

### 1. USUARIOS - `/v1/usuarios`
- `GET /` - Obtener todos los usuarios
- `GET /{id}` - Obtener usuario por ID
- `POST /` - Crear nuevo usuario
- `PUT /{id}` - Actualizar usuario
- `DELETE /{id}` - Eliminar usuario

### 2. ZONAS AFECTADAS - `/v1/zonas-afectadas`
- `GET /` - Obtener todas las zonas
- `GET /{id}` - Obtener zona por ID
- `POST /` - Crear nueva zona
- `PUT /{id}` - Actualizar zona
- `DELETE /{id}` - Eliminar zona

### 3. RECURSOS - `/v1/recursos`
- `GET /` - Obtener todos los recursos
- `GET /{id}` - Obtener recurso por ID
- `POST /` - Crear nuevo recurso
- `PUT /{id}` - Actualizar recurso
- `DELETE /{id}` - Eliminar recurso

### 4. REPORTES - `/v1/reportes`
- `GET /` - Obtener todos los reportes
- `GET /{id}` - Obtener reporte por ID
- `POST /` - Crear nuevo reporte
- `PUT /{id}` - Actualizar reporte
- `DELETE /{id}` - Eliminar reporte

### 5. VOLUNTARIOS - `/v1/voluntarios`
- `GET /` - Obtener todos los voluntarios
- `GET /{id}` - Obtener voluntario por ID
- `POST /` - Crear nuevo voluntario
- `PUT /{id}` - Actualizar voluntario
- `DELETE /{id}` - Eliminar voluntario

### 6. ALERTAS - `/v1/alertas`
- `GET /` - Obtener todas las alertas
- `GET /{id}` - Obtener alerta por ID
- `POST /` - Crear nueva alerta
- `PUT /{id}` - Actualizar alerta
- `DELETE /{id}` - Eliminar alerta

### 7. BLOG - `/v1/blog`
- `GET /` - Obtener todos los blogs
- `GET /{id}` - Obtener blog por ID
- `POST /` - Crear nuevo blog
- `PUT /{id}` - Actualizar blog
- `DELETE /{id}` - Eliminar blog

### 8. ASIGNACIONES DE RECURSOS - `/v1/asignaciones`
- `GET /` - Obtener todas las asignaciones
- `GET /{id}` - Obtener asignación por ID
- `POST /` - Crear nueva asignación (con control de inventario)
- `DELETE /{id}` - Eliminar asignación (devuelve recursos)

## Ejemplos de Uso

### Crear un Usuario
```json
POST /v1/usuarios/
{
  "Nombre": "Juan Pérez",
  "Email": "juan@example.com",
  "Telefono": "1234567890",
  "Direccion": "Calle Principal 123",
  "Contraseña": "segura123",
  "Rol": "Voluntario"
}
```

### Crear una Zona Afectada
```json
POST /v1/zonas-afectadas/
{
  "Nombre_Zona": "Barrio San Luis",
  "Coordenadas": "10.5,-77.5",
  "Tipo_Zona": "Urbana",
  "Poblacion_Afectada": 5000,
  "Nivel_Gravedad": "Critico",
  "Impacto_Medio": "Inundación"
}
```

### Crear un Recurso
```json
POST /v1/recursos/
{
  "Nombre_Recurso": "Tienda de Campaña",
  "Categoria": "Viveres",
  "Cantidad_Disponible": 50,
  "Ubicacion_Almacen": "Almacén Central"
}
```

### Crear una Asignación de Recursos
```json
POST /v1/asignaciones/
{
  "ID_Reporte": 1,
  "ID_Recurso": 1,
  "Cantidad_Asignada": 10
}
```

## Base de Datos

- **Nombre**: `guardian_zero2`
- **Motor**: MySQL
- **Conexión**: `mysql+pymysql://root:@localhost:3306/guardian_zero2`

### Tablas Principales (15 total)
1. **usuario** - Registros de usuarios con roles
2. **blog** - Blogs informativos
3. **conocimientos_tecnicos** - Catálogo de habilidades
4. **puestos** - Tipos de puestos
5. **tipo_evidencia** - Tipos de archivos de evidencia
6. **zona_afectada** - Áreas geográficas afectadas
7. **recursos** - Inventario de recursos
8. **contenido_blog** - Contenido de blogs
9. **curriculum** - CVs de voluntarios
10. **voluntario** - Registro de voluntarios
11. **reporte** - Reportes de emergencia
12. **asignacion_recursos** - Asignaciones de recursos
13. **alertas** - Alertas del sistema
14. **detalle_conocimientos** - Relación CV-Conocimientos
15. **evidencia** - Archivos de evidencia

## Respuestas Estándar

Éxito (200):
```json
{
  "status": "200",
  "total": 5,
  "data": [...]
}
```

Creación (201):
```json
{
  "status": "201",
  "mensaje": "Recurso creado correctamente",
  "data": {...}
}
```

Error (404):
```json
{
  "detail": "Usuario no encontrado"
}
```

## Cambios Realizados

✅ Actualizado `db.py` para MySQL
✅ Creado `guardian_models.py` con 15 modelos SQLAlchemy
✅ Creado `guardian_schemas.py` con modelos Pydantic
✅ Creados 8 routers con endpoints CRUD
✅ Actualizado `main.py` para incluir todos los routers
✅ Control de inventario en asignaciones de recursos
✅ Validación de datos con Pydantic

## Próximos Pasos

1. Actualizar requirements.txt con dependencias necesarias
2. Crear la BD en MySQL
3. Ejecutar las migraciones
4. Probar los endpoints con Postman o similar
5. Agregar autenticación JWT si es necesario
6. Agregar filtrado y paginación avanzada
