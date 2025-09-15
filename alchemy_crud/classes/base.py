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
        data: CreateSchemaType,
        commit: bool = False
    ) -> ModelType:
        return create_one(session, self.model, data, commit)

    def get_one(
        self,
        session: Session,
        filters: FilterSchemaType,
        req: FindOneRequestData = FindOneRequestData(),
    ) -> Optional[ModelType]:
        return get_one(session, self.model, filters, req)
        
    def get_many(
        self,
        session: Session,
        filters: FilterSchemaType,
        req: FindManyRequestData = FindOneRequestData(),
    ) -> list[ModelType]:
        return get_many(session, self.model, filters, req)

    def update_one(
        self,
        session: Session,
        filters: FilterSchemaType,
        data: UpdateSchemaType | dict[str, Any],
        req: FindOneRequestData = FindOneRequestData(),
        commit: bool = False
    ) -> Optional[ModelType]:
        return update_one(session, self.model, filters, data, req, commit)
    
    def update_many(
        self,
        session: Session,
        filters: FilterSchemaType,
        data: UpdateSchemaType,
        req: FindManyRequestData = FindManyRequestData(),
        commit: bool = False
    ) -> list[ModelType]:
        return update_many(session, self.model, filters, data, req, commit)
    
    def delete_one(
        self,
        session: Session,
        filters: FilterSchemaType,
        req: FindOneRequestData = FindOneRequestData(),
        commit: bool = False
    ) -> None:
        return delete_one(session, self.model, filters, req, commit)

    def delete_many(
        self,
        session: Session,
        filters: FilterSchemaType,
        req: FindManyRequestData = FindManyRequestData(),
        commit: bool = False
    ) -> int:
        return delete_many(session, self.model, filters, req, commit)