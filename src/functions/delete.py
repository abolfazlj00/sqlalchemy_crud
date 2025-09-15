from sqlalchemy.orm import Session
from typing import Type, List
from ..typing import ModelType
from ..models.query import FindOneRequestData, FindManyRequestData
from .read import get_one, get_many

def delete_object(
    session: Session,
    obj: ModelType,
    commit: bool = False
) -> None:
    session.delete(obj)
    if commit:
        session.commit()

def delete_objects(
    session: Session,
    objs: List[ModelType],
    commit: bool = False
):
    count = len(objs)
    for obj in objs:
        session.delete(obj)
    if commit:
        session.commit()
    return count

def delete_one(
    session: Session,
    model: Type[ModelType],
    req: FindOneRequestData,
    commit: bool = False
) -> None:
    obj = get_one(session, model, req)
    if obj:
        delete_object(session, obj, commit)

def delete_many(
    session: Session,
    model: Type[ModelType],
    req: FindManyRequestData,
    commit: bool = False
) -> int:
    objs = get_many(session, model, req)
    return delete_objects(session, objs, commit)