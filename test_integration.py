import requests
import pytest
import time
import json
import random # Adicione esta importação se ainda não tiver

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
        # Ajustamos para >= 10 para não falhar após o POST de outros testes
        assert len(data) >= 10
        
    except requests.exceptions.ConnectionError:
        # CORREÇÃO DE SINTAXE (Removendo o \n da f-string)
        pytest.fail(f"❌ ERRO DE CONEXÃO. O servidor NÃO ESTÁ RODANDO em {BASE_URL}. Inicie-o com 'python src/app.py'.")

def test_02_exchange_usd_to_brl_integration():
    """Testa a chamada em tempo real à AwesomeAPI (Integração Externa)."""
    endpoint = f"{BASE_URL}/exchange/usd-to-brl"
    
    # Adiciona um pequeno delay para ser educado com a AwesomeAPI
    time.sleep(1) 
    
    try:
        response = requests.get(endpoint, timeout=TIMEOUT)
        response.raise_for_status() # Lança exceção se for 4xx/5xx

        assert response.status_code == 200
        data = response.json()
        
        # Verifica se o valor de 'bid' é um número (float) válido (maior que 1.0)
        assert float(data['bid']) > 1.0
        assert data['source'] == 'AwesomeAPI'

    except requests.exceptions.HTTPError as e:
        pytest.fail(f"❌ Falha HTTP da AwesomeAPI ou da sua API (Status: {e.response.status_code}).")
    except requests.exceptions.ConnectionError:
        # CORREÇÃO DE SINTAXE (Removendo o \n da f-string)
        pytest.fail("❌ ERRO: Servidor Flask não está rodando. Inicie com 'python src/app.py'.")

def test_03_create_new_user_integration():
    """Testa a criação de um novo usuário via POST."""
    endpoint = f"{BASE_URL}/users"
    
    # Gera um e-mail único para garantir que o teste seja repetível
    unique_id = int(time.time() * 1000)
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
        pytest.fail(f"❌ ERRO: Servidor Flask não está rodando em {BASE_URL}. Inicie-o com 'python src/app.py'.")
    except Exception as e:
        pytest.fail(f"❌ Falha no teste POST: {e}")


def test_04_get_user_by_id_integration():
    """Testa a busca de usuário por ID (sucesso e falha)."""
    
    # Teste 4.1: Sucesso (Buscando o usuário de ID 1)
    user_id_success = 1
    endpoint_success = f"{BASE_URL}/users/{user_id_success}"

    try:
        response_success = requests.get(endpoint_success, timeout=TIMEOUT)
        response_success.raise_for_status()
        
        data_success = response_success.json()
        
        assert response_success.status_code == 200
        assert data_success['id'] == user_id_success
        assert data_success['name'] == 'Fernando' # Primeiro usuário na lista
        print("✅ Busca por ID (Existente) OK.")

    except requests.exceptions.ConnectionError:
        pytest.fail("❌ ERRO: Servidor Flask não está rodando.")
    
    # Teste 4.2: Falha (Buscando um ID que não existe)
    user_id_fail = 99999
    endpoint_fail = f"{BASE_URL}/users/{user_id_fail}"

    try:
        response_fail = requests.get(endpoint_fail, timeout=TIMEOUT)
        
        assert response_fail.status_code == 404
        data_fail = response_fail.json()
        
        assert "User not found" in data_fail['error']
        print("✅ Busca por ID (Não Existente) OK (Retornou 404).")

    except requests.exceptions.ConnectionError:
        pytest.fail("❌ ERRO: Servidor Flask não está rodando.")


def test_05_delete_user_integration():
    """
    INTEGRAÇÃO: Testa a remoção de um usuário por ID.
    Busca o ID 10 da lista inicial (Camila) e o remove.
    """
    user_id_to_delete = 10
    endpoint_delete = f"{BASE_URL}/users/{user_id_to_delete}"
    
    print(f"\nTestando endpoint DELETE: {endpoint_delete}")

    try:
        # 1. Tenta deletar o usuário
        response_delete = requests.delete(endpoint_delete, timeout=TIMEOUT)
        
        # O Flask deve retornar 204 No Content para exclusão bem sucedida
        assert response_delete.status_code == 204
        assert response_delete.text == '' # 204 não deve ter corpo

        print("✅ Usuário deletado com sucesso (Status 204).")

    except requests.exceptions.ConnectionError:
        pytest.fail("❌ ERRO: Servidor Flask não está rodando.")
    
    # 2. Testa se o usuário realmente sumiu (Verificação de 404)
    endpoint_check = f"{BASE_URL}/users/{user_id_to_delete}"
    print(f"Verificando exclusão com GET: {endpoint_check}")

    try:
        response_check = requests.get(endpoint_check, timeout=TIMEOUT)
        
        # A requisição GET deve agora falhar e retornar 404
        assert response_check.status_code == 404
        data_check = response_check.json()
        assert "User not found" in data_check['error']
        
        print("✅ Verificação de exclusão OK (Retornou 404).")

    except requests.exceptions.ConnectionError:
        pytest.fail("❌ ERRO: Servidor Flask não está rodando.")
    except Exception as e:
        pytest.fail(f"❌ Falha no teste DELETE/Verificação: {e}")
