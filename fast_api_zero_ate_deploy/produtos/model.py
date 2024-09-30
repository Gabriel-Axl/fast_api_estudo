from banco.database import Base
from sqlalchemy import Column, Integer, String, Float

class Produto(Base):
    __tablename__ = "produto"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50))
    preco = Column(Float)
    descricao = Column(String(100))
    quantidade = Column(Integer)
    
    def __repr__(self):
        return f"<Produto {self.nome}>"