"""
Módulo de paginação estilo Django REST Framework.
"""

from typing import Any, Dict, List, Optional
from flask import request


class PageNumberPagination:
    """
    Classe de paginação estilo Django REST Framework.
    
    Suporta paginação baseada em número de página com parâmetros:
    - page: número da página (padrão: 1)
    - page_size: tamanho da página (padrão: 20)
    """

    page_size = 20
    page_size_query_param = "page_size"
    page_query_param = "page"
    max_page_size = 100

    def get_page_size(self, request_obj: Any) -> int:
        """
        Retorna o tamanho da página baseado nos parâmetros da requisição.
        
        Args:
            request_obj: Objeto request do Flask
            
        Returns:
            Tamanho da página
        """
        if self.page_size_query_param:
            try:
                page_size = int(request_obj.args.get(self.page_size_query_param, self.page_size))
                if page_size > 0:
                    return min(page_size, self.max_page_size)
            except (ValueError, TypeError):
                pass
        return self.page_size

    def get_page_number(self, request_obj: Any) -> int:
        """
        Retorna o número da página baseado nos parâmetros da requisição.
        
        Args:
            request_obj: Objeto request do Flask
            
        Returns:
            Número da página (1-indexed)
        """
        try:
            page = int(request_obj.args.get(self.page_query_param, 1))
            return max(1, page)
        except (ValueError, TypeError):
            return 1

    def paginate_queryset(self, queryset: List[Any], request_obj: Any) -> List[Any]:
        """
        Pagina uma lista de objetos.
        
        Args:
            queryset: Lista de objetos a serem paginados
            request_obj: Objeto request do Flask
            
        Returns:
            Lista paginada de objetos
        """
        page_size = self.get_page_size(request_obj)
        page_number = self.get_page_number(request_obj)
        
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        
        return queryset[start_index:end_index]

    def get_paginated_response(self, data: List[Any], request_obj: Any) -> Dict[str, Any]:
        """
        Retorna uma resposta paginada no formato DRF.
        
        Args:
            data: Lista paginada de dados
            request_obj: Objeto request do Flask
            
        Returns:
            Dicionário com a resposta paginada
        """
        page_size = self.get_page_size(request_obj)
        page_number = self.get_page_number(request_obj)
        
        # Para calcular o total, precisaríamos ter acesso ao queryset completo
        # Por enquanto, retornamos apenas os dados paginados
        return {
            "count": len(data),  # Será atualizado se tiver acesso ao total
            "next": self.get_next_link(page_number, page_size, request_obj) if len(data) == page_size else None,
            "previous": self.get_previous_link(page_number, request_obj) if page_number > 1 else None,
            "results": data,
        }

    def get_paginated_response_schema(self, data: List[Any], total_count: int, request_obj: Any) -> Dict[str, Any]:
        """
        Retorna uma resposta paginada com o total de itens.
        
        Args:
            data: Lista paginada de dados
            total_count: Total de itens no queryset completo
            request_obj: Objeto request do Flask
            
        Returns:
            Dicionário com a resposta paginada completa
        """
        page_size = self.get_page_size(request_obj)
        page_number = self.get_page_number(request_obj)
        
        has_next = (page_number * page_size) < total_count
        has_previous = page_number > 1
        
        return {
            "count": total_count,
            "next": self.get_next_link(page_number, page_size, request_obj) if has_next else None,
            "previous": self.get_previous_link(page_number, request_obj) if has_previous else None,
            "results": data,
        }

    def get_next_link(self, page_number: int, page_size: int, request_obj: Any) -> Optional[str]:
        """
        Gera o link para a próxima página.
        
        Args:
            page_number: Número da página atual
            page_size: Tamanho da página
            request_obj: Objeto request do Flask
            
        Returns:
            URL da próxima página ou None
        """
        if not request_obj:
            return None
        
        next_page = page_number + 1
        base_url = request_obj.url.split("?")[0]
        params = dict(request_obj.args)
        params[self.page_query_param] = next_page
        if self.page_size_query_param:
            params[self.page_size_query_param] = page_size
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{query_string}" if query_string else base_url

    def get_previous_link(self, page_number: int, request_obj: Any) -> Optional[str]:
        """
        Gera o link para a página anterior.
        
        Args:
            page_number: Número da página atual
            request_obj: Objeto request do Flask
            
        Returns:
            URL da página anterior ou None
        """
        if not request_obj or page_number <= 1:
            return None
        
        previous_page = page_number - 1
        base_url = request_obj.url.split("?")[0]
        params = dict(request_obj.args)
        params[self.page_query_param] = previous_page
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{query_string}" if query_string else base_url


class LimitOffsetPagination:
    """
    Classe de paginação estilo limit/offset.
    
    Suporta paginação baseada em limite e offset com parâmetros:
    - limit: número máximo de itens (padrão: 20)
    - offset: número de itens a pular (padrão: 0)
    """

    default_limit = 20
    limit_query_param = "limit"
    offset_query_param = "offset"
    max_limit = 100

    def get_limit(self, request_obj: Any) -> int:
        """
        Retorna o limite baseado nos parâmetros da requisição.
        
        Args:
            request_obj: Objeto request do Flask
            
        Returns:
            Limite de itens
        """
        try:
            limit = int(request_obj.args.get(self.limit_query_param, self.default_limit))
            if limit > 0:
                return min(limit, self.max_limit)
        except (ValueError, TypeError):
            pass
        return self.default_limit

    def get_offset(self, request_obj: Any) -> int:
        """
        Retorna o offset baseado nos parâmetros da requisição.
        
        Args:
            request_obj: Objeto request do Flask
            
        Returns:
            Offset (número de itens a pular)
        """
        try:
            offset = int(request_obj.args.get(self.offset_query_param, 0))
            return max(0, offset)
        except (ValueError, TypeError):
            return 0

    def paginate_queryset(self, queryset: List[Any], request_obj: Any) -> List[Any]:
        """
        Pagina uma lista de objetos usando limit/offset.
        
        Args:
            queryset: Lista de objetos a serem paginados
            request_obj: Objeto request do Flask
            
        Returns:
            Lista paginada de objetos
        """
        limit = self.get_limit(request_obj)
        offset = self.get_offset(request_obj)
        
        return queryset[offset:offset + limit]

    def get_paginated_response_schema(self, data: List[Any], total_count: int, request_obj: Any) -> Dict[str, Any]:
        """
        Retorna uma resposta paginada com o total de itens.
        
        Args:
            data: Lista paginada de dados
            total_count: Total de itens no queryset completo
            request_obj: Objeto request do Flask
            
        Returns:
            Dicionário com a resposta paginada completa
        """
        limit = self.get_limit(request_obj)
        offset = self.get_offset(request_obj)
        
        has_next = (offset + limit) < total_count
        has_previous = offset > 0
        
        return {
            "count": total_count,
            "next": self.get_next_link(limit, offset, total_count, request_obj) if has_next else None,
            "previous": self.get_previous_link(limit, offset, request_obj) if has_previous else None,
            "results": data,
        }

    def get_next_link(self, limit: int, offset: int, total_count: int, request_obj: Any) -> Optional[str]:
        """
        Gera o link para a próxima página.
        
        Args:
            limit: Limite atual
            offset: Offset atual
            total_count: Total de itens
            request_obj: Objeto request do Flask
            
        Returns:
            URL da próxima página ou None
        """
        if not request_obj or (offset + limit) >= total_count:
            return None
        
        next_offset = offset + limit
        base_url = request_obj.url.split("?")[0]
        params = dict(request_obj.args)
        params[self.limit_query_param] = limit
        params[self.offset_query_param] = next_offset
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{query_string}" if query_string else base_url

    def get_previous_link(self, limit: int, offset: int, request_obj: Any) -> Optional[str]:
        """
        Gera o link para a página anterior.
        
        Args:
            limit: Limite atual
            offset: Offset atual
            request_obj: Objeto request do Flask
            
        Returns:
            URL da página anterior ou None
        """
        if not request_obj or offset <= 0:
            return None
        
        previous_offset = max(0, offset - limit)
        base_url = request_obj.url.split("?")[0]
        params = dict(request_obj.args)
        params[self.limit_query_param] = limit
        params[self.offset_query_param] = previous_offset
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{query_string}" if query_string else base_url

