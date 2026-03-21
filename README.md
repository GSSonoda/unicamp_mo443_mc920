# MO443 / MC920

Repositório do Trabalho 1 de Introdução ao Processamento Digital de Imagens.

O trabalho tem 13 exercícios. A organização foi feita para deixar o fluxo simples para o professor, separar a execução do código da geração do relatório e reaproveitar o que é comum entre os exercícios.

## Fluxo recomendado

Instale a única dependência do código:

```bash
python3 -m pip install -r requirements.txt
```

Execute um exercício específico:

```bash
python3 main.py 1
```

Execute tudo que já estiver implementado:

```bash
python3 run_all.py
```

Gere o PDF do relatório em uma etapa separada:

```bash
python3 build_report.py
```

Essa separação evita que um problema de LaTeX atrapalhe a execução dos exercícios.

## Onde ficam os arquivos

- Inputs baixados ou copiados: `data/input/exercicio_XX/`
- Resultados gerados pelos exercícios: `results/exercicio_XX/`
- Figuras copiadas para o relatório: `docs/relatorio/figuras/exercicio_XX/`
- Fonte do relatório em LaTeX: `docs/relatorio/relatorio.tex`
- PDF final do relatório: `docs/relatorio/relatorio.pdf`

Ao executar um exercício, o projeto:

- baixa automaticamente as imagens de entrada necessárias, se ainda não existirem;
- salva as entradas em `data/input/exercicio_XX/`;
- executa a transformação;
- salva as saídas em `results/exercicio_XX/`.
- copia para `docs/relatorio/figuras/exercicio_XX/` as imagens que serão usadas como figuras no LaTeX.

No caso do exercício 1, os caminhos principais ficam assim:

- input: `data/input/exercicio_01/baboon_monocromatica.png`
- outputs:
  - `results/exercicio_01/baboon_rotacao_90_horario.png`
  - `results/exercicio_01/baboon_rotacao_180.png`
  - `results/exercicio_01/baboon_rotacao_270_horario.png`
- figures used in the report:
  - `docs/relatorio/figuras/exercicio_01/input_baboon_monocromatica.png`
  - `docs/relatorio/figuras/exercicio_01/baboon_rotacao_90_horario.png`
  - `docs/relatorio/figuras/exercicio_01/baboon_rotacao_180.png`
  - `docs/relatorio/figuras/exercicio_01/baboon_rotacao_270_horario.png`
- final PDF:
  - `docs/relatorio/relatorio.pdf`

Para sobrescrever entradas e saídas já existentes:

```bash
python3 main.py 1 --overwrite
```

## Para o professor

Se a ideia for apenas reproduzir o que já está implementado, os comandos principais são:

```bash
python3 -m pip install -r requirements.txt
python3 run_all.py
python3 build_report.py
```

O primeiro comando instala `Pillow`, o segundo gera as imagens e organiza os arquivos do trabalho, e o terceiro compila o PDF do relatório a partir do LaTeX.

## Estrutura

```text
.
├── docs/
│   ├── enunciado/
│   └── relatorio/
├── data/
│   └── input/
│       └── exercicio_XX/
├── results/
│   └── exercicio_XX/
├── src/
│   ├── common/
│   └── exercicio_XX/
├── main.py
└── requirements.txt
```

## Ideia da estrutura

- `src/common/` concentra o que se repete entre exercícios.
- `src/exercicio_XX/` contém a lógica específica de cada exercício.
- `data/input/exercicio_XX/` guarda as entradas usadas.
- `results/exercicio_XX/` guarda as saídas geradas.
- `docs/relatorio/figuras/exercicio_XX/` guarda as figuras usadas no relatório.
- `build_report.py` compila o PDF sem interferir na execução dos exercícios.

## O que já está implementado

- Exercício 1: rotação de imagens monocromáticas em 90, 180 e 270 graus.
- Os demais exercícios continuam só com a estrutura de pastas e README.

## Observação

No exercício 1, a leitura e escrita da imagem PNG usam Pillow, mas a rotação é feita manualmente por manipulação de índices, como pedido no enunciado.
