from domain.example.entities.example import Example
from domain.example.value_objects.address import Address
from infrastructure.persistence.db import models


def convert_example_entity_to_db_model(example: Example) -> models.Example:
    return models.Example(
        id=example.id,
        address=example.address.as_generic_type(),
    )

def convert_db_model_to_example_entity(db_example: models.Example) -> Example:
    return Example(id=db_example.id, address=Address(value=db_example.address))
