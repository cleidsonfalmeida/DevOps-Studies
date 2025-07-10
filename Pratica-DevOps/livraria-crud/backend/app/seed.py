from . import models, database

LIVROS_INICIAIS = [
    {"titulo": "Dom Casmurro", "autor": "Machado de Assis", "preco": 29.90},
    {"titulo": "O Cortiço", "autor": "Aluísio Azevedo", "preco": 25.00},
    {"titulo": "A Moreninha", "autor": "Joaquim Manuel", "preco": 22.50},
    {"titulo": "Memórias Póstumas", "autor": "Machado de Assis", "preco": 34.90},
    {"titulo": "Senhora", "autor": "José de Alencar", "preco": 28.00},
    {"titulo": "Iracema", "autor": "José de Alencar", "preco": 24.50},
    {"titulo": "Vidas Secas", "autor": "Graciliano Ramos", "preco": 31.90},
    {"titulo": "Capitães da Areia", "autor": "Jorge Amado", "preco": 27.00},
    {"titulo": "Grande Sertão: Veredas", "autor": "Guimarães Rosa", "preco": 45.00},
    {"titulo": "Quincas Borba", "autor": "Machado de Assis", "preco": 30.00}
]

def popular_dados():
    db = database.SessionLocal()
    if db.query(models.Livro).count() == 0:
        for item in LIVROS_INICIAIS:
            livro = models.Livro(**item)
            db.add(livro)
        db.commit()
    db.close()
