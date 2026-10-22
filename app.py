from pathlib import Path
from urllib.parse import quote

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()

produtos = [
    {"id": 1, "nome": "Maçã", "imagem": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?auto=format&fit=crop&w=800&q=80", "sabor": "Doce e levemente ácido", "cor": "Vermelha", "tem_sementes": True},
    {"id": 2, "nome": "Abacate", "imagem": "https://images.unsplash.com/photo-1523049673857-eb18f1d7b578?auto=format&fit=crop&w=800&q=80", "sabor": "Suave e cremoso", "cor": "Verde", "tem_sementes": True},
    {"id": 3, "nome": "Melancia", "imagem": "https://images.unsplash.com/photo-1587049352846-4a222e784d38?auto=format&fit=crop&w=800&q=80", "sabor": "Doce e refrescante", "cor": "Verde e vermelha", "tem_sementes": True},
    {"id": 4, "nome": "Blueberry", "imagem": "https://images.unsplash.com/photo-1498557850523-fd3d118b962e?auto=format&fit=crop&w=800&q=80", "sabor": "Doce e levemente ácido", "cor": "Azul-arroxeada", "tem_sementes": True},
    {"id": 5, "nome": "Morango", "imagem": "https://images.unsplash.com/photo-1464965911861-746a04b4bca6?auto=format&fit=crop&w=800&q=80", "sabor": "Doce e levemente ácido", "cor": "Vermelha", "tem_sementes": True},
]
proximo_id = 6


class NovoProduto(BaseModel):
    nome: str = Field(min_length=1, max_length=80)
    imagem: HttpUrl | None = None
    sabor: str = Field(min_length=1, max_length=80)
    cor: str = Field(min_length=1, max_length=40)
    tem_sementes: bool

@app.get("/")
def inicio():
    return FileResponse(Path(__file__).parent / "static" / "index.html")



@app.get("/produtos")
def listar_produtos():
    return sorted(produtos, key=lambda produto: produto["nome"].casefold())

@app.get("/produtos/{item}")
def buscar_item(item:str):
    produto = next(
        (produto for produto in produtos if produto["nome"].casefold() == item.casefold()),
        None,
    )
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


@app.post("/produtos", status_code=201)
def adicionar_produto(novo_produto: NovoProduto):
    global proximo_id

    nome = novo_produto.nome.strip()
    if not nome:
        raise HTTPException(status_code=422, detail="O nome do produto não pode ficar vazio")
    if any(produto["nome"].casefold() == nome.casefold() for produto in produtos):
        raise HTTPException(status_code=409, detail="Este produto já está cadastrado")

    imagem = novo_produto.imagem or (
        f"https://loremflickr.com/800/600/{quote(nome)}?lock={proximo_id}"
    )
    produto = {
        "id": proximo_id,
        "nome": nome,
        "imagem": str(imagem),
        "sabor": novo_produto.sabor.strip(),
        "cor": novo_produto.cor.strip(),
        "tem_sementes": novo_produto.tem_sementes,
    }
    proximo_id += 1
    produtos.append(produto)
    return produto


@app.put("/produtos/{item}")
def atualizar_produto(item: int, dados_atualizados: NovoProduto):
    produto = next((produto for produto in produtos if produto["id"] == item), None)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    nome = dados_atualizados.nome.strip()
    if not nome:
        raise HTTPException(status_code=422, detail="O nome do produto não pode ficar vazio")
    if any(
        outro["id"] != item and outro["nome"].casefold() == nome.casefold()
        for outro in produtos
    ):
        raise HTTPException(status_code=409, detail="Este produto já está cadastrado")

    produto.update(
        {
            "nome": nome,
            "imagem": str(dados_atualizados.imagem or produto["imagem"]),
            "sabor": dados_atualizados.sabor.strip(),
            "cor": dados_atualizados.cor.strip(),
            "tem_sementes": dados_atualizados.tem_sementes,
        }
    )
    return produto


@app.delete("/apagar/{item}")
@app.delete("/produtos/{item}")
def deletar_produtos(item: int):
    produto = next((produto for produto in produtos if produto["id"] == item), None)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    produtos.remove(produto)
    return {"mensagem": f"O item {produto['nome']} foi removido!", "id": item}