import json
import requests

# Base API URL
base_api_url = 'https://api.promeritum.org.mx/vacancies'

# Initial request parameters
params = {'status': 'published', 'limit': 12, 'skip': 0}

# List to store all vacancies
all_vacancies = []

# Requesting and collecting all vacancies from the API
while True:
    response = requests.get(base_api_url, params=params)
    data = response.json()
    vacancies = data.get('data', [])
    
    if not vacancies:
        break
    
    all_vacancies.extend(vacancies)
    params['skip'] += len(vacancies)

# Filtering vacancies based on specified criteria
filtered_vacancies = []

for vacancy in all_vacancies:
    if (vacancy['location']['state'] == 'Ciudad de México' and
        any(keyword in ' '.join(vacancy['degree']) for keyword in ['Ing', 'TI', 'Sistemas', 'Computación'])):
        filtered_vacancies.append(vacancy)

# Extracting specific fields from each filtered vacancy
filtered_vacancies_data = []

for vacancy in filtered_vacancies:
    filtered_vacancy = {
        "empresa": vacancy["company"]["name"],
        "vacante": vacancy["name"],
        "duracion": vacancy["duration"],
        "lugar": vacancy["location"]["city"],
        "modalidad": vacancy["modality"],
        "sueldo": vacancy["scholarship"],
        "actividades": vacancy["activities"],
        "comentarios": vacancy["comments"],
        "carreras": vacancy["degree"],
        "habilidades": [knowledge["name"] for knowledge in vacancy["knowledges"]]
    }
    filtered_vacancies_data.append(filtered_vacancy)

# Saving filtered vacancies with specified fields to a new JSON file
with open('vacantes_filtradas_campos.json', 'w', encoding="utf-8") as file:
    json.dump(filtered_vacancies_data, file, indent=4, ensure_ascii=False)

print(f'Número total de vacantes encontradas: {len(all_vacancies)}')
print(f'Número total de vacantes filtradas: {len(filtered_vacancies)}')
