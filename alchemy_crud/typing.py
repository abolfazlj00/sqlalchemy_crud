from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import TypeVar
from .models.base import CreateSchemaBaseModel, UpdateSchemaBaseModel, FilterSchemaBaseModel

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)

CreateSchemaType = TypeVar("CreateSchemaType", bound=CreateSchemaBaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=UpdateSchemaBaseModel)
FilterSchemaType = TypeVar("FilterSchemaType", bound=FilterSchemaBaseModel)