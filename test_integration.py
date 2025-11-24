import requests
import pytest
import time
import json
import random # Importado para gerar dados aleatórios

BASE_URL = "http://127.0.0.1:5000"
TIMEOUT = 5

def test_01_api_is_running_and_users_endpoint():
    """Verifica se a API está no ar e o endpoint /users funciona."""
    try:
        # 1. Health Check
        response_root = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
        assert response_root.status_code == 200
        
        # 2. Teste da Rota /users
        response_users = requests.get(f"{BASE_URL}/users", timeout=TIMEOUT)
        data = response_users.json()

        assert response_users.status_code == 200
        assert isinstance(data, list)
        
        # CORREÇÃO: Usamos >= 10 para que o teste não quebre se novos usuários forem criados
        assert len(data) >= 10 
        
    except requests.exceptions.ConnectionError:
        pytest.fail(f"\n❌ ERRO DE CONEXÃO. O servidor NÃO ESTÁ RODANDO em {BASE_URL}. Inicie-o com 'python src/app.py'.")

def test_02_exchange_usd_to_brl_integration():
    """Testa a chamada em tempo real à AwesomeAPI."""
    endpoint = f"{BASE_URL}/exchange/usd-to-brl"
    
    time.sleep(1) 
    
    try:
        response = requests.get(endpoint, timeout=TIMEOUT)
        response.raise_for_status()

        assert response.status_code == 200
        data = response.json()
        
        assert float(data['bid']) > 1.0
        assert data['source'] == 'AwesomeAPI'

    except requests.exceptions.HTTPError as e:
        pytest.fail(f"❌ Falha HTTP: {e.response.status_code}")
    except requests.exceptions.ConnectionError:
        pytest.fail(f"❌ ERRO: Servidor Flask não está rodando.")

# ... (imports existentes: requests, pytest, BASE_URL, TIMEOUT)

def test_03_create_new_user_integration():
    """
    INTEGRAÇÃO: Testa a criação de um novo usuário via POST.
    Verifica se a API retorna 201 Created e o JSON do novo usuário.
    """
    endpoint = f"{BASE_URL}/users"
    new_user_data = {
        "name": "Usuario Integracao",
        "email": "integracao@teste.com"
    }
    
    print(f"\nTestando endpoint POST: {endpoint}")

    try:
        # Faz a chamada real à API
        response = requests.post(endpoint, json=new_user_data, timeout=TIMEOUT)
        
        # Verifica se a requisição foi bem sucedida
        assert response.status_code == 201, f"Falha ao criar usuário. Status: {response.status_code}"
        
        data = response.json()
        
        # Valida os dados retornados
        assert data['name'] == new_user_data['name']
        assert data['email'] == new_user_data['email']
        assert 'id' in data # Garante que o ID foi gerado automaticamente
        assert isinstance(data['id'], int)
        
        print("✅ Usuário criado com sucesso via integração.")

    except requests.exceptions.ConnectionError:
        pytest.fail(f"❌ ERRO: O servidor Flask não está acessível em {BASE_URL}. Inicie-o em outro terminal.")

def test_04_get_user_by_id_integration():
    """
    INTEGRAÇÃO: Testa a busca de um usuário existente por ID.
    Baseado na lista inicial em routes.py, o ID 1 deve ser 'Fernando'.
    """
    # Vamos buscar o usuário de ID 1, que sabemos que existe na lista inicial
    user_id = 1
    endpoint = f"{BASE_URL}/users/{user_id}"
    
    print(f"\nTestando endpoint GET ID: {endpoint}")

    try:
        response = requests.get(endpoint, timeout=TIMEOUT)
        
        assert response.status_code == 200, f"Usuário {user_id} não encontrado."
        
        data = response.json()
        
        # Valida se os dados correspondem ao registro esperado
        assert data['id'] == 1
        assert data['name'] == 'Fernando'
        assert data['email'] == 'fernando@example.com'
        
        print(f"✅ Usuário {data['name']} recuperado com sucesso.")

    except requests.exceptions.ConnectionError:
        pytest.fail(f"❌ ERRO: O servidor Flask não está acessível em {BASE_URL}.")
