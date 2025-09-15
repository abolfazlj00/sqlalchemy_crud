from sqlalchemy.orm import Session
from typing import Type, Any
from ..typing import ModelType, CreateSchemaType
from ..helper import _to_dict

def create_one(
    session: Session,
    model: Type[ModelType],
    data: CreateSchemaType | dict[str, Any],
    commit: bool = False
) -> ModelType:
    obj = model(**_to_dict(data))
    session.add(obj)
    if commit:
        session.commit()
        session.refresh(obj)
    return obj