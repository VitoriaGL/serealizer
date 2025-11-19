"""
Módulo principal do serializer.
"""

import json
from typing import Any, Dict, Optional
from datetime import datetime
from decimal import Decimal


class Serializer:
    """Classe base abstrata para serializers."""

    def serialize(self, obj: Any) -> str:
        """
        Serializa um objeto para string.

        Args:
            obj: Objeto a ser serializado

        Returns:
            String representando o objeto serializado

        Raises:
            NotImplementedError: Se o método não for implementado
        """
        raise NotImplementedError("Subclasses devem implementar serialize")

    def deserialize(self, data: str) -> Any:
        """
        Deserializa uma string para objeto.

        Args:
            data: String a ser deserializada

        Returns:
            Objeto deserializado

        Raises:
            NotImplementedError: Se o método não for implementado
        """
        raise NotImplementedError("Subclasses devem implementar deserialize")


class JSONSerializer(Serializer):
    """Serializer para formato JSON."""

    def __init__(self, indent: Optional[int] = None, ensure_ascii: bool = False):
        """
        Inicializa o JSONSerializer.

        Args:
            indent: Número de espaços para indentação (None para compacto)
            ensure_ascii: Se True, garante que apenas caracteres ASCII sejam usados
        """
        self.indent = indent
        self.ensure_ascii = ensure_ascii

    def serialize(self, obj: Any) -> str:
        """
        Serializa um objeto para JSON.

        Args:
            obj: Objeto a ser serializado

        Returns:
            String JSON representando o objeto

        Raises:
            TypeError: Se o objeto não puder ser serializado
        """
        return json.dumps(
            obj,
            indent=self.indent,
            ensure_ascii=self.ensure_ascii,
            default=self._default_serializer,
        )

    def deserialize(self, data: str) -> Any:
        """
        Deserializa uma string JSON para objeto Python.

        Args:
            data: String JSON a ser deserializada

        Returns:
            Objeto Python deserializado

        Raises:
            json.JSONDecodeError: Se a string não for um JSON válido
        """
        return json.loads(data)

    @staticmethod
    def is_valid_json(data: str) -> bool:
        """
        Verifica se uma string é um JSON válido.

        Args:
            data: String a ser verificada

        Returns:
            True se a string for um JSON válido, False caso contrário
        """
        try:
            json.loads(data)
            return True
        except (json.JSONDecodeError, TypeError):
            return False

    @staticmethod
    def _default_serializer(obj: Any) -> Any:
        """
        Função auxiliar para serializar tipos especiais.

        Args:
            obj: Objeto a ser serializado

        Returns:
            Representação serializável do objeto

        Raises:
            TypeError: Se o tipo não for suportado
        """
        if isinstance(obj, datetime):
            return {"__type__": "datetime", "__value__": obj.isoformat()}
        elif isinstance(obj, Decimal):
            return {"__type__": "decimal", "__value__": str(obj)}
        elif isinstance(obj, set):
            return {"__type__": "set", "__value__": list(obj)}
        elif hasattr(obj, "__dict__"):
            return {"__type__": type(obj).__name__, "__dict__": obj.__dict__}
        raise TypeError(f"Tipo {type(obj)} não é serializável")


class DictSerializer:
    """Serializer para converter objetos Python em dicionários."""

    @staticmethod
    def to_dict(obj: Any) -> Dict[str, Any]:
        """
        Converte um objeto Python em dicionário.

        Args:
            obj: Objeto a ser convertido

        Returns:
            Dicionário representando o objeto
        """
        if isinstance(obj, dict):
            return {key: DictSerializer.to_dict(value) for key, value in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [DictSerializer.to_dict(item) for item in obj]
        elif isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        elif isinstance(obj, datetime):
            return {"__type__": "datetime", "__value__": obj.isoformat()}
        elif isinstance(obj, Decimal):
            return {"__type__": "decimal", "__value__": str(obj)}
        elif isinstance(obj, set):
            return {"__type__": "set", "__value__": list(obj)}
        elif hasattr(obj, "__dict__"):
            return {
                "__type__": type(obj).__name__,
                "__dict__": DictSerializer.to_dict(obj.__dict__),
            }
        else:
            return str(obj)

