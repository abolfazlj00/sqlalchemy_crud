from typing import Any, Type, Optional, Dict
from pydantic import BaseModel
from sqlalchemy import and_, or_
from sqlalchemy.orm import Query, DeclarativeMeta
from sqlalchemy.sql.elements import ColumnElement
from .enum.operation import Operator
from .models.query import OrderByData, PaginationData
from .enum.sort_directions import SortDirection
from .exceptions.invalid_filter import InvalidFilterError
from .typing import ModelType

def _to_dict(obj: Any, exclude_unset: bool = False) -> dict[str, Any]:
    """Convert Pydantic model or dict to dict."""
    if isinstance(obj, BaseModel):
        return obj.model_dump(
            exclude_unset=exclude_unset
        )
    if isinstance(obj, dict):
        return obj
    raise TypeError(f"Expected dict or 'pydantic.BaseModel', got {type(obj)}")

def _apply_order(query: Query, model: Type[ModelType], order: OrderByData):
    column: Optional[ColumnElement] = getattr(model, order.column, None)
    if not column:
        raise InvalidFilterError(f"Invalid order column: {order.column}")
    if order.direction == SortDirection.ASC:
        query = query.order_by(column.asc().nullsfirst() if order.nulls_first else column.asc().nullslast())
    else:
        query = query.order_by(column.desc().nullsfirst() if order.nulls_first else column.desc().nullslast())
    return query

def _apply_pagination(query: Query, pagination: PaginationData):
    return query.offset(pagination.offset).limit(pagination.limit)

def build_filter(model: DeclarativeMeta, filters: Dict[str, Any]):
    expressions = []

    for key, value in filters.items():
        if key == "and_" and isinstance(value, list):
            expressions.append(
                and_(*[build_filter(model, f) for f in value])
            )
        elif key == "or_" and isinstance(value, list):
            expressions.append(
                or_(*[build_filter(model, f) for f in value])
            )
        else:
            column = getattr(model, key)
            if isinstance(value, dict):
                for op_str, v in value.items():
                    op = Operator(op_str)
                    if op == Operator.EQ:
                        expressions.append(column == v)
                    elif op == Operator.NEQ:
                        expressions.append(column != v)
                    elif op == Operator.LT:
                        expressions.append(column < v)
                    elif op == Operator.LTE:
                        expressions.append(column <= v)
                    elif op == Operator.GT:
                        expressions.append(column > v)
                    elif op == Operator.GTE:
                        expressions.append(column >= v)
                    elif op == Operator.IN:
                        expressions.append(column.in_(v))
                    elif op == Operator.LIKE:
                        expressions.append(column.like(v))
                    elif op == Operator.ILIKE:
                        expressions.append(column.ilike(v))
            else:
                expressions.append(column == value)

    if len(expressions) == 1:
        return expressions[0]
    if len(expressions) == 0:
        return and_(True)
    return and_(*expressions)