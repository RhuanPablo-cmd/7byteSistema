# 7byte Sistema de Gestão de Estoque

Aplicação desktop para controle de produtos e movimentações de estoque. O sistema reúne cadastro de itens, registro de entradas e saídas, consulta de saldo, acompanhamento de estoque baixo, relatórios e cópias de segurança em uma interface feita com PyQt5.

## Funcionalidades

- **Dashboard:** resumo de produtos, unidades em estoque, entradas e saídas do mês, valor estimado do estoque, itens com saldo baixo (5 unidades ou menos) e movimentações recentes.
- **Produtos:** cadastro com nome, categoria, preço e quantidade inicial; pesquisa por nome ou categoria; edição dos dados sem alterar o saldo; exclusão somente quando o item está sem saldo e não possui histórico.
- **Movimentações:** registro de entradas e saídas com data e observações. O sistema impede saídas maiores que o saldo disponível.
- **Relatórios:** consulta das movimentações por período e tipo, com totalização e exportação para CSV, compatível com planilhas eletrônicas.
- **Backup:** exportação do banco de dados e restauração a partir de um backup válido. Antes de restaurar, o sistema cria uma cópia de segurança dos dados atuais.
- **Acesso:** login e tela de redefinição de senha.

## Requisitos

- Windows
- Python 3.10 ou superior
- PyQt5

## Instalação e execução

Abra o PowerShell na pasta raiz do projeto, onde estão `README.md`, `base_dados/` e `gestao_estoque/`. Instale a dependência e inicie a aplicação:

```powershell
py -m pip install PyQt5
py gestao_estoque/main.py
```

Para isolar as dependências em um ambiente virtual:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install PyQt5
python gestao_estoque\main.py
```

Se o PowerShell bloquear a ativação do ambiente virtual, execute a política somente para a sessão atual e tente novamente:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

O programa cria `base_dados/estoque.db` automaticamente, caso o banco ainda não exista, usando a estrutura definida em `base_dados/estoque.sql`.

## Primeiro acesso

O esquema inclui uma conta administrativa inicial:

| Usuário | Senha |
| --- | --- |
| `Admin` | `1234` |

Altere essa senha antes de usar o sistema com dados reais. A redefinição disponível na tela de login aceita o nome de usuário sem comprovar a identidade; por isso, esta versão deve ser usada apenas em ambiente local e controlado, até que a recuperação seja protegida por um mecanismo de verificação.

## Arquivos e dados

- `gestao_estoque/main.py`: inicialização, interface e regras da aplicação.
- `Telas.ui/`: telas de login e gestão.
- `base_dados/estoque.sql`: criação das tabelas de usuários, produtos e movimentações, além da conta inicial.
- `base_dados/estoque.db`: banco SQLite utilizado em execução; contém os dados cadastrados e não deve ser apagado sem backup.
- `img/7byte.png`: identidade visual exibida pela aplicação.

Os backups podem ser criados e restaurados pela página **Configurações**. Guarde as cópias em local separado do computador onde o sistema é executado.

## Observações de segurança

Esta aplicação foi estruturada para uso local. As senhas são armazenadas com SHA-256 simples, sem salt, e o fluxo de recuperação não valida a identidade de quem solicita a alteração. Não exponha o sistema ou o banco em rede nem o utilize para dados sensíveis sem antes reforçar a autenticação, a recuperação de conta e o armazenamento de senhas.
