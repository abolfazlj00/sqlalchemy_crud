from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import TypeVar
from .models.base import CreateSchemaBaseModel, ReadSchemaBaseModel, UpdateSchemaBaseModel, FilterSchemaBaseModel

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)

CreateSchemaType = TypeVar("CreateSchemaType", bound=CreateSchemaBaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=ReadSchemaBaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=UpdateSchemaBaseModel)
FilterSchemaType = TypeVar("FilterSchemaType", bound=FilterSchemaBaseModel)