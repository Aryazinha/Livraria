# Livraria - Sistema de Gerenciamento

Este é um projeto de sistema de gerenciamento para uma livraria, desenvolvido como parte dos meus estudos de desenvolvimento Web Full Stack. O objetivo é permitir o controle de acervo, vendas e organização dos livros.

## Tecnologias Utilizadas
* **Linguagem:** Python
* **Framework Web:** Flask
* **ORM:** SQLAlchemy
* **Banco de Dados:** SQLite 
* **Design:** CSS Moderno

## Como rodar o projeto localmente

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/SEU_USUARIO/Livraria.git](https://github.com/SEU_USUARIO/Livraria.git)

2. **Criar o ambiente**
   ```bash
   python -m venv venv

3. **Ative o ambiente virtual:**
   ```bash
    # Ativar (Windows)
   venv\\Scripts\\activate

    # Ativar (Linux/Mac)
    source venv/bin/activate
   
4. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt

5. **Execute a aplicação**
   ```bash
   flask run


## Estrutura do Projeto
* `app/`: Contém a lógica principal, rotas e modelos da aplicação.
* `migrations/`: Histórico de alterações no banco de dados.
* `instance/`: Arquivos de instância local (banco de dados).
* `config.py`: Configurações gerais do Flask.

---
Desenvolvido por Thales de Lima Dias - Estudante de Ciência da Computação na UEPB.
