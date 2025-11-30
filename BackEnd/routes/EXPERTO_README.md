# Módulo Experto de Información - Patrón Expert

## Descripción

El módulo `Experto.py` implementa el **Patrón Expert** (Experto en Información) para la obtención y serialización de datos de todos los objetos ORM a formato JSON.

### ¿Qué es el Patrón Expert?

El patrón Expert asigna la responsabilidad de realizar una tarea a la clase que tiene la información necesaria para llevarla a cabo. En este caso:
- **Modelos ORM**: Conocen sus atributos y relaciones
- **ExpertoInformacion**: Sabe cómo extraer y serializar esos atributos

## Características

✅ **Obtener todas las entidades** de la base de datos  
✅ **Obtener entidades por tipo** (modelo específico)  
✅ **Obtener un registro por ID**  
✅ **Serializar automáticamente** tipos especiales (datetime, date, bytes, Decimal)  
✅ **Obtener estadísticas** de la base de datos  
✅ **Exportar a JSON** formateado o compacto  

## Instalación

El módulo ya está incluido en el proyecto. No requiere dependencias adicionales más allá de las ya instaladas (SQLAlchemy, Flask, etc.).

## Uso

### 1. Obtener todas las entidades

```python
from Experto import ExpertoInformacion
from sqlalchemy.orm import Session

session = Session()  # Tu sesión de base de datos
experto = ExpertoInformacion(session)

# Obtener todas las entidades
datos = experto.obtener_todas_entidades()
json_string = experto.a_json(datos)
print(json_string)
```

### 2. Obtener estadísticas

```python
estadisticas = experto.obtener_estadisticas()
# Retorna: {"total_tablas": N, "total_registros": M, "tablas": {...}}
```

### 3. Obtener entidades por tipo

```python
from models_db import Persona

# Obtener todas las personas
personas_dict = experto.obtener_entidad_por_tipo(Persona)
```

### 4. Obtener un registro por ID

```python
from models_db import Persona

# Obtener la persona con ID 5
registro = experto.obtener_por_id(Persona, 5)
```

### 5. Convertir a JSON

```python
# JSON con indentación (legible)
json_indentado = experto.a_json(datos, indent=2)

# JSON compacto
json_compacto = experto.a_json(datos, indent=None)
```

## Endpoints API

Se han agregado tres endpoints que utilizan este módulo:

### `GET /api/datos/todas-entidades`
Obtiene todas las entidades de todas las tablas.

**Respuesta:**
```json
{
  "tabla_1": [...],
  "tabla_2": [...],
  ...
}
```

### `GET /api/datos/estadisticas`
Obtiene estadísticas de la base de datos.

**Respuesta:**
```json
{
  "total_tablas": 26,
  "total_registros": 150,
  "tablas": {
    "persona": 50,
    "grupo": 10,
    ...
  }
}
```

### `GET /api/datos/<tabla>/<id>`
Obtiene un registro específico.

**Ejemplo:** `GET /api/datos/persona/5`

**Respuesta:**
```json
{
  "persona": {
    "id": 5,
    "nombre": "Juan",
    "apellido": "Pérez",
    ...
  }
}
```

## Conversión de Tipos

El módulo maneja automáticamente la conversión de tipos no serializables:

| Tipo Original | Conversión |
|---|---|
| `datetime` | ISO format string |
| `date` | ISO format string |
| `time` | ISO format string |
| `Decimal` | float |
| `bytes` | UTF-8 string (o hex si no se puede decodificar) |
| `None` | null |
| Otros | str() |

## Ejemplos de Ejecución

Ver `ejemplo_experto.py` para ver ejemplos prácticos:

```bash
cd BackEnd
python ejemplo_experto.py
```

## Estructura del Código

```
Experto.py
├── ExpertoInformacion (clase principal)
│   ├── __init__(session)
│   ├── obtener_todas_entidades()
│   ├── obtener_entidad_por_tipo(model_class)
│   ├── obtener_por_id(model_class, id_valor)
│   ├── _serializar_objeto(objeto)
│   ├── _convertir_valor(valor)
│   ├── a_json(datos, indent)
│   └── obtener_estadisticas()
```

## Ventajas del Patrón Expert

✅ **Centralización**: Toda la lógica de serialización en un solo lugar  
✅ **Reutilización**: Se puede usar en múltiples endpoints  
✅ **Mantenibilidad**: Cambios en la serialización se hacen en un solo lugar  
✅ **Escalabilidad**: Fácil agregar nuevos métodos de obtención/serialización  
✅ **Testabilidad**: El módulo es fácil de testear de forma independiente  

## Extensiones Futuras

- Filtros avanzados (WHERE clauses)
- Paginación
- Ordenamiento
- Relaciones anidadas (eager loading)
- Caché de resultados
