"""
ViewSets para expor os serializers através de uma API REST.
"""

import json
from flask import Flask, request, jsonify
from typing import Any, Dict, Optional, List
from .serializer import JSONSerializer, DictSerializer
from .pagination import PageNumberPagination, LimitOffsetPagination


class JSONSerializerViewSet:
    """ViewSet para operações com JSONSerializer."""

    def __init__(
        self,
        app: Optional[Flask] = None,
        url_prefix: str = "/api/json",
        pagination_class: Optional[type] = PageNumberPagination,
    ):
        """
        Inicializa o ViewSet.

        Args:
            app: Instância da aplicação Flask
            url_prefix: Prefixo da URL para os endpoints
            pagination_class: Classe de paginação a ser usada (None para desabilitar)
        """
        self.app = app
        self.url_prefix = url_prefix
        self.serializer = JSONSerializer(indent=2)
        self.pagination_class = pagination_class
        if app:
            self.register_routes()

    def register_routes(self):
        """Registra as rotas no Flask."""
        if not self.app:
            raise ValueError("App Flask não foi fornecido")

        @self.app.route(f"{self.url_prefix}/serialize", methods=["POST"])
        def serialize():
            """Endpoint para serializar dados."""
            try:
                if not request.is_json:
                    return jsonify({"error": "Content-Type deve ser application/json"}), 400
                
                data = request.get_json(force=True)
                if data is None:
                    return jsonify({"error": "Dados JSON não fornecidos"}), 400

                serialized = self.serializer.serialize(data)
                return jsonify({"serialized": serialized}), 200
            except (TypeError, ValueError) as e:
                return jsonify({"error": f"Erro ao serializar: {str(e)}"}), 400
            except Exception as e:
                return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500

        @self.app.route(f"{self.url_prefix}/deserialize", methods=["POST"])
        def deserialize():
            """Endpoint para deserializar dados."""
            try:
                data = request.get_json()
                if data is None or "json_string" not in data:
                    return jsonify({"error": "Campo 'json_string' não fornecido"}), 400

                json_string = data["json_string"]
                deserialized = self.serializer.deserialize(json_string)
                return jsonify({"deserialized": deserialized}), 200
            except (ValueError, json.JSONDecodeError) as e:
                return jsonify({"error": f"Erro ao deserializar: {str(e)}"}), 400
            except Exception as e:
                return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500

        @self.app.route(f"{self.url_prefix}/validate", methods=["POST"])
        def validate():
            """Endpoint para validar JSON."""
            try:
                data = request.get_json()
                if data is None or "json_string" not in data:
                    return jsonify({"error": "Campo 'json_string' não fornecido"}), 400

                json_string = data["json_string"]
                is_valid = self.serializer.is_valid_json(json_string)
                return jsonify({"is_valid": is_valid}), 200
            except Exception as e:
                return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500

        @self.app.route(f"{self.url_prefix}/list", methods=["GET", "POST"])
        def list_items():
            """
            Endpoint de exemplo que retorna uma lista paginada.
            Demonstra como usar a paginação estilo DRF.
            
            GET: Retorna lista paginada de exemplo
            POST: Aceita uma lista no body e retorna paginada
            """
            try:
                # Exemplo: lista de dados (em produção viria de um banco de dados)
                if request.method == "POST":
                    data = request.get_json()
                    if data is None or "items" not in data:
                        return jsonify({"error": "Campo 'items' não fornecido"}), 400
                    items = data["items"]
                else:
                    # Lista de exemplo para demonstração
                    items = [{"id": i, "nome": f"Item {i}", "valor": i * 10} for i in range(1, 101)]

                # Aplicar paginação se configurada
                if self.pagination_class:
                    paginator = self.pagination_class()
                    paginated_items = paginator.paginate_queryset(items, request)
                    response_data = paginator.get_paginated_response_schema(
                        paginated_items, len(items), request
                    )
                    return jsonify(response_data), 200
                else:
                    return jsonify({"results": items, "count": len(items)}), 200
            except Exception as e:
                return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500


class DictSerializerViewSet:
    """ViewSet para operações com DictSerializer."""

    def __init__(self, app: Optional[Flask] = None, url_prefix: str = "/api/dict"):
        """
        Inicializa o ViewSet.

        Args:
            app: Instância da aplicação Flask
            url_prefix: Prefixo da URL para os endpoints
        """
        self.app = app
        self.url_prefix = url_prefix
        if app:
            self.register_routes()

    def register_routes(self):
        """Registra as rotas no Flask."""
        if not self.app:
            raise ValueError("App Flask não foi fornecido")

        @self.app.route(f"{self.url_prefix}/to_dict", methods=["POST"])
        def to_dict():
            """Endpoint para converter objeto para dicionário."""
            try:
                data = request.get_json()
                if data is None or "data" not in data:
                    return jsonify({"error": "Campo 'data' não fornecido"}), 400

                obj = data["data"]
                result = DictSerializer.to_dict(obj)
                return jsonify({"result": result}), 200
            except Exception as e:
                return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500


def create_app() -> Flask:
    """
    Cria e configura a aplicação Flask.

    Returns:
        Instância da aplicação Flask configurada
    """
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    # Registrar ViewSets
    JSONSerializerViewSet(app=app)
    DictSerializerViewSet(app=app)

    @app.route("/health", methods=["GET"])
    def health():
        """Endpoint de health check."""
        return jsonify({"status": "ok"}), 200

    return app

