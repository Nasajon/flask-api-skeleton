import datetime
import uuid

from app.model.abstract_model import AbstractModel


class Cliente(AbstractModel):

    id: uuid.UUID
    nome: str
    documento: str
    created_at: datetime.datetime

    def __init__(self) -> None:
        super().__init__()

        self.id = None
        self.nome = None
        self.documento = None
        self.created_at = None
