from sqlalchemy.orm import Session
from typing import Type
from ..typing import ModelType, CreateSchemaType, ReadSchemaType

def create_one(
    session: Session,
    model: Type[ModelType],
    data: CreateSchemaType,
    output_schema: Type[ReadSchemaType],
    commit: bool = False
) -> ReadSchemaType:
    obj = model(**data.model_dump())
    session.add(obj)
    if commit:
        session.commit()
        session.refresh(obj)
    return output_schema.model_validate(obj)