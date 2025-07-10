from pydantic import BaseModel

class LivroBase(BaseModel):
    titulo: str
    autor: str
    preco: float

class Livro(LivroBase):
    id: int

    class Config:
        from_attributes = True

class LivroCreate(BaseModel):
    titulo: str
    autor: str
    preco: float
