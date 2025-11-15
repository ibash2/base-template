from pydantic import BaseModel

from application.example import dto
from domain.example.entities.example import Example
from presentation.api.controllers.schemas import BaseQueryResponseSchema


class GetExampleInfoRequest(BaseModel):
    address: str


class GetExampleInfoResponse(BaseModel):
    balance: int
    energy: int
    bandwidth: int

    @classmethod
    def from_dto(cls, example_info: dto.ExampleInfo) -> "GetExampleInfoResponse":
        return cls(
            balance=example_info.balance,
            energy=example_info.energy,
            bandwidth=example_info.bandwidth,
        )


class ExampleInfoDetail(BaseModel):
    address: str

    @classmethod
    def from_entity(cls, example: Example) -> "ExampleInfoDetail":
        return cls(
            address=example.address.as_generic_type(),
        )


class GetExamplesQueryResponse(
    BaseQueryResponseSchema[list[ExampleInfoDetail]],
): ...
