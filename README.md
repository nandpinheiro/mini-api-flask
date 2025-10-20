# 🧩 Mini API em Flask

Este projeto faz parte da **TDE — Módulo 1: Organização e Versionamento**.  
Trata-se de uma **Mini API desenvolvida em Flask**, que permite o gerenciamento simples de usuários (criação, listagem e consulta por ID).

O objetivo do trabalho é aplicar conceitos de:
- Organização de pastas e modularização de código
- Versionamento com Git e GitHub
- Criação de endpoints em Flask
- Testes básicos e documentação colaborativa

---

## ⚙️ Tecnologias utilizadas

- [Python 3.11+](https://www.python.org/)
- [Flask 3.0.3](https://flask.palletsprojects.com/)
- [Git / GitHub](https://github.com/)
- [GitHub Codespaces](https://github.com/features/codespaces)
- [VS Code](https://code.visualstudio.com/)
- [Thunder Client](https://www.thunderclient.io/) ou [Postman](https://www.postman.com/)
- [Pytest](https://docs.pytest.org/en/stable/)

---

## 🏗️ Estrutura do projeto

```
miniapi/
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── routes.py
│   ├── config.py
│   └── models.py
├── tests/
│   └── test_example.py
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Como executar o projeto

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/<SEU_USUARIO>/Mini-API-em-Flask.git
cd Mini-API-em-Flask/miniapi
```

### 2️⃣ Criar o ambiente virtual
```bash
python -m venv venv
```

Ativar:
- Windows → `venv\Scripts\activate`
- Linux/Mac → `source venv/bin/activate`

### 3️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Executar o servidor
```bash
python -m src.app
```

A API será iniciada em:
```
http://127.0.0.1:5000
```

---

## 🌐 Endpoints disponíveis

| Método | Rota | Descrição | Exemplo de uso |
|---------|------|------------|----------------|
| GET | `/users` | Retorna todos os usuários cadastrados | `curl http://127.0.0.1:5000/users` |
| POST | `/users` | Adiciona um novo usuário | `curl -X POST http://127.0.0.1:5000/users -H "Content-Type: application/json" -d '{"name":"Ana","email":"ana@example.com"}'` |
| GET | `/users/<id>` | Retorna o usuário com o ID especificado | `curl http://127.0.0.1:5000/users/1` |
| GET | `/` | (Opcional) Mensagem de boas-vindas | `curl http://127.0.0.1:5000/` |

### 💡 Exemplo de resposta do GET `/users`
```json
[
  {"id": 1, "name": "Fernando", "email": "fernando@example.com"},
  {"id": 2, "name": "Ana", "email": "ana@example.com"}
]
```

---

## 🔁 Fluxo de versionamento Git

O desenvolvimento foi feito seguindo o modelo **Git Flow**, com as seguintes branches:

```
main
 └── develop
      ├── feature/flask-setup
      ├── feature/routes
      ├── feature/tests-docs
```

### 📜 Branches e responsabilidades

| Branch | Responsável | Descrição |
|---------|--------------|-----------|
| `main` | Pessoa 5 | Versão final e estável |
| `develop` | Pessoa 5 | Integração de features |
| `feature/base-setup` | Pessoa 1 | Estrutura inicial e versionamento |
| `feature/flask-setup` | Pessoa 2 | Configuração e inicialização do Flask |
| `feature/routes` | Pessoa 3 | Implementação dos endpoints da API |
| `feature/tests-docs` | Pessoa 4 | Testes e documentação inicial |

---

## 👥 Equipe de desenvolvimento

| Integrante | Função | Responsabilidade |
|-------------|--------|------------------|
| Pessoa 1 | Estrutura inicial | Criação do repositório, .gitignore e requirements.txt |
| Pessoa 2 | Configuração do Flask | Arquivos `app.py` e `config.py` |
| Pessoa 3 | Rotas da API | Implementação dos endpoints (`GET`, `POST`, `GET /<id>`) |
| Pessoa 4 | Testes e documentação | Testes automáticos e README inicial |
| Pessoa 5 | Integração e finalização | Merge final e README final |

---

## 🧪 Como rodar os testes

Na raiz do projeto:
```bash
pytest
```

Exemplo de teste básico (em `tests/test_example.py`):

```python
def test_example():
    assert True
```

---

## 📚 Observações finais

- Os dados dos usuários são armazenados **em memória** (lista Python).  
- Sempre que o servidor é reiniciado, a lista volta ao estado inicial.  
- O projeto segue princípios de modularização e versionamento colaborativo.  
- Para uso em produção, recomenda-se adicionar um banco de dados e servidor WSGI (como Gunicorn).  

---

## 🏁 Status do projeto

✅ Estrutura completa  
✅ Endpoints funcionais  
✅ Versionamento em múltiplas branches  
✅ Testes básicos  
✅ Documentação finalizada  

---
