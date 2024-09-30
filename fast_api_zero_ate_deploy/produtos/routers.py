from fastapi import APIRouter, Depends
from banco.dependencias import get_db
from pydantic import BaseModel
from sqlalchemy.orm import Session
from produtos.model import Produto

router = APIRouter(prefix="/produtos")

class ProdutoDTO(BaseModel):
    nome: str
    preco: float
    descricao: str
    quantidade: int
    
@router.get("/")
def listar_produtos(db: Session = Depends(get_db)):
    produtos = db.query(Produto).all()
    return produtos

@router.get("/{produto_id}")
def buscar_produto(produto_id: int, db: Session = Depends(get_db) ):
    try:
        produto = db.query(Produto).filter(Produto.id == produto_id).first()
    except Exception as e:
        print(e)
        return {"mensagem": "Produto não encontrado"}
    return produto

@router.post("/")
def criar_produto(produto: ProdutoDTO, db: Session = Depends(get_db)):
    novo_produto = Produto(nome=produto.nome, preco=produto.preco, descricao=produto.descricao, quantidade=produto.quantidade)
    try:
        db.add(novo_produto)
        db.commit()
        db.refresh(novo_produto)
    except Exception as e:
        print(e)
        db.rollback()    
        
    return {"mensagem": "Produto criado com sucesso", "Produto": novo_produto}

@router.put("/{produto_id}")
def atualizar_produto(produto_id: int, 
                      produto: ProdutoDTO, 
                      db: Session = Depends(get_db)):
    try:
        db.query(Produto).filter(Produto.id == produto_id).update({
            Produto.nome: produto.nome,
            Produto.preco: produto.preco,
            Produto.descricao: produto.descricao,
            Produto.quantidade: produto.quantidade
        })
        db.commit()
        produto_atualizado = db.query(Produto).filter(Produto.id == produto_id).first()
    except Exception as e:
        print(e)
        db.rollback()
        return {"mensagem": str(e)}
    
    return produto_atualizado

@router.delete("/{produto_id}")
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    try:
        db.query(Produto).filter(Produto.id == produto_id).delete()
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        return {"mensagem": str(e)}
    
    return {"mensagem": f"Produto {produto_id} deletado com sucesso"}