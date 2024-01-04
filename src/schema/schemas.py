from pydantic import BaseModel, Field

# Model Pydantic, używany do walidacji danych wejściowych dla żądań.
class Dummy(BaseModel):
    # Pole `id` typu UUID jest zakomentowane, aby uniknąć konfliktu z modelem SQLAlchemy.
    # id: UUID
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)