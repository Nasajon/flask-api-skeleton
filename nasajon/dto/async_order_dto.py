from pydantic import BaseModel, constr


class AsyncOrderDTO(BaseModel):
    msg: constr(min_length=1, max_length=100)
