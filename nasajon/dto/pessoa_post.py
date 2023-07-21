import uuid

from typing import Optional
from pydantic import BaseModel, constr


class PessoaPostDTO(BaseModel):
    id: Optional[uuid.UUID]
    nome: constr(min_length=1, max_length=100)
    documento: constr(min_length=11, max_length=14)
