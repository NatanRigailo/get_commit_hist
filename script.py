import os
import requests
import datetime
from collections import Counter

# Obter configurações das variáveis de ambiente
TOKEN = os.getenv('GITLAB_TOKEN')
REPOSITORIO_IDS = os.getenv('GITLAB_REPO_IDS').split(',')  # IDs separados por vírgula
URL_BASE = os.getenv('GITLAB_API_URL', 'https://gitlab.com/api/v4/projects/')

# Verificar se todas as configurações necessárias estão presentes
if not TOKEN or not REPOSITORIO_IDS:
    raise ValueError("As variáveis de ambiente GITLAB_TOKEN e GITLAB_REPO_IDS são necessárias.")

# Função para obter commits de um repositório
def obter_commits(repo_id):
    url = f"{URL_BASE}{repo_id}/repository/commits"
    headers = {'Authorization': f'Bearer {TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao buscar commits do repositório {repo_id}: {response.status_code}")
        return []

# Contar commits por dia
contador_commits = Counter()

for repo_id in REPOSITORIO_IDS:
    commits = obter_commits(repo_id)
    for commit in commits:
        data = commit['created_at'].split('T')[0]
        contador_commits[data] += 1

# Mostrar resultados
for data, quantidade in contador_commits.items():
    print(f"{data}: {quantidade} commits")
