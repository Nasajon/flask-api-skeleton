import uuid

from typing import Optional
from pydantic import BaseModel, constr


class ContatoPostDTO(BaseModel):
    id: Optional[uuid.UUID]
    cliente: Optional[uuid.UUID]
    descricao: constr(min_length=1, max_length=150)
    principal: Optional[bool]
    tipo: constr(min_length=1, max_length=100)
    ddd: constr(min_length=1, max_length=100)
    numero: constr(min_length=1, max_length=20)
    ramal: Optional[str]
