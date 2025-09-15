from sqlalchemy.orm import Session
from typing import Type, Any, Optional
from ..typing import ModelType, UpdateSchemaType
from ..helper import _to_dict
from ..models.query import FindOneRequestData, FindManyRequestData
from .read import get_one, get_many

def update_obj(
    session: Session,
    obj: ModelType,
    data: UpdateSchemaType | dict[str, Any],
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
    req: FindOneRequestData,
    data: UpdateSchemaType | dict[str, Any],
    commit: bool = False
) -> Optional[ModelType]:
    obj = get_one(session, model, req)
    if obj:
        return update_obj(session, obj, data, commit)

def update_many(
    session: Session,
    model: Type[ModelType],
    req: FindManyRequestData,
    data: UpdateSchemaType | dict[str, Any],
    commit: bool = False
) -> list[ModelType]:
    objs = get_many(session, model, req)
    update_data = _to_dict(data, exclude_unset=True)
    for obj in objs:
        for field, value in update_data.items():
            setattr(obj, field, value)
    if commit:
        session.commit()
        for obj in objs:
            session.refresh(obj)
    return objs
