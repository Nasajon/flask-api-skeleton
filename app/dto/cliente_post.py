import uuid


class ClientePostDTO:
    id: uuid.UUID
    nome: str
    documento: str

    def __init__(self) -> None:
        super().__init__()

        self.id = None
        self.nome = None
        self.documento = None
