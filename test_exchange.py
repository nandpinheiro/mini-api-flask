import pytest
import json
import requests # Essencial para referenciar requests.RequestException
from unittest.mock import patch, Mock
from src.app import create_app

# Exemplo de resposta simulada da AwesomeAPI para USD-BRL
MOCK_SUCCESS_RESPONSE_USD_BRL = {
    "USDBRL": {
        "code": "USD",
        "codein": "BRL",
        "name": "Dólar Americano/Real Brasileiro",
        "high": "5.4500",
        "low": "5.4300",
        "bid": "5.4410", # <--- Valor que você testará
        "ask": "5.4415",
        "timestamp": "1700000000",
        "create_date": "2023-11-15 10:00:00"
    }
}

# ======================================
# FIXTURES E MOCK DADOS
# ======================================

@pytest.fixture
def client():
    """Fixture para o cliente de teste do Flask (Unitário)."""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Resposta de sucesso esperada da AwesomeAPI (USDBRL)
MOCK_SUCCESS_RESPONSE = {
    "USDBRL": {
        "code": "USD",
        "codein": "BRL",
        "name": "Dólar Americano/Real Brasileiro",
        "high": "5.4500",
        "low": "5.4300",
        "bid": "5.4410", # Valor usado no teste
        "ask": "5.4415",
        "timestamp": "1700000000",
        "create_date": "2023-11-15 10:00:00"
    }
}

# ======================================
# TESTES DE ROTA /users
# ======================================

def test_get_all_users_success(client):
    """Teste unitário para listar todos os usuários."""
    response = client.get('/users')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 10
    assert data[0]['name'] == 'Fernando'

# ======================================
# TESTES DE ROTA /exchange/usd-to-brl
# ======================================

@patch('requests.get')
def test_exchange_usd_to_brl_success(mock_get, client):
    """Teste unitário: Sucesso na chamada à AwesomeAPI."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_SUCCESS_RESPONSE
    mock_get.return_value = mock_response

    response = client.get('/exchange/usd-to-brl')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['from'] == 'USD'
    assert data['to'] == 'BRL'
    assert data['bid'] == '5.4410' # Valor mockado

@patch('requests.get')
def test_exchange_usd_to_brl_connection_error(mock_get, client):
    """Teste unitário: Simula falha de conexão (Timeout, DNS, etc.)."""
    # Esta linha finalmente deve funcionar, pois 'requests' agora está importado
    mock_get.side_effect = requests.RequestException("Simulated connection error")

    response = client.get('/exchange/usd-to-brl')
    data = json.loads(response.data)

    assert response.status_code == 502 # Bad Gateway
    assert data['error'] == "Failed to fetch exchange rate from upstream service"

@patch('requests.get')
def test_exchange_usd_to_brl_api_http_error(mock_get, client):
    """Teste unitário: Simula um erro HTTP 4xx/5xx da AwesomeAPI."""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = requests.HTTPError("Simulated HTTP Error")
    mock_get.return_value = mock_response

    response = client.get('/exchange/usd-to-brl')
    data = json.loads(response.data)

    assert response.status_code == 502
    assert data['error'] == "Failed to fetch exchange rate from upstream service"

@patch('requests.get')
def test_exchange_usd_to_brl_invalid_json_format(mock_get, client):
    """Teste unitário: Simula JSON retornado sem a chave esperada (ex: USDBRL)."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {} # Retorno vazio
    mock_get.return_value = mock_response

    response = client.get('/exchange/usd-to-brl')
    data = json.loads(response.data)

    # O código no routes.py deve detectar isso e retornar 502
    assert response.status_code == 502
    assert data['error'] == "Unexpected response format from upstream service"

# ======================================
# TESTES DE ROTA /users (POST)
# ======================================

def test_add_user_success(client):
    """Teste unitário para adicionar um novo usuário via POST."""
    new_user_data = {
        "name": "Maria Teste",
        "email": "maria@teste.com"
    }
    
    # 1. Faz a requisição POST com o corpo JSON
    response = client.post('/users', 
                           data=json.dumps(new_user_data), # Converte o dicionário Python para string JSON
                           content_type='application/json')
    
    data = json.loads(response.data)

    # 2. Verifica se o status de criação (201) foi retornado
    assert response.status_code == 201
    
    # 3. Verifica se o usuário foi criado corretamente
    assert data['name'] == "Maria Teste"
    assert data['email'] == "maria@teste.com"
    
    # O ID deve ser gerado sequencialmente (será 11 no primeiro teste do arquivo)
    assert 'id' in data

def test_add_user_invalid_data(client):
    """Teste unitário para falha ao adicionar usuário com dados inválidos/ausentes."""
    # Simula a falta do campo 'email'
    invalid_user_data = {
        "name": "Teste Invalido"
        # 'email' está faltando
    }
    
    # 1. Faz a requisição POST com o corpo JSON inválido
    response = client.post('/users', 
                           data=json.dumps(invalid_user_data),
                           content_type='application/json')
    
    data = json.loads(response.data)

    # 2. Verifica se o status de erro (400 Bad Request) foi retornado
    assert response.status_code == 400
    
    # 3. Verifica se a mensagem de erro é clara (depende de como seu Flask trata isso)
    # Assumimos que sua API retorna um JSON com a chave 'error'
    assert 'error' in data
    assert "Missing required fields" in data['error'] or "Invalid data format" in data['error']


# @patch intercepta a chamada requests.get em src.routes
@patch('requests.get')
def test_exchange_usd_to_brl_success_new(mock_get, client):
    """
    Teste unitário que simula a resposta de sucesso da AwesomeAPI 
    e verifica se o servidor Flask a parseia corretamente.
    """
    # 1. Configura a resposta simulada (mock)
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_SUCCESS_RESPONSE_USD_BRL
    mock_get.return_value = mock_response

    # 2. Executa a função do Flask usando o cliente de teste
    response = client.get('/exchange/usd-to-brl')
    data = json.loads(response.data)

    # 3. Asserções (Verificações)
    assert response.status_code == 200
    assert data['from'] == 'USD'
    assert data['to'] == 'BRL'
    assert data['bid'] == '5.4410' 
    
    # 4. Verifica se a chamada externa foi feita (para garantir que o mocking funcionou)
    mock_get.assert_called_once()
