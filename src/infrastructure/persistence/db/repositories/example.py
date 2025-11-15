from typing import Iterable
from dataclasses import dataclass

from sqlalchemy import select, or_, and_

from domain.example.entities.example import Example
from infrastructure.persistence.db import models
from infrastructure.persistence.db.converters import (
    convert_example_entity_to_db_model,
    convert_db_model_to_example_entity,
)
from application.example.interfaces.persistence.repo import ExampleRepo
from infrastructure.persistence.db.repositories.base import SQLAlchemyRepo


@dataclass
class SqlAlchemyExampleRepo(SQLAlchemyRepo, ExampleRepo):
    async def add_account(self, example: Example) -> None:
        db_account = convert_example_entity_to_db_model(example)
        self.session.add(db_account)
        try:
            await self.session.flush((db_account,))
        except Exception as e:
            return ValueError("Sql Error")

    async def get_accounts(
        self, offset: int, limit: int
    ) -> tuple[Iterable[Example], int]:
        stmt = select(models.Example).offset(offset).limit(limit)
        db_examples = await self.session.scalars(stmt)

        return map(convert_db_model_to_example_entity, db_examples), len(db_examples)
