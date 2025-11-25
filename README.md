# Serealizer

Um serializer Python para converter objetos em diferentes formatos (JSON, dicionários, etc.).

## Instalação

Este projeto usa [Poetry](https://python-poetry.org/) para gerenciamento de dependências.

### Pré-requisitos

- Python 3.8 ou superior
- Poetry instalado

### Instalação das dependências

```bash
poetry install
```

## Uso

### JSONSerializer

Serializa e deserializa objetos Python para/do formato JSON:

```python
from serealizer import JSONSerializer
from datetime import datetime

# Criar instância do serializer
serializer = JSONSerializer(indent=2)

# Serializar um dicionário
data = {"nome": "João", "idade": 30, "data": datetime.now()}
json_str = serializer.serialize(data)
print(json_str)

# Deserializar
obj = serializer.deserialize(json_str)
print(obj)
```

### DictSerializer

Converte objetos Python em dicionários:

```python
from serealizer.serializer import DictSerializer
from datetime import datetime

data = {"nome": "Maria", "data": datetime.now()}
dict_result = DictSerializer.to_dict(data)
print(dict_result)
```

## Executando os Testes

Para executar todos os testes unitários (serializers + viewsets):

```bash
poetry run pytest
```

Ou usando pytest diretamente:

```bash
python -m pytest tests/ -v
```

Para executar com cobertura:

```bash
poetry run pytest --cov=serealizer --cov-report=html
```

**Status dos Testes:**
- ✅ 35 testes para serializers
- ✅ 24 testes para viewsets
- ✅ **Total: 59 testes passando**

## API REST (ViewSets)

O projeto inclui ViewSets baseados em Flask para expor os serializers através de uma API REST.

### Executando a API

```bash
python app.py
```

A API estará disponível em `http://localhost:5000`

### Endpoints Disponíveis

#### JSONSerializerViewSet

- `POST /api/json/serialize` - Serializa dados para JSON
  ```bash
  curl -X POST http://localhost:5000/api/json/serialize \
    -H "Content-Type: application/json" \
    -d '{"nome": "João", "idade": 30}'
  ```

- `POST /api/json/deserialize` - Deserializa JSON para objeto Python
  ```bash
  curl -X POST http://localhost:5000/api/json/deserialize \
    -H "Content-Type: application/json" \
    -d '{"json_string": "{\"nome\": \"Maria\", \"idade\": 25}"}'
  ```

- `POST /api/json/validate` - Valida se uma string é JSON válido
  ```bash
  curl -X POST http://localhost:5000/api/json/validate \
    -H "Content-Type: application/json" \
    -d '{"json_string": "{\"nome\": \"João\"}"}'
  ```

#### DictSerializerViewSet

- `POST /api/dict/to_dict` - Converte objeto para dicionário
  ```bash
  curl -X POST http://localhost:5000/api/dict/to_dict \
    -H "Content-Type: application/json" \
    -d '{"data": {"nome": "João", "idade": 30}}'
  ```

#### Health Check

- `GET /health` - Verifica se a API está funcionando
  ```bash
  curl http://localhost:5000/health
  ```

## Estrutura do Projeto

```
serealizer/
├── serealizer/
│   ├── __init__.py
│   ├── serializer.py
│   └── viewsets.py
├── tests/
│   ├── __init__.py
│   ├── test_serializer.py
│   └── test_viewsets.py
├── app.py
├── pyproject.toml
└── README.md
```

## Funcionalidades

- Serialização/deserialização JSON
- Suporte para tipos especiais (datetime, Decimal, set)
- Conversão de objetos Python para dicionários
- Serialização de objetos customizados
- **API REST com ViewSets baseados em Flask**
- **Testes unitários completos para serializers e viewsets**

## Desenvolvimento

Para contribuir com o projeto:

1. Instale as dependências de desenvolvimento: `poetry install`
2. Execute os testes: `poetry run pytest`
3. Formate o código: `poetry run black serealizer tests`
4. Verifique o lint: `poetry run flake8 serealizer tests`

