# MC920 / MO443 — Introdução ao Processamento Digital de Imagens

Este repositório contém os Trabalhos 1 e 2 da disciplina.

## 1. Montar o ambiente

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 2. Executar exercícios / métodos

Executar um item específico:

```bash
# Trabalho 1 — exercícios 1 a 13 (padrão)
python main.py NUMERO

# Trabalho 2 — métodos 1 a 12
python main.py NUMERO --trabalho 2
```

Executar tudo que está implementado:

```bash
python run_all.py               # ambos os trabalhos
python run_all.py --trabalho 1  # só o trabalho 1
python run_all.py --trabalho 2  # só o trabalho 2
```

Para refazer arquivos já gerados, adicione `--overwrite`.

## 3. Benchmarks

```bash
# Trabalho 1
python benchmark.py NUMERO --repeats 30 --warmup 3

# Trabalho 2
python benchmark.py NUMERO --trabalho 2 --repeats 30 --warmup 3
```

Os resultados são salvos em `results/benchmarks/`.

## 4. Relatório

Gerar o PDF:

```bash
python build_report.py --report 1   # trabalho 1 (padrão)
python build_report.py --report 2   # trabalho 2
```

Atualizar as figuras a partir dos resultados locais antes de compilar:

```bash
python build_report.py --report 2 --sync-figures
```

Requer LaTeX com `latexmk` instalado.

## 5. Estrutura de pastas

```
src/
├── common/           # utilitários compartilhados
├── trabalho_01/      # exercicio_01 … exercicio_13
└── trabalho_02/      # metodo_01_global … metodo_12_histogramas

docs/
├── relatorio_01/     # relatório do trabalho 1 (LaTeX + PDF)
└── relatorio_02/     # relatório do trabalho 2 (LaTeX + PDF)

data/input/           # entradas baixadas na execução (não versionadas)
results/              # saídas geradas na execução (não versionadas)
```

As figuras em `docs/relatorio*/figuras/` são versionadas porque o LaTeX depende delas.
Rodar os exercícios isoladamente **não** atualiza as figuras do relatório; use `--sync-figures` para isso.
