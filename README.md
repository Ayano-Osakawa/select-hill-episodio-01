<div align="center">

<img src="docs/capa.jpg" alt="SELECT HILL — Episódio 1: Eu só queria fazer backup" width="100%">

# SELECT HILL
### Episódio 1 · Eu só queria fazer backup

**Um plantão de TI. Um cabo desconectado. Uma cidade que precisava de um DBA.**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-local-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Episódio](https://img.shields.io/badge/SELECT_HILL-EPIS%C3%93DIO_01-7b2328?style=for-the-badge)

*Banco de dados para universitários tentando passar na matéria — e sobreviver ao plantão.*

</div>

---

> Fui fazer backup à meia-noite de uma sexta-feira 13, com lua de sangue e fumaça na Amazônia. Acabei em Silent Hill. Agora preciso organizar o que sabemos antes que a neblina organize a gente.

Este é o laboratório do primeiro episódio de **SELECT HILL**, do canal Ayano. Aqui você encontra o código para reproduzir o cadastro, executar a consulta mostrada no vídeo e conferir os dados depois de fechar o programa.

## 🗺️ O que encontramos até aqui

| Conceito | Dentro da história | Neste laboratório |
| :--- | :--- | :--- |
| Dado | Um nome ou um lugar registrado | Valores de cada campo |
| Informação | Interpretar os registros para responder uma pergunta | Ler o resultado no contexto |
| Tabela | Organizar pessoas e lugares separadamente | `pessoas` e `locais` |
| Coluna | Uma propriedade do que estamos cadastrando | `id`, `nome`, `regiao`, `ordem` |
| Registro | Um lugar representado em uma linha | Café 5to2 ou Beco inicial |
| Persistência | Fechar o terminal sem esquecer as pistas | Arquivo SQLite no disco |
| Consulta | Pedir uma resposta específica ao arquivo | `SELECT`, `WHERE` e `ORDER BY` |

> [!NOTE]
> `ordem` representa **a ordem do cadastro didático**. Ela não representa a cronologia do acidente de Harry. Os registros deste episódio ficam restritos a Café 5to2, Beco inicial, Harry, Cheryl e Cybil.

## ⚡ Abra o terminal

Você precisa de **Python 3.10 ou superior**. O laboratório usa somente a biblioteca padrão, incluindo `sqlite3`.

Dentro da pasta deste projeto:

```bash
python3 laboratorio.py iniciar
python3 laboratorio.py consultar
```

O primeiro comando cria `build/select-hill.sqlite3`. O segundo abre o arquivo novamente e executa a consulta do episódio.

```text
id | nome
---|-------------
1  | Café 5to2
2  | Beco inicial
```

Execute `consultar` em outro terminal ou depois de fechar e abrir o programa: os dois registros continuam no arquivo.

> [!TIP]
> Rodar `iniciar` novamente preserva o banco existente, incluindo suas alterações. Para experimentar do zero, escolha um novo nome:
>
> ```bash
> python3 laboratorio.py iniciar --banco build/outro-ensaio.sqlite3
> python3 laboratorio.py consultar --banco build/outro-ensaio.sqlite3
> ```

## 🔦 A primeira consulta

A consulta de [sql/03-consulta.sql](sql/03-consulta.sql) é a mesma apresentada no vídeo:

```sql
SELECT id, nome
FROM locais
WHERE ordem <= 2
ORDER BY ordem;
```

| Trecho | O que estamos pedindo |
| :--- | :--- |
| `SELECT id, nome` | Somente o identificador e o nome |
| `FROM locais` | Buscar na tabela de lugares |
| `WHERE ordem <= 2` | Manter os registros cuja ordem é até 2 |
| `ORDER BY ordem` | Apresentar o resultado pela ordem de cadastro |

Ordenar pelo nome muda a apresentação do resultado. **O identificador continua ligado ao mesmo lugar.**

### Prefere executar SQL diretamente?

Com o programa de terminal `sqlite3` instalado, use um arquivo novo:

```bash
mkdir -p build
sqlite3 build/terminal.sqlite3 < sql/01-esquema.sql
sqlite3 build/terminal.sqlite3 < sql/02-dados.sql
sqlite3 -header -column build/terminal.sqlite3 < sql/03-consulta.sql
```

Os scripts de criação e carga são para um banco vazio. Para repetir apenas a consulta, execute somente o último comando.

Para inspecionar os campos e conferir os dois cadastros:

```bash
sqlite3 -header -column build/terminal.sqlite3 < sql/04-conferir.sql
```

## 📻 SQL, SQLite e o arquivo

| Nome | Papel |
| :--- | :--- |
| **SQL** | A linguagem usada para escrever instruções |
| **SQLite** | O mecanismo que executa essas instruções |
| **`select-hill.sqlite3`** | O arquivo que guarda os dados e sua estrutura |

Guardar o relato de Harry não comprova que ele é verdadeiro. Da mesma forma, ter tabelas de pessoas e lugares **não registra quem esteve em cada lugar**. Nosso cadastro ainda não permite responder quem estava no café.

*A neblina já inventa bastante coisa. O seu SELECT não precisa.*

## ↩️ “Qualquer coisa a gente dá rollback”

A abertura também cita `ROLLBACK`. Este exemplo extra usa uma rotina de manutenção isolada do cadastro principal:

```bash
python3 laboratorio.py rollback
```

```text
antes: pendente
provisorio: em teste
apos rollback: pendente
```

A alteração fica dentro de uma transação. `ROLLBACK` descarta essa alteração, retornando à situação anterior. Ele não desfaz ações físicas nem fecha o portal.

A versão em SQL está em [extras/rollback.sql](extras/rollback.sql):

```bash
sqlite3 -header -column :memory: < extras/rollback.sql
```

## 💾 Fazer backup, desta vez de verdade

O exemplo abaixo usa a API de backup do SQLite para copiar o banco:

```bash
python3 backup.py build/select-hill.sqlite3 build/backup.sqlite3
python3 laboratorio.py consultar --banco build/backup.sqlite3
```

O script confere a integridade estrutural da cópia. A consulta permite conferir os registros do episódio no arquivo copiado. Um destino que já existe é preservado; escolha outro nome para uma nova cópia.

> [!IMPORTANT]
> Copiar para outro arquivo na mesma máquina demonstra o procedimento. Um plano de recuperação também precisa considerar um destino separado, os dados necessários ao sistema e testes de restauração.

## 🧩 Sua vez de investigar

Faça os [exercícios](exercicios/enunciados.md) usando somente os dados deste episódio.

<details>
<summary><strong>Já tentou? Abrir as respostas</strong></summary>

As consultas e explicações estão em [exercicios/respostas.sql](exercicios/respostas.sql).

</details>

## ✅ Conferir o laboratório

```bash
python3 -m unittest discover -s testes -v
```

Os testes verificam o resultado da consulta, os campos da tabela, a persistência em outro processo, a preservação de alterações, o rollback e a leitura do backup. Usam bancos temporários, separados do seu laboratório.

## 🗂️ Arquivos

```text
select-hill-episodio-01/
├── README.md
├── .gitignore
├── laboratorio.py          # Criar, consultar e demonstrar rollback
├── backup.py               # Copiar o banco usando a API do SQLite
├── sql/
│   ├── 01-esquema.sql      # Estrutura dos cadastros
│   ├── 02-dados.sql        # Dados apresentados no episódio
│   ├── 03-consulta.sql     # A primeira consulta
│   └── 04-conferir.sql     # Conferência dos campos e cadastros
├── extras/
│   └── rollback.sql       # Exemplo da manutenção na abertura
├── exercicios/
│   ├── enunciados.md
│   └── respostas.sql
├── testes/
│   └── test_laboratorio.py
└── docs/
    ├── capa.jpg
    └── resultado-esperado.csv
```

O arquivo do banco é gerado por você. A pasta `build/` e os caches do Python estão no `.gitignore`.

---

<div align="center">

**Criado por Ayano · SELECT HILL**

Material educativo independente inspirado em *Silent Hill*. O banco foi criado para a série e não representa os arquivos internos do jogo.

**A investigação continua.**

</div>
