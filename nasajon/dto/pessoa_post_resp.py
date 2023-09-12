import uuid
import datetime


class PessoaPostResponseDTO:
    id: uuid.UUID
    codigo: str
    created_at: datetime.datetime

    def __init__(self) -> None:
        super().__init__()

        self.id = None
        self.codigo = None
        self.created_at = None
