from sqlalchemy.orm import Session
from typing import Type, Optional
from ..typing import ModelType, UpdateSchemaType, ReadSchemaType, FilterSchemaType
from ..helper import _to_dict
from ..models.query import FindOneRequestData, FindManyRequestData
from .read import get_object, get_objects

def update_obj(
    session: Session,
    obj: ModelType,
    data: UpdateSchemaType,
    commit: bool = False
) -> ModelType:
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
    to_schema: Type[ReadSchemaType],
    req: Optional[FindOneRequestData] = None,
    commit: bool = False
) -> Optional[ReadSchemaType]:
    obj = get_object(session, model, filters, req)
    if obj:
        return to_schema.model_validate(
            obj=update_obj(session, obj, data, commit)
        )

def update_many(
    session: Session,
    model: Type[ModelType],
    filters: FilterSchemaType,
    data: UpdateSchemaType,
    to_schema: Type[ReadSchemaType],
    req: Optional[FindManyRequestData] = None,
    commit: bool = False
) -> list[ReadSchemaType]:
    objs = get_objects(session, model, filters, req)
    if objs:
        update_data = data.model_dump()
        for obj in objs:
            for field, value in update_data.items():
                setattr(obj, field, value)
        if commit:
            session.commit()
            for obj in objs:
                session.refresh(obj)
    return [
        to_schema.model_validate(obj)
        for obj in objs
    ]
