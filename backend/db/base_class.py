from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        # Convert CamelCase to snake_case if desired, or just use lower
        return cls.__name__.lower() + "s" if not cls.__name__.endswith("s") else cls.__name__.lower()
