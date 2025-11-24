"""
Serealizer - Um serializer Python para converter objetos em diferentes formatos.
"""

from .serializer import Serializer, JSONSerializer, DictSerializer
from .viewsets import JSONSerializerViewSet, DictSerializerViewSet, create_app

__version__ = "0.1.0"
__all__ = [
    "Serializer",
    "JSONSerializer",
    "DictSerializer",
    "JSONSerializerViewSet",
    "DictSerializerViewSet",
    "create_app",
]

