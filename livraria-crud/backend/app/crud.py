from sqlalchemy.orm import Session
from . import models, schemas

def listar_livros(db: Session):
    return db.query(models.Livro).all()

def buscar_livro(db: Session, livro_id: int):
    return db.query(models.Livro).filter(models.Livro.id == livro_id).first()

def criar_livro(db: Session, livro: schemas.LivroCreate):
    novo = models.Livro(**livro.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

def atualizar_livro(db: Session, livro_id: int, livro: schemas.LivroCreate):
    existente = buscar_livro(db, livro_id)
    if existente:
        existente.titulo = livro.titulo
        existente.autor = livro.autor
        existente.preco = livro.preco
        db.commit()
        db.refresh(existente)
    return existente

def deletar_livro(db: Session, livro_id: int):
    existente = buscar_livro(db, livro_id)
    if existente:
        db.delete(existente)
        db.commit()
    return existente
