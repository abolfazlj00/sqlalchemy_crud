from pydantic import BaseModel, ConfigDict

class CustomBaseModel(BaseModel): ...

class ForbidExtraBaseModel(CustomBaseModel):
    model_config = ConfigDict(
        extra="ignore"
    )

class IgnoreExtraBaseModel(CustomBaseModel):
    model_config = ConfigDict(
        extra="ignore"
    )

class AllowExtraBaseModel(CustomBaseModel):
    model_config = ConfigDict(
        extra="allow"
    )

class CreateSchemaBaseModel(IgnoreExtraBaseModel): ...
class UpdateSchemaBaseModel(IgnoreExtraBaseModel): ...
class FilterSchemaBaseModel(IgnoreExtraBaseModel): ...