"""
Exemplo de uso do serializer.
"""

from serealizer import JSONSerializer, DictSerializer
from datetime import datetime
from decimal import Decimal


def main():
    """Demonstra o uso do serializer."""
    print("=== Exemplo de uso do JSONSerializer ===\n")

    # Criar serializer
    serializer = JSONSerializer(indent=2)

    # Exemplo 1: Serializar dicionario simples
    print("1. Serializando dicionario simples:")
    data1 = {"nome": "Joao Silva", "idade": 30, "ativo": True}
    json_str = serializer.serialize(data1)
    print(json_str)
    print()

    # Exemplo 2: Serializar com tipos especiais
    print("2. Serializando com datetime e Decimal:")
    data2 = {
        "produto": "Notebook",
        "preco": Decimal("2499.99"),
        "data_compra": datetime(2023, 12, 25, 14, 30, 0),
        "tags": {"eletronicos", "computadores", "tecnologia"},
    }
    json_str2 = serializer.serialize(data2)
    print(json_str2)
    print()

    # Exemplo 3: Deserializar
    print("3. Deserializando JSON:")
    json_input = '{"nome": "Maria", "idade": 25}'
    obj = serializer.deserialize(json_input)
    print(f"Objeto deserializado: {obj}")
    print()

    # Exemplo 4: Usar DictSerializer
    print("=== Exemplo de uso do DictSerializer ===\n")
    print("4. Convertendo objeto para dicionario:")
    data3 = {
        "cliente": {
            "nome": "Carlos",
            "pedidos": [{"id": 1, "valor": Decimal("150.50")}],
            "ultima_compra": datetime(2023, 11, 15, 10, 0, 0),
        }
    }
    dict_result = DictSerializer.to_dict(data3)
    print(f"Dicionario resultante: {dict_result}")


if __name__ == "__main__":
    main()
