"""Script de prueba para el endpoint obtener_datos_grupo_por_fecha"""
import urllib.request
import json

# Probar primero el grupo 1
url = "http://127.0.0.1:5000/api/experto/grupo/1"

try:
    with urllib.request.urlopen(url) as response:
        data = response.read().decode('utf-8')
        status_code = response.status
        
        print(f"Status Code: {status_code}")
        print(f"\nRespuesta JSON:")
        print(json.dumps(json.loads(data), indent=2, ensure_ascii=False))
        
except Exception as e:
    print(f"Error al hacer la petición: {e}")
