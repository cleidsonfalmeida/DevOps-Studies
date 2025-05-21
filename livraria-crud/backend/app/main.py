from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from . import models, database, crud, schemas

app = FastAPI()

# CORS: permitir frontend se comunicar com backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/livros", response_model=list[schemas.Livro])
def listar_livros(db: Session = Depends(get_db)):
    return crud.listar_livros(db)

@app.post("/livros", response_model=schemas.Livro)
def criar_livro(livro: schemas.LivroCreate, db: Session = Depends(get_db)):
    return crud.criar_livro(db, livro)

@app.get("/livros/{id}", response_model=schemas.Livro)
def buscar_livro(id: int, db: Session = Depends(get_db)):
    livro = crud.buscar_livro(db, id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro

@app.put("/livros/{id}", response_model=schemas.Livro)
def atualizar_livro(id: int, livro: schemas.LivroCreate, db: Session = Depends(get_db)):
    atualizado = crud.atualizar_livro(db, id, livro)
    if not atualizado:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return atualizado

@app.delete("/livros/{id}")
def deletar_livro(id: int, db: Session = Depends(get_db)):
    removido = crud.deletar_livro(db, id)
    if not removido:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return {"ok": True, "mensagem": "Livro removido com sucesso"}
