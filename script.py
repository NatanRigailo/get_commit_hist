import requests
from collections import Counter
import os

# Obter configurações das variáveis de ambiente
TOKEN = os.getenv('GITLAB_TOKEN')
REPOSITORIO_IDS = os.getenv('GITLAB_REPO_IDS').split(',')  # IDs separados por vírgula
URL_BASE = os.getenv('GITLAB_API_URL', 'https://gitlab.com/api/v4/projects/')

# Verificar se todas as configurações necessárias estão presentes
if not TOKEN or not REPOSITORIO_IDS:
    raise ValueError("As variáveis de ambiente GITLAB_TOKEN e GITLAB_REPO_IDS são necessárias.")

# Função para obter commits de um repositório com paginação
def obter_commits(repo_id):
    commits = []
    url = f"{URL_BASE}{repo_id}/repository/commits"
    headers = {'Authorization': f'Bearer {TOKEN}'}
    page = 1

    while True:
        params = {'page': page, 'per_page': 100}  # 100 é o máximo permitido por página
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Erro ao buscar commits do repositório {repo_id}: {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        commits.extend(data)
        page += 1
    
    return commits

# Processar commits de cada repositório
relatorios = {}
contador_total = Counter()

for repo_id in REPOSITORIO_IDS:
    print(f"Buscando commits para o repositório {repo_id}...")
    commits = obter_commits(repo_id)
    contador = Counter(commit['created_at'].split('T')[0] for commit in commits)
    relatorios[repo_id] = contador
    contador_total.update(contador)

# Mostrar resultados
for repo_id, contador in relatorios.items():
    print(f"\nRelatório de commits para o repositório {repo_id}:")
    for data, quantidade in contador.items():
        print(f"{data}: {quantidade} commits")

print("\nRelatório combinado de todos os repositórios:")
for data, quantidade in contador_total.items():
    print(f"{data}: {quantidade} commits")

