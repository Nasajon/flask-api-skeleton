import datetime
import uuid


class Pessoa:

    id: uuid.UUID
    codigo: str
    nome: str
    documento: str
    created_at: datetime.datetime

    def __init__(self) -> None:
        super().__init__()

        self.id = None
        self.codigo = None
        self.nome = None
        self.documento = None
        self.created_at = None
