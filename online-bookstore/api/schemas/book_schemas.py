from pydantic import BaseModel


class BookSchema(BaseModel):
    id: int
    title : str
    # description: str
    author : str