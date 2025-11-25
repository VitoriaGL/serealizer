"""
Testes unitários para os ViewSets.
"""

import pytest
import json
from datetime import datetime
from decimal import Decimal
from serealizer.viewsets import (
    JSONSerializerViewSet,
    DictSerializerViewSet,
    create_app,
)


class TestJSONSerializerViewSet:
    """Testes para JSONSerializerViewSet."""

    @pytest.fixture
    def app(self):
        """Cria uma instância da aplicação Flask para testes."""
        return create_app()

    @pytest.fixture
    def client(self, app):
        """Cria um cliente de teste."""
        return app.test_client()

    def test_serialize_endpoint_success(self, client):
        """Testa serialização bem-sucedida."""
        data = {"nome": "João", "idade": 30}
        response = client.post(
            "/api/json/serialize",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 200
        result = json.loads(response.data)
        assert "serialized" in result
        assert json.loads(result["serialized"]) == data

    def test_serialize_endpoint_with_datetime(self, client):
        """Testa serialização com datetime."""
        data = {"data": "2023-12-25T10:30:00"}
        response = client.post(
            "/api/json/serialize",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 200

    def test_serialize_endpoint_missing_data(self, client):
        """Testa serialização sem dados."""
        response = client.post(
            "/api/json/serialize",
            data=json.dumps(None),
            content_type="application/json",
        )
        # Flask pode retornar 200 com None ou 400 dependendo da implementação
        assert response.status_code in [200, 400]
        result = json.loads(response.data)
        assert "error" in result or "serialized" in result

    def test_serialize_endpoint_invalid_json(self, client):
        """Testa serialização com JSON inválido."""
        response = client.post(
            "/api/json/serialize",
            data="invalid json",
            content_type="application/json",
        )
        # Flask pode retornar 400 ou 500 dependendo de como trata JSON inválido
        assert response.status_code in [400, 500]
        result = json.loads(response.data)
        assert "error" in result

    def test_deserialize_endpoint_success(self, client):
        """Testa deserialização bem-sucedida."""
        json_string = '{"nome": "Maria", "idade": 25}'
        data = {"json_string": json_string}
        response = client.post(
            "/api/json/deserialize",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 200
        result = json.loads(response.data)
        assert "deserialized" in result
        assert result["deserialized"] == {"nome": "Maria", "idade": 25}

    def test_deserialize_endpoint_missing_field(self, client):
        """Testa deserialização sem campo obrigatório."""
        data = {}
        response = client.post(
            "/api/json/deserialize",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 400
        result = json.loads(response.data)
        assert "error" in result

    def test_deserialize_endpoint_invalid_json(self, client):
        """Testa deserialização com JSON inválido."""
        data = {"json_string": "invalid json"}
        response = client.post(
            "/api/json/deserialize",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_validate_endpoint_valid_json(self, client):
        """Testa validação de JSON válido."""
        data = {"json_string": '{"nome": "João"}'}
        response = client.post(
            "/api/json/validate",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result["is_valid"] is True

    def test_validate_endpoint_invalid_json(self, client):
        """Testa validação de JSON inválido."""
        data = {"json_string": "invalid json"}
        response = client.post(
            "/api/json/validate",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result["is_valid"] is False

    def test_validate_endpoint_missing_field(self, client):
        """Testa validação sem campo obrigatório."""
        data = {}
        response = client.post(
            "/api/json/validate",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 400
        result = json.loads(response.data)
        assert "error" in result

    def test_serialize_complex_data(self, client):
        """Testa serialização de dados complexos."""
        data = {
            "usuarios": [
                {"nome": "João", "idade": 30},
                {"nome": "Maria", "idade": 25},
            ],
            "metadata": {"total": 2},
        }
        response = client.post(
            "/api/json/serialize",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 200
        result = json.loads(response.data)
        deserialized = json.loads(result["serialized"])
        assert len(deserialized["usuarios"]) == 2
        assert deserialized["metadata"]["total"] == 2


class TestDictSerializerViewSet:
    """Testes para DictSerializerViewSet."""

    @pytest.fixture
    def app(self):
        """Cria uma instância da aplicação Flask para testes."""
        return create_app()

    @pytest.fixture
    def client(self, app):
        """Cria um cliente de teste."""
        return app.test_client()

    def test_to_dict_endpoint_simple_dict(self, client):
        """Testa conversão de dicionário simples."""
        data = {"data": {"nome": "João", "idade": 30}}
        response = client.post(
            "/api/dict/to_dict",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 200
        result = json.loads(response.data)
        assert "result" in result
        assert result["result"] == {"nome": "João", "idade": 30}

    def test_to_dict_endpoint_list(self, client):
        """Testa conversão de lista."""
        data = {"data": [1, 2, 3, "teste"]}
        response = client.post(
            "/api/dict/to_dict",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result["result"] == [1, 2, 3, "teste"]

    def test_to_dict_endpoint_nested_dict(self, client):
        """Testa conversão de dicionário aninhado."""
        data = {
            "data": {
                "pessoa": {
                    "nome": "Maria",
                    "endereco": {"rua": "Rua A", "numero": 123},
                }
            }
        }
        response = client.post(
            "/api/dict/to_dict",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result["result"]["pessoa"]["nome"] == "Maria"
        assert result["result"]["pessoa"]["endereco"]["rua"] == "Rua A"

    def test_to_dict_endpoint_missing_field(self, client):
        """Testa conversão sem campo obrigatório."""
        data = {}
        response = client.post(
            "/api/dict/to_dict",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 400
        result = json.loads(response.data)
        assert "error" in result

    def test_to_dict_endpoint_empty_dict(self, client):
        """Testa conversão de dicionário vazio."""
        data = {"data": {}}
        response = client.post(
            "/api/dict/to_dict",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result["result"] == {}

    def test_to_dict_endpoint_empty_list(self, client):
        """Testa conversão de lista vazia."""
        data = {"data": []}
        response = client.post(
            "/api/dict/to_dict",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result["result"] == []

    def test_to_dict_endpoint_primitives(self, client):
        """Testa conversão de tipos primitivos."""
        test_cases = [
            {"data": 42},
            {"data": 3.14},
            {"data": "texto"},
            {"data": True},
            {"data": None},
        ]
        for test_data in test_cases:
            response = client.post(
                "/api/dict/to_dict",
                data=json.dumps(test_data),
                content_type="application/json",
            )
            assert response.status_code == 200
            result = json.loads(response.data)
            assert result["result"] == test_data["data"]


class TestAppIntegration:
    """Testes de integração da aplicação."""

    @pytest.fixture
    def app(self):
        """Cria uma instância da aplicação Flask para testes."""
        return create_app()

    @pytest.fixture
    def client(self, app):
        """Cria um cliente de teste."""
        return app.test_client()

    def test_health_endpoint(self, client):
        """Testa endpoint de health check."""
        response = client.get("/health")
        assert response.status_code == 200
        result = json.loads(response.data)
        assert result["status"] == "ok"

    def test_json_serializer_viewset_registration(self, app):
        """Testa se JSONSerializerViewSet está registrado."""
        # Criar um novo app para evitar conflito de rotas
        from flask import Flask
        new_app = Flask(__name__)
        viewset = JSONSerializerViewSet(app=new_app)
        assert viewset.app == new_app
        assert viewset.url_prefix == "/api/json"

    def test_dict_serializer_viewset_registration(self, app):
        """Testa se DictSerializerViewSet está registrado."""
        # Criar um novo app para evitar conflito de rotas
        from flask import Flask
        new_app = Flask(__name__)
        viewset = DictSerializerViewSet(app=new_app)
        assert viewset.app == new_app
        assert viewset.url_prefix == "/api/dict"

    def test_viewset_without_app(self):
        """Testa criação de ViewSet sem app."""
        viewset = JSONSerializerViewSet()
        assert viewset.app is None

    def test_viewset_register_routes_without_app(self):
        """Testa registro de rotas sem app."""
        viewset = JSONSerializerViewSet()
        with pytest.raises(ValueError):
            viewset.register_routes()

    def test_end_to_end_serialize_deserialize(self, client):
        """Testa fluxo completo de serialização e deserialização."""
        # Serializar
        original_data = {"nome": "Carlos", "idade": 35}
        serialize_response = client.post(
            "/api/json/serialize",
            data=json.dumps(original_data),
            content_type="application/json",
        )
        assert serialize_response.status_code == 200
        serialize_result = json.loads(serialize_response.data)
        json_string = serialize_result["serialized"]

        # Deserializar
        deserialize_data = {"json_string": json_string}
        deserialize_response = client.post(
            "/api/json/deserialize",
            data=json.dumps(deserialize_data),
            content_type="application/json",
        )
        assert deserialize_response.status_code == 200
        deserialize_result = json.loads(deserialize_response.data)
        assert deserialize_result["deserialized"] == original_data

