from pydantic import Field, field_validator, model_validator
from typing import Annotated, Optional, List
from .base import IgnoreExtraBaseModel
from ..enum.sort_directions import SortDirection
from ..typing import FilterSchemaType

class OrderByData(IgnoreExtraBaseModel):
    column: str
    direction: SortDirection = Field(
        default=SortDirection.ASC
    )
    nulls_first: bool = Field(
        default=True,
        description="Whether to put NULL values first"
    )

class SelectFields(IgnoreExtraBaseModel):
    includes: Optional[List[str]] = Field(
        default=None,
        description="Fields to include in response (None returns all fields)"
    )
    excludes: Optional[List[str]] = Field(
        default=None,
        description="Fields to exclude from response"
    )

    @field_validator("includes", "excludes")
    @classmethod
    def check_not_empty(cls, v):
        if v is not None:
            if len(v) == 0:
                raise ValueError("Cannot be empty!")
        return v
    
    @model_validator(mode="after")
    def check_model(self):
        if self.includes and self.excludes:
            raise ValueError("Cannot use 'includes' and 'excludes' simultaneously!")
        if not self.includes and not self.excludes:
            raise ValueError("'includes' or 'excludes' is required!")
        return self

class PaginationData(IgnoreExtraBaseModel):
    limit: Annotated[int, Field(strict=True, ge=1, le=50)] = Field(
        default=20,
        description="Maximum number of results (1-50); default: 20"
    )
    page: Annotated[int, Field(strict=True, ge=1)] = Field(
        default=1,
        description="Page"
    )

    @property
    def offset(self):
        return (self.page - 1) * self.limit


class FindRequestData(IgnoreExtraBaseModel):

    order_by: Optional[OrderByData] = Field(
        default=None,
        description="Sorting criteria"
    )
    fields: Optional[SelectFields] = Field(
        default=None,
        description="Field selection options"
    )

class FindOneRequestData(FindRequestData): ...

class FindManyRequestData(FindRequestData):
    pagination: PaginationData = Field(
        default_factory=PaginationData,
        description="Pagination data"
    )
    