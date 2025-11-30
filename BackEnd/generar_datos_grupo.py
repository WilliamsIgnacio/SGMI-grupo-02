"""Script para generar datos de grupo de prueba"""
import urllib.request
import json

# Datos del grupo a crear
grupo_data = {
    "sigla": "GII",
    "nombre": "Grupo de Investigación en Ingeniería",
    "objetivos": "Desarrollar investigación científica y tecnológica en el área de ingeniería de software y sistemas",
    "organigrama": "Director: Juan Pérez, Subdirector: María López",
    "consejo_ejecutivo": "Juan Pérez, María López, Carlos Gómez",
    "unidad_academica": "Facultad de Ingeniería"
}

url = "http://127.0.0.1:5000/api/organizaciones"

# Crear la petición POST
req = urllib.request.Request(
    url,
    data=json.dumps(grupo_data).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
    method='POST'
)

try:
    with urllib.request.urlopen(req) as response:
        data = response.read().decode('utf-8')
        status_code = response.status
        
        print(f"Status Code: {status_code}")
        print(f"\nRespuesta:")
        print(json.dumps(json.loads(data), indent=2, ensure_ascii=False))
        
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")
    error_data = e.read().decode('utf-8')
    print(f"Error response: {error_data}")
except Exception as e:
    print(f"Error al hacer la petición: {e}")
