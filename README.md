# 🍓 Feira API

## Descrição

Catálogo de frutas com API REST em **FastAPI** e interface web responsiva para cadastrar, editar, excluir e pesquisar produtos. Cada item tem ID numérico, imagem, sabor, cor e indicação de sementes; o catálogo fica em ordem alfabética e os detalhes podem ser consultados em JSON.

## ✨ O que tem no projeto

- Catálogo com busca instantânea e ordenação alfabética.
- Cadastro e edição de frutas com nome, sabor, cor, imagem e indicação de sementes.
- Exclusão com confirmação visual.
- Identificadores numéricos estáveis durante a execução do servidor.
- Consulta dos detalhes de cada item em formato JSON.
- Interface responsiva com imagens, animações, glitter e uma trilha instrumental original controlada pelo usuário.
- Documentação interativa da API pelo Swagger UI.

## 🧰 Tecnologias

- Python
- FastAPI e Pydantic
- HTML, CSS e JavaScript
- Web Audio API para a trilha instrumental

## 🚀 Como executar

Requer Python 3.10 ou superior.

1. Clone o repositório e acesse a pasta:

	```bash
	git clone <URL_DO_REPOSITORIO>
	cd construcao-api
	```

2. Crie e ative um ambiente virtual:

	```bash
	python -m venv .venv
	source .venv/bin/activate
	```

	No Windows, ative com:

	```powershell
	.venv\Scripts\activate
	```

3. Instale as dependências e inicie o servidor:

	```bash
	python -m pip install fastapi uvicorn
	uvicorn app:app --reload
	```

4. Acesse:

	- Site: http://127.0.0.1:8000
	- Documentação interativa: http://127.0.0.1:8000/docs

## 📡 Rotas da API

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/produtos` | Lista os produtos em ordem alfabética. |
| `GET` | `/produtos/{nome}` | Busca um produto pelo nome. |
| `POST` | `/produtos` | Cadastra um produto. |
| `PUT` | `/produtos/{id}` | Atualiza um produto pelo ID. |
| `DELETE` | `/produtos/{id}` | Exclui um produto pelo ID. |

Exemplo de corpo para cadastro ou edição:

```json
{
  "nome": "Kiwi",
  "imagem": null,
  "sabor": "Doce e ácido",
  "cor": "Marrom e verde",
  "tem_sementes": true
}
```

`imagem` pode receber uma URL; se for omitida no cadastro, a API seleciona uma imagem externa com base no nome do produto.

## 📁 Estrutura

```text
.
├── app.py
├── README.md
└── static/
	 └── index.html
```

## ℹ️ Observações

- Os produtos são armazenados em memória. Eles voltam aos valores iniciais quando o servidor é reiniciado.
- A imagem automática e algumas imagens do catálogo dependem de serviços externos e de conexão com a internet.
- A música é instrumental e sintetizada no navegador; o navegador só a inicia após uma interação do usuário.