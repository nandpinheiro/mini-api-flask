from flask import Blueprint, jsonify, request
import requests

user_bp = Blueprint('user_bp', __name__)

users = [
    {"id": 1, "name": "Fernando", "email": "fernando@example.com"},
  {"id": 2, "name": "Juliana", "email": "juliana@example.com"},
  {"id": 3, "name": "Carlos", "email": "carlos@example.com"},
  {"id": 4, "name": "Ana", "email": "ana@example.com"},
  {"id": 5, "name": "Rafael", "email": "rafael@example.com"},
  {"id": 6, "name": "Beatriz", "email": "beatriz@example.com"},
  {"id": 7, "name": "Lucas", "email": "lucas@example.com"},
  {"id": 8, "name": "Mariana", "email": "mariana@example.com"},
  {"id": 9, "name": "João", "email": "joao@example.com"},
  {"id": 10, "name": "Camila", "email": "camila@example.com"}
]

@user_bp.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

@user_bp.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = {
        "id": len(users) + 1,
        "name": data.get("name"),
        "email": data.get("email")
    }
    users.append(new_user)
    return jsonify(new_user), 201

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


@user_bp.route('/exchange/usd-to-brl', methods=['GET'])
def get_usd_to_brl():
    """Consulta a API externa (AwesomeAPI) e retorna a cotação USD->BRL."""
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
    except requests.RequestException:
        return jsonify({"error": "Failed to fetch exchange rate from upstream service"}), 502

    data = resp.json()
    # estrutura esperada: { "USDBRL": { ... } }
    pair_key = next(iter(data)) if isinstance(data, dict) and data else None
    if not pair_key:
        return jsonify({"error": "Unexpected response format from upstream service"}), 502

    pair = data.get(pair_key, {})
    result = {
        "from": "USD",
        "to": "BRL",
        "bid": pair.get("bid"),
        "ask": pair.get("ask"),
        "timestamp": pair.get("timestamp"),
        "create_date": pair.get("create_date"),
        "source": "AwesomeAPI"
    }
    return jsonify(result), 200

@user_bp.route('/', methods=['GET'])
def home():
    return {
        "message": "Bem-vindo a Mini API em Flask!",
        "endpoints": {
            "listar_usuarios": "/users",
            "criar_usuario": "/users (POST)",
            "buscar_por_id": "/users/<id>",
            "cotacao_usd_brl": "/exchange/usd-to-brl"
        }
    }, 200