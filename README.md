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
- Dependencias Python listadas em `requirements.txt`

## Instalação e execução

Abra o PowerShell na pasta raiz do projeto e instale as dependências:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python gestao_estoque\main.py
```

## Gerar o executável para Windows

Com Python instalado, execute na raiz do projeto:
```powershell
py -m venv .venv-build
.\build.ps1
```

O script instala as dependências de build, cria um ícone `.ico` a partir de `img/7byte.png` e gera o executável de arquivo único:

```powershell
dist\7byteSistema.exe
```

O executável inclui as telas, o esquema do banco e o logo. Ao executar, os dados são gravados em `%LOCALAPPDATA%\7byteSistema\estoque.db`, fora do executável, para que continuem disponíveis após fechar o programa. No modo Python, o banco fica em `base_dados/estoque.db`. Em ambos os casos, ele é criado automaticamente usando `base_dados/estoque.sql`.

## Baixar para Windows

Baixe o executável pronto: [7byteSistema.exe](https://github.com/RhuanPablo-cmd/7byteSistema/raw/refs/heads/main/dist/7byteSistema.exe). Não é necessário instalar Python. No primeiro acesso, use o usuário `Admin` e a senha `1234` e altere a senha antes de usar dados reais.

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
- `base_dados/estoque.db`: banco local criado durante a execução em modo Python; não é versionado e não deve ser apagado sem backup.
- `img/7byte.png`: identidade visual exibida pela aplicação.
- `build.ps1` e `requirements-build.txt`: geração reproduzível do executável Windows.

Os backups podem ser criados e restaurados pela página **Configurações**. Guarde as cópias em local separado do computador onde o sistema é executado.

## Publicar no GitHub

O `.gitignore` exclui ambientes virtuais, arquivos temporários, banco de dados local, telas antigas de backup e arquivos gerados de build. O executável Windows pronto fica em `dist/7byteSistema.exe` para download; gere uma nova versão com `build.ps1` quando o código ou o sistema mudar.

## Observações de segurança

Esta aplicação foi estruturada para uso local. As senhas são armazenadas com SHA-256 simples, sem salt, e o fluxo de recuperação não valida a identidade de quem solicita a alteração. Não exponha o sistema ou o banco em rede nem o utilize para dados sensíveis sem antes reforçar a autenticação, a recuperação de conta e o armazenamento de senhas.
