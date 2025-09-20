from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.inspection import inspect
from typing import Type, Optional, NewType, Tuple
from ..typing import ModelType, FilterSchemaType, ReadSchemaType
from ..helper import _to_dict, _apply_order, _apply_pagination, build_filter
from ..models.query import FindOneRequestData, FindManyRequestData

TotalInt = NewType("TotalInt", int)
PagesInt = NewType("PagesInt", int)

def get_object(
    session: Session,
    model: Type[ModelType],
    filters: FilterSchemaType,
    req: Optional[FindOneRequestData] = None,
) -> Optional[ModelType]:
    if req is None:
        req = FindOneRequestData()
    query = session.query(model).filter(
        build_filter(model, _to_dict(filters, exclude_unset=True))
    )
    if req.order_by:
        query = _apply_order(query, model, req.order_by)
    return query.first()

def get_objects(
    session: Session,
    model: Type[ModelType],
    filters: FilterSchemaType,
    req: Optional[FindManyRequestData] = None
) -> Tuple[list[ModelType], TotalInt, PagesInt]:
    if req is None:
        req = FindManyRequestData()
    query = session.query(model).filter(
        build_filter(model, _to_dict(filters, exclude_unset=True))
    )
    # Count rows safely without modifying the original query
    total_count = session.query(func.count()).select_from(inspect(model).local_table).filter(
        build_filter(model, filters)
    ).scalar() or 0
    if req.order_by:
        query = _apply_order(query, model, req.order_by)
    query = _apply_pagination(query, req.pagination)
    query = query.offset(req.pagination.offset).limit(req.pagination.limit)
    print("total_count, req.pagination.limit", total_count, req.pagination.limit)
    pages = total_count // req.pagination.limit
    if total_count % req.pagination.limit:
        pages += 1
    return query.all(), TotalInt(total_count), PagesInt(pages)

def get_one(
    session: Session,
    model: Type[ModelType],
    filters: FilterSchemaType,
    to_schema: Type[ReadSchemaType],
    req: Optional[FindOneRequestData] = None,
) -> Optional[ReadSchemaType]:
    obj = get_object(
        session,
        model,
        filters,
        req
    )
    return to_schema.model_validate(obj) if obj else None

def get_many(
    session: Session,
    model: Type[ModelType],
    filters: FilterSchemaType,
    to_schema: Type[ReadSchemaType],
    req: Optional[FindManyRequestData] = None
) -> Tuple[list[ReadSchemaType], TotalInt, PagesInt]:
    objects, total, pages = get_objects(
        session,
        model,
        filters,
        req
    )
    return [
        to_schema.model_validate(obj)
        for obj in objects
    ], total, pages