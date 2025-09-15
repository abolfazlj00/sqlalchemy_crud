from sqlalchemy.orm import Session
from typing import Type, Optional
from ..typing import ModelType, FilterSchemaType
from ..helper import _to_dict, _apply_order, _apply_pagination
from ..models.query import FindOneRequestData, FindManyRequestData

def get_one(
    session: Session,
    model: Type[ModelType],
    filters: FilterSchemaType,
    req: FindOneRequestData = FindOneRequestData(),
) -> Optional[ModelType]:
    query = session.query(model).filter_by(**_to_dict(filters, exclude_unset=True))
    query = _apply_order(query, model, req.order_by)
    return query.first()

def get_many(
    session: Session,
    model: Type[ModelType],
    filters: FilterSchemaType,
    req: FindManyRequestData = FindManyRequestData(),
) -> list[ModelType]:
    query = session.query(model).filter_by(**_to_dict(filters, exclude_unset=True))
    query = _apply_order(query, model, req.order_by)
    query = _apply_pagination(query, req.pagination)
    return query.all()