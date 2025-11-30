import requests
import json

# Configuración
BASE_URL = 'http://127.0.0.1:5000/api'
HEADERS = {'Content-Type': 'application/json'}
INSTITUCION_ID = 1 

def print_result(test_name, response, expected_status=[200, 201]):
    if response.status_code in expected_status:
        print(f"✅ {test_name}: OK ({response.status_code})")
        return True
    else:
        print(f"❌ {test_name}: FALLÓ ({response.status_code})")
        print(f"   Respuesta: {response.text}")
        return False

def verify_change(entity_name, field, expected_value, response_json):
    actual_value = response_json[entity_name].get(field)
    # CORRECCIÓN: Convertimos ambos a string para comparar sin importar si es int o str
    if str(actual_value) == str(expected_value):
        print(f"   -> 🔍 {entity_name.capitalize()} {field}: Actualizado correctamente a '{actual_value}'")
    else:
        print(f"   -> ⚠️ {entity_name.capitalize()} {field}: ERROR. Esperaba '{expected_value}', recibió '{actual_value}'")

def run_tests():
    print("="*70)
    print("🚀 TEST MAESTRO: CRUD COMPLETO DE TODO EL PERSONAL")
    print("="*70)

    # --- 1. SETUP ---
    print("\n--- 1. PREPARACIÓN ---")
    requests.get(f'{BASE_URL}/enums/')
    
    # Crear Grado
    res = requests.post(f'{BASE_URL}/grados-academicos/', json={"nombre": "Grado Test"}, headers=HEADERS)
    if not print_result("Crear Grado", res): return
    grado_id = res.json().get('id')

    # IDs para limpieza
    created_ids = {}

    # --- 2. INVESTIGADOR ---
    print("\n--- 2. INVESTIGADOR ---")
    payload = {"nombre": "Juan", "apellido": "Inv", "horas": 20, "gradoAcademicoId": grado_id, "institucionId": INSTITUCION_ID, "categoria": "A", "incentivo": "No", "dedicacion": "Parcial"}
    res = requests.post(f'{BASE_URL}/investigadores/', json=payload, headers=HEADERS)
    if print_result("Crear", res):
        id_inv = res.json()['investigador']['id']
        created_ids['investigadores'] = id_inv
        
        # Modificar
        res = requests.put(f'{BASE_URL}/investigadores/{id_inv}', json={"horas": 50, "categoria": "Super"}, headers=HEADERS)
        print_result("Modificar", res)
        verify_change('investigador', 'horas', 50, res.json())

    # --- 3. BECARIO ---
    print("\n--- 3. BECARIO ---")
    payload = {"nombre": "Ana", "apellido": "Bec", "horas": 30, "gradoAcademicoId": grado_id, "institucionId": INSTITUCION_ID, "rol": "doctorado"}
    res = requests.post(f'{BASE_URL}/becarios/', json=payload, headers=HEADERS)
    if print_result("Crear", res):
        id_bec = res.json()['becario']['id']
        created_ids['becarios'] = id_bec
        
        # Modificar (Cambiamos el rol y las horas)
        res = requests.put(f'{BASE_URL}/becarios/{id_bec}', json={"horas": 10, "rol": "pasante"}, headers=HEADERS)
        print_result("Modificar", res)
        verify_change('becario', 'rol', 'pasante', res.json())

    # --- 4. PROFESIONAL ---
    print("\n--- 4. PROFESIONAL ---")
    payload = {"nombre": "Pedro", "apellido": "Prof", "horas": 40, "gradoAcademicoId": grado_id, "institucionId": INSTITUCION_ID, "especialidad": "Dev", "descripcion": "Junior"}
    res = requests.post(f'{BASE_URL}/profesionales/', json=payload, headers=HEADERS)
    if print_result("Crear", res):
        id_prof = res.json()['profesional']['id']
        created_ids['profesionales'] = id_prof
        
        # Modificar (Cambiamos especialidad)
        res = requests.put(f'{BASE_URL}/profesionales/{id_prof}', json={"especialidad": "DevOps", "descripcion": "Senior"}, headers=HEADERS)
        print_result("Modificar", res)
        verify_change('profesional', 'especialidad', 'DevOps', res.json())

    # --- 5. SOPORTE ---
    print("\n--- 5. SOPORTE ---")
    payload = {"nombre": "Luis", "apellido": "Sop", "horas": 35, "gradoAcademicoId": grado_id, "institucionId": INSTITUCION_ID, "rol": "tecnico"}
    res = requests.post(f'{BASE_URL}/soportes/', json=payload, headers=HEADERS)
    if print_result("Crear", res):
        id_sop = res.json()['soporte']['id']
        created_ids['soportes'] = id_sop
        
        # Modificar (Cambiamos rol)
        res = requests.put(f'{BASE_URL}/soportes/{id_sop}', json={"rol": "administrativo"}, headers=HEADERS)
        print_result("Modificar", res)
        verify_change('soporte', 'rol', 'administrativo', res.json())

    # --- 6. VISITANTE ---
    print("\n--- 6. VISITANTE ---")
    payload = {"nombre": "Maria", "apellido": "Vis", "horas": 10, "gradoAcademicoId": grado_id, "institucionId": INSTITUCION_ID, "rol": "academica"}
    res = requests.post(f'{BASE_URL}/visitantes/', json=payload, headers=HEADERS)
    if print_result("Crear", res):
        id_vis = res.json()['visitante']['id']
        created_ids['visitantes'] = id_vis
        
        # Modificar (Cambiamos horas)
        res = requests.put(f'{BASE_URL}/visitantes/{id_vis}', json={"horas": 99}, headers=HEADERS)
        print_result("Modificar", res)
        verify_change('visitante', 'horas', 99, res.json())

    # --- 7. LIMPIEZA ---
    print("\n--- 7. LIMPIEZA ---")
    for endpoint, pid in reversed(created_ids.items()):
        requests.delete(f'{BASE_URL}/{endpoint}/{pid}')
        print(f"🗑️  Borrado {endpoint} ID={pid}")
    
    requests.delete(f'{BASE_URL}/grados-academicos/{grado_id}')
    print(f"🗑️  Borrado Grado ID={grado_id}")

    print("\n✅ PRUEBA FINALIZADA")

if __name__ == '__main__':
    try:
        requests.get(f'{BASE_URL}/hello')
        run_tests()
    except:
        print("❌ Error de conexión. Corre 'python app.py' primero.")