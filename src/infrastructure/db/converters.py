from dataclasses import asdict

from domain.entities.account import Account
from domain.values.address import Address
from infrastructure.db import models


def convert_account_entity_to_db_model(account: Account) -> models.Account:
    return models.Account(
        id=account.id,
        address=account.address.as_generic_type(),
    )


def convert_db_model_to_account_entity(db_account: models.Account) -> Account:
    return Account(id=db_account.id, address=Address(value=db_account.address))
