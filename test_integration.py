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
        pytest.fail(f"\n❌ ERRO: Servidor Flask não está rodando.")

def test_03_create_new_user_integration():
    """Testa a criação de um novo usuário via POST."""
    endpoint = f"{BASE_URL}/users"
    
    # CORREÇÃO: Gera um e-mail único para evitar conflitos em execuções repetidas
    unique_id = int(time.time())
    new_user_data = {
        "name": f"Integracao Teste {unique_id}",
        "email": f"integracao_{unique_id}@teste.com"
    }
    print(f"\nTestando endpoint POST: {endpoint}")

    try:
        response = requests.post(endpoint, json=new_user_data, timeout=TIMEOUT)
        response.raise_for_status() 

        assert response.status_code == 201
        data = response.json()
        
        assert data['name'] == new_user_data['name']
        assert data['email'] == new_user_data['email']
        assert 'id' in data
        print("✅ Criação de usuário via POST OK.")

    except requests.exceptions.ConnectionError:
        pytest.fail(f"\n❌ ERRO: Servidor Flask não está rodando.")
    except Exception as e:
        pytest.fail(f"❌ Falha no teste POST: {e}")

def test_04_get_user_by_id_integration():
    """Testa a busca de usuário por ID."""
    
    # Teste 4.1: Sucesso
    # Assume que o ID 1 sempre existe (o 'Fernando' dos dados iniciais)
    user_id_success = 1
    endpoint_success = f"{BASE_URL}/users/{user_id_success}"

    try:
        response_success = requests.get(endpoint_success, timeout=TIMEOUT)
        response_success.raise_for_status()
        data_success = response_success.json()
        
        assert response_success.status_code == 200
        assert data_success['id'] == user_id_success
        # Removemos a verificação do nome 'Fernando' se houver risco de edição, 
        # mas para este exercício pode manter.
        assert data_success['name'] == 'Fernando' 

    except requests.exceptions.ConnectionError:
        pytest.fail("❌ ERRO: Servidor Flask não está rodando.")
    
    # Teste 4.2: Falha
    user_id_fail = 99999 # Um número bem alto para garantir que não existe
    endpoint_fail = f"{BASE_URL}/users/{user_id_fail}"

    try:
        response_fail = requests.get(endpoint_fail, timeout=TIMEOUT)
        assert response_fail.status_code == 404
        data_fail = response_fail.json()
        assert "User not found" in data_fail['error']

    except requests.exceptions.ConnectionError:
        pytest.fail("❌ ERRO: Servidor Flask não está rodando.")
