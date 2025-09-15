from typing import Any, Type, Optional
from sqlalchemy.orm import Query
from sqlalchemy.sql.elements import ColumnElement
from .models.base import CustomBaseModel
from .models.query import OrderByData, PaginationData
from .enum.sort_directions import SortDirection
from .exceptions.invalid_filter import InvalidFilterError
from .typing import ModelType

def _to_dict(obj: Any, exclude_unset: bool = False) -> dict[str, Any]:
    """Convert Pydantic model or dict to dict."""
    if isinstance(obj, CustomBaseModel):
        return obj.model_dump(
            exclude_unset=exclude_unset
        )
    if isinstance(obj, dict):
        return obj
    raise TypeError(f"Expected dict or 'CustomBaseModel', got {type(obj)}")


def _apply_order(query: Query, model: Type[ModelType], order: Optional[OrderByData]):
    if order:
        column: Optional[ColumnElement] = getattr(model, order.column, None)
        if not column:
            raise InvalidFilterError(f"Invalid order column: {order.column}")
        if order.direction == SortDirection.ASC:
            query = query.order_by(column.asc().nullsfirst() if order.nulls_first else column.asc().nullslast())
        else:
            query = query.order_by(column.desc().nullsfirst() if order.nulls_first else column.desc().nullslast())
    return query

def _apply_pagination(query: Query, pagination: PaginationData):
    if pagination:
        query = query.offset(pagination.offset).limit(pagination.limit)
    return query