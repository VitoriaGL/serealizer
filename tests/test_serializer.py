"""
Testes unitários para o módulo serializer.
"""

import pytest
import json
from datetime import datetime
from decimal import Decimal
from serealizer.serializer import JSONSerializer, DictSerializer, Serializer


class TestJSONSerializer:
    """Testes para a classe JSONSerializer."""

    def test_serialize_dict(self):
        """Testa serialização de dicionário."""
        serializer = JSONSerializer()
        data = {"nome": "João", "idade": 30}
        result = serializer.serialize(data)
        assert isinstance(result, str)
        assert json.loads(result) == data

    def test_serialize_list(self):
        """Testa serialização de lista."""
        serializer = JSONSerializer()
        data = [1, 2, 3, "teste"]
        result = serializer.serialize(data)
        assert isinstance(result, str)
        assert json.loads(result) == data

    def test_serialize_with_indent(self):
        """Testa serialização com indentação."""
        serializer = JSONSerializer(indent=2)
        data = {"nome": "João", "idade": 30}
        result = serializer.serialize(data)
        assert "\n" in result
        assert json.loads(result) == data

    def test_deserialize_dict(self):
        """Testa deserialização de dicionário."""
        serializer = JSONSerializer()
        json_str = '{"nome": "João", "idade": 30}'
        result = serializer.deserialize(json_str)
        assert result == {"nome": "João", "idade": 30}

    def test_deserialize_list(self):
        """Testa deserialização de lista."""
        serializer = JSONSerializer()
        json_str = '[1, 2, 3, "teste"]'
        result = serializer.deserialize(json_str)
        assert result == [1, 2, 3, "teste"]

    def test_serialize_deserialize_roundtrip(self):
        """Testa ciclo completo de serialização e deserialização."""
        serializer = JSONSerializer()
        original = {"nome": "Maria", "idade": 25, "ativo": True}
        serialized = serializer.serialize(original)
        deserialized = serializer.deserialize(serialized)
        assert deserialized == original

    def test_serialize_datetime(self):
        """Testa serialização de datetime."""
        serializer = JSONSerializer()
        dt = datetime(2023, 12, 25, 10, 30, 0)
        result = serializer.serialize({"data": dt})
        data = json.loads(result)
        assert data["data"]["__type__"] == "datetime"
        assert "2023-12-25T10:30:00" in data["data"]["__value__"]

    def test_serialize_decimal(self):
        """Testa serialização de Decimal."""
        serializer = JSONSerializer()
        value = Decimal("123.45")
        result = serializer.serialize({"valor": value})
        data = json.loads(result)
        assert data["valor"]["__type__"] == "decimal"
        assert data["valor"]["__value__"] == "123.45"

    def test_serialize_set(self):
        """Testa serialização de set."""
        serializer = JSONSerializer()
        value = {1, 2, 3}
        result = serializer.serialize({"numeros": value})
        data = json.loads(result)
        assert data["numeros"]["__type__"] == "set"
        assert set(data["numeros"]["__value__"]) == {1, 2, 3}

    def test_deserialize_invalid_json(self):
        """Testa deserialização de JSON inválido."""
        serializer = JSONSerializer()
        with pytest.raises(json.JSONDecodeError):
            serializer.deserialize("invalid json")

    def test_serialize_custom_object(self):
        """Testa serialização de objeto customizado."""
        serializer = JSONSerializer()

        class Pessoa:
            def __init__(self, nome, idade):
                self.nome = nome
                self.idade = idade

        pessoa = Pessoa("Carlos", 35)
        result = serializer.serialize({"pessoa": pessoa})
        data = json.loads(result)
        assert data["pessoa"]["__type__"] == "Pessoa"
        assert data["pessoa"]["__dict__"]["nome"] == "Carlos"
        assert data["pessoa"]["__dict__"]["idade"] == 35

    def test_serialize_empty_dict(self):
        """Testa serialização de dicionário vazio."""
        serializer = JSONSerializer()
        result = serializer.serialize({})
        assert result == "{}"
        assert serializer.deserialize(result) == {}

    def test_serialize_empty_list(self):
        """Testa serialização de lista vazia."""
        serializer = JSONSerializer()
        result = serializer.serialize([])
        assert result == "[]"
        assert serializer.deserialize(result) == []

    def test_serialize_none(self):
        """Testa serialização de None."""
        serializer = JSONSerializer()
        result = serializer.serialize({"valor": None})
        data = json.loads(result)
        assert data["valor"] is None

    def test_serialize_empty_string(self):
        """Testa serialização de string vazia."""
        serializer = JSONSerializer()
        result = serializer.serialize({"texto": ""})
        data = json.loads(result)
        assert data["texto"] == ""

    def test_serialize_nested_empty_structures(self):
        """Testa serialização de estruturas aninhadas vazias."""
        serializer = JSONSerializer()
        data = {"lista": [], "dict": {}, "nested": {"lista": [], "dict": {}}}
        result = serializer.serialize(data)
        assert serializer.deserialize(result) == data

    def test_serialize_ensure_ascii_true(self):
        """Testa serialização com ensure_ascii=True."""
        serializer = JSONSerializer(ensure_ascii=True)
        data = {"texto": "café", "numero": 123}
        result = serializer.serialize(data)
        # Verifica que o JSON foi gerado corretamente
        deserialized = serializer.deserialize(result)
        assert deserialized["numero"] == 123
        # Com ensure_ascii=True, caracteres não-ASCII podem ser escapados
        assert isinstance(result, str)

    def test_is_valid_json_valid(self):
        """Testa validação de JSON válido."""
        valid_jsons = [
            '{"nome": "teste"}',
            '[1, 2, 3]',
            '{"nested": {"key": "value"}}',
            'null',
            'true',
            'false',
            '42',
            '"string"',
        ]
        for json_str in valid_jsons:
            assert JSONSerializer.is_valid_json(json_str) is True

    def test_is_valid_json_invalid(self):
        """Testa validação de JSON inválido."""
        invalid_jsons = [
            "invalid json",
            "{nome: teste}",
            "[1, 2, 3",
            '{"unclosed": "string}',
            "undefined",
            "",
        ]
        for json_str in invalid_jsons:
            assert JSONSerializer.is_valid_json(json_str) is False

    def test_serialize_complex_nested_structure(self):
        """Testa serialização de estrutura complexa aninhada."""
        serializer = JSONSerializer()
        data = {
            "usuarios": [
                {"nome": "Joao", "idade": 30, "tags": {"ativo", "premium"}},
                {"nome": "Maria", "idade": 25, "tags": {"ativo"}},
            ],
            "metadata": {"total": 2, "data_criacao": datetime(2023, 1, 1)},
        }
        result = serializer.serialize(data)
        deserialized = serializer.deserialize(result)
        assert len(deserialized["usuarios"]) == 2
        assert deserialized["metadata"]["total"] == 2


class TestDictSerializer:
    """Testes para a classe DictSerializer."""

    def test_to_dict_simple_dict(self):
        """Testa conversão de dicionário simples."""
        data = {"nome": "João", "idade": 30}
        result = DictSerializer.to_dict(data)
        assert result == data

    def test_to_dict_nested_dict(self):
        """Testa conversão de dicionário aninhado."""
        data = {
            "pessoa": {
                "nome": "Maria",
                "endereco": {"rua": "Rua A", "numero": 123},
            }
        }
        result = DictSerializer.to_dict(data)
        assert result == data

    def test_to_dict_list(self):
        """Testa conversão de lista."""
        data = [1, 2, 3, "teste"]
        result = DictSerializer.to_dict(data)
        assert result == data

    def test_to_dict_tuple(self):
        """Testa conversão de tupla."""
        data = (1, 2, 3)
        result = DictSerializer.to_dict(data)
        assert isinstance(result, list)
        assert result == [1, 2, 3]

    def test_to_dict_datetime(self):
        """Testa conversão de datetime."""
        dt = datetime(2023, 12, 25, 10, 30, 0)
        result = DictSerializer.to_dict({"data": dt})
        assert result["data"]["__type__"] == "datetime"
        assert "2023-12-25T10:30:00" in result["data"]["__value__"]

    def test_to_dict_decimal(self):
        """Testa conversão de Decimal."""
        value = Decimal("99.99")
        result = DictSerializer.to_dict({"valor": value})
        assert result["valor"]["__type__"] == "decimal"
        assert result["valor"]["__value__"] == "99.99"

    def test_to_dict_set(self):
        """Testa conversão de set."""
        value = {"a", "b", "c"}
        result = DictSerializer.to_dict({"letras": value})
        assert result["letras"]["__type__"] == "set"
        assert set(result["letras"]["__value__"]) == {"a", "b", "c"}

    def test_to_dict_custom_object(self):
        """Testa conversão de objeto customizado."""
        class Produto:
            def __init__(self, nome, preco):
                self.nome = nome
                self.preco = preco

        produto = Produto("Notebook", 2500.00)
        result = DictSerializer.to_dict({"produto": produto})
        assert result["produto"]["__type__"] == "Produto"
        assert result["produto"]["__dict__"]["nome"] == "Notebook"
        assert result["produto"]["__dict__"]["preco"] == 2500.00

    def test_to_dict_primitives(self):
        """Testa conversão de tipos primitivos."""
        assert DictSerializer.to_dict(42) == 42
        assert DictSerializer.to_dict(3.14) == 3.14
        assert DictSerializer.to_dict("texto") == "texto"
        assert DictSerializer.to_dict(True) is True
        assert DictSerializer.to_dict(None) is None

    def test_to_dict_empty_dict(self):
        """Testa conversão de dicionário vazio."""
        result = DictSerializer.to_dict({})
        assert result == {}

    def test_to_dict_empty_list(self):
        """Testa conversão de lista vazia."""
        result = DictSerializer.to_dict([])
        assert result == []

    def test_to_dict_empty_set(self):
        """Testa conversão de set vazio."""
        result = DictSerializer.to_dict(set())
        assert result["__type__"] == "set"
        assert result["__value__"] == []

    def test_to_dict_mixed_types(self):
        """Testa conversão de estrutura com tipos mistos."""
        data = {
            "numero": 42,
            "texto": "teste",
            "lista": [1, "dois", 3.0],
            "set": {1, 2, 3},
            "decimal": Decimal("10.5"),
            "data": datetime(2023, 1, 1),
        }
        result = DictSerializer.to_dict(data)
        assert result["numero"] == 42
        assert result["texto"] == "teste"
        assert len(result["lista"]) == 3
        assert result["set"]["__type__"] == "set"


class TestSerializerBase:
    """Testes para a classe base Serializer."""

    def test_serialize_not_implemented(self):
        """Testa que serialize levanta NotImplementedError."""
        serializer = Serializer()
        with pytest.raises(NotImplementedError):
            serializer.serialize({"test": "data"})

    def test_deserialize_not_implemented(self):
        """Testa que deserialize levanta NotImplementedError."""
        serializer = Serializer()
        with pytest.raises(NotImplementedError):
            serializer.deserialize('{"test": "data"}')

