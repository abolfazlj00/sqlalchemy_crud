from pydantic import Field, field_validator, model_validator
from typing import Annotated, Optional, List
from .base import ForbidExtraBaseModel
from ..enum.sort_directions import SortDirection

class OrderByData(ForbidExtraBaseModel):
    column: str
    direction: SortDirection = Field(
        default=SortDirection.ASC
    )
    nulls_first: bool = Field(
        default=True,
        description="Whether to put NULL values first"
    )

class PaginationData(ForbidExtraBaseModel):
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


class FindRequestData(ForbidExtraBaseModel):

    order_by: Optional[OrderByData] = Field(
        default=None,
        description="Sorting criteria"
    )

class FindOneRequestData(FindRequestData): ...

class FindManyRequestData(FindRequestData):
    pagination: PaginationData = Field(
        default_factory=PaginationData,
        description="Pagination data"
    )
    