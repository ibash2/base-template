from pydantic import BaseModel

from domain.entities.account import Account, AccountInfo
from presentation.api.controllers.schemas import BaseQueryResponseSchema


class GetAccountInfoRequestSchema(BaseModel):
    address: str


class GetAccountInfoResponseSchema(BaseModel):
    balance: int
    energy: int
    bandwidth: int

    @classmethod
    def from_entity(cls, account_info: AccountInfo) -> "GetAccountInfoResponseSchema":
        return cls(
            balance=account_info.balance,
            energy=account_info.energy,
            bandwidth=account_info.bandwidth,
        )


class AccountDetailSchema(BaseModel):
    address: str

    @classmethod
    def from_entity(cls, account: Account) -> "AccountDetailSchema":
        return cls(
            address=account.address.as_generic_type(),
        )


class GetAccountsQueryResponseSchema(
    BaseQueryResponseSchema[list[AccountDetailSchema]],
): ...
