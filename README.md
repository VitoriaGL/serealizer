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

Para executar os testes unitários:

```bash
poetry run pytest
```

Para executar com cobertura:

```bash
poetry run pytest --cov=serealizer --cov-report=html
```

## Estrutura do Projeto

```
serealizer/
├── serealizer/
│   ├── __init__.py
│   └── serializer.py
├── tests/
│   ├── __init__.py
│   └── test_serializer.py
├── pyproject.toml
└── README.md
```

## Funcionalidades

- Serialização/deserialização JSON
- Suporte para tipos especiais (datetime, Decimal, set)
- Conversão de objetos Python para dicionários
- Serialização de objetos customizados

## Desenvolvimento

Para contribuir com o projeto:

1. Instale as dependências de desenvolvimento: `poetry install`
2. Execute os testes: `poetry run pytest`
3. Formate o código: `poetry run black serealizer tests`
4. Verifique o lint: `poetry run flake8 serealizer tests`

