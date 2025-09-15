from sqlalchemy.orm import Session
from typing import Type, Optional
from ..typing import ModelType, UpdateSchemaType, FilterSchemaType
from ..helper import _to_dict
from ..models.query import FindOneRequestData, FindManyRequestData
from .read import get_one, get_many

def update_obj(
    session: Session,
    obj: ModelType,
    data: UpdateSchemaType,
    commit: bool = False
):
    update_data = _to_dict(data, exclude_unset=True)
    for field, value in update_data.items():
        setattr(obj, field, value)
    if commit:
        session.commit()
        session.refresh(obj)
    return obj

def update_one(
    session: Session,
    model: Type[ModelType],
    filters: FilterSchemaType,
    data: UpdateSchemaType,
    req: FindOneRequestData = FindOneRequestData(),
    commit: bool = False
) -> Optional[ModelType]:
    obj = get_one(session, model, filters, req)
    if obj:
        return update_obj(session, obj, data, commit)

def update_many(
    session: Session,
    model: Type[ModelType],
    filters: FilterSchemaType,
    data: UpdateSchemaType,
    req: FindManyRequestData = FindManyRequestData(),
    commit: bool = False
) -> list[ModelType]:
    objs = get_many(session, model, filters, req)
    update_data = _to_dict(data, exclude_unset=True)
    for obj in objs:
        for field, value in update_data.items():
            setattr(obj, field, value)
    if commit:
        session.commit()
        for obj in objs:
            session.refresh(obj)
    return objs
