from sqlalchemy.orm import Session
from typing import Generic, Type, Any, Optional
from ..typing import *
from ..models.query import FindOneRequestData, FindManyRequestData
from ..functions.create import create_one
from ..functions.read import get_one, get_many
from ..functions.update import update_one, update_many
from ..functions.delete import delete_one, delete_many

class CRUDBase(Generic[ModelType, CreateSchemaType, ReadSchemaType, UpdateSchemaType, FilterSchemaType]):
    def __init__(self, model_cls: Type[ModelType], read_cls: Type[ReadSchemaType]):
        self.model_cls = model_cls
        self.read_cls = read_cls

    def create_one(
        self,
        session: Session,
        data: CreateSchemaType,
        commit: bool = False
    ):
        return create_one(session, self.model_cls, data, self.read_cls, commit)

    def get_one(
        self,
        session: Session,
        filters: FilterSchemaType,
        req: Optional[FindOneRequestData] = None,
    ):
        return get_one(session, self.model_cls, filters, self.read_cls, req)
        
    def get_many(
        self,
        session: Session,
        filters: FilterSchemaType,
        req: Optional[FindManyRequestData] = None
    ):
        return get_many(session, self.model_cls, filters, self.read_cls, req)

    def update_one(
        self,
        session: Session,
        filters: FilterSchemaType,
        data: UpdateSchemaType | dict[str, Any],
        req: Optional[FindOneRequestData] = None,
        commit: bool = False
    ):
        return update_one(session, self.model_cls, filters, data, self.read_cls, req, commit)
    
    def update_many(
        self,
        session: Session,
        filters: FilterSchemaType,
        data: UpdateSchemaType,
        req: Optional[FindManyRequestData] = None,
        commit: bool = False
    ):
        return update_many(session, self.model_cls, filters, data, self.read_cls, req, commit)
    
    def delete_one(
        self,
        session: Session,
        filters: FilterSchemaType,
        req: FindOneRequestData = FindOneRequestData(),
        commit: bool = False
    ) -> None:
        return delete_one(session, self.model_cls, filters, req, commit)

    def delete_many(
        self,
        session: Session,
        filters: FilterSchemaType,
        req: FindManyRequestData = FindManyRequestData(),
        commit: bool = False
    ) -> int:
        return delete_many(session, self.model_cls, filters, req, commit)
