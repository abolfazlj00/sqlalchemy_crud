from sqlalchemy.orm import Session
from typing import Generic, Type, Any, Optional
from ..typing import ModelType, CreateSchemaType, UpdateSchemaType, FilterSchemaType
from ..models.query import FindOneRequestData, FindManyRequestData
from ..functions.create import create_one
from ..functions.read import get_one, get_many
from ..functions.update import update_one, update_many
from ..functions.delete import delete_one, delete_many

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, FilterSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create_one(
        self,
        session: Session,
        data: CreateSchemaType | dict[str, Any],
        commit: bool = False
    ) -> ModelType:
        return create_one(session, self.model, data, commit)

    def get_one(
        self,
        session: Session,
        req: FindOneRequestData,
    ) -> Optional[ModelType]:
        return get_one(session, self.model, req)
        
    def get_many(
        self,
        session: Session,
        req: FindManyRequestData,
    ) -> list[ModelType]:
        return get_many(session, self.model, req)

    def update_one(
        self,
        session: Session,
        req: FindOneRequestData,
        data: UpdateSchemaType | dict[str, Any],
        commit: bool = False
    ) -> Optional[ModelType]:
        return update_one(session, self.model, req, data, commit)
    
    def update_many(
        self,
        session: Session,
        req: FindManyRequestData,
        data: UpdateSchemaType | dict[str, Any],
        commit: bool = False
    ) -> list[ModelType]:
        return update_many(session, self.model, req, data, commit)
    
    def delete_one(
        self,
        session: Session,
        req: FindOneRequestData,
        commit: bool = False
    ) -> None:
        return delete_one(session, self.model, req, commit)

    def delete_many(
        self,
        session: Session,
        req: FindManyRequestData,
        commit: bool = False
    ) -> int:
        return delete_many(session, self.model, req, commit)