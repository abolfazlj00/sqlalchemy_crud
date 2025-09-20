from pydantic import BaseModel, ConfigDict, Field
from typing import List

class CustomBaseModel(BaseModel): ...

class ForbidExtraBaseModel(CustomBaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )

class IgnoreExtraBaseModel(CustomBaseModel):
    model_config = ConfigDict(
        extra="ignore"
    )

class AllowExtraBaseModel(CustomBaseModel):
    model_config = ConfigDict(
        extra="allow"
    )

class CreateSchemaBaseModel(ForbidExtraBaseModel): ...
class ReadSchemaBaseModel(IgnoreExtraBaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
class UpdateSchemaBaseModel(ForbidExtraBaseModel): ...

class FilterSchemaBaseModel(ForbidExtraBaseModel):

    and_: List["FilterSchemaBaseModel"] = Field(default_factory=list)
    or_: List["FilterSchemaBaseModel"] = Field(default_factory=list)