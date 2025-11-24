import requests
import pytest
import time
import json

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
        assert len(data) == 10
        
    except requests.exceptions.ConnectionError:
        pytest.fail(f"\n❌ ERRO DE CONEXÃO. O servidor NÃO ESTÁ RODANDO em {BASE_URL}. Inicie-o com 'python src/app.py'.")

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
        pytest.fail(f"\n❌ ERRO: Servidor Flask não está rodando. Inicie com 'python src/app.py'.")